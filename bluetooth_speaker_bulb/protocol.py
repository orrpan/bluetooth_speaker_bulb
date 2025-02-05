from .const import *


def encode_msg(category, function, data=[]):
    """
    Construct a message

    :param category: category to use
    :param function: function to use
    :param data: int, list or tuple, data for function
    :return: encoded msg
    """
    if isinstance(data, int):
        # Only one int as data, put in list, length will be 1
        data = [data]
    msg = bytearray([0x55, 0xaa, len(data), category, function])
    for d in data:
        msg.append(d)
    msg.append(encode_checksum(msg))

    return msg

# Checksum


def encode_checksum(msg):
    """
    Construct checksum for msg to send

    :param msg: encoded message
    :return: checksum
    """
    checksum_multiple = 256  # 0x100
    hex_sum = sum(i for i in msg) + 1
    return ((checksum_multiple * len(msg)) - hex_sum) % checksum_multiple

# Decode


def decode_function(buffer):
    """
    Retrieve

    :param buffer: buffer to decode not pretty
    """
    if buffer is None:
        return []
    if len(buffer) < 1:
        return []
    c = buffer[3]
    f = buffer[4]

    if c == GetBulbCategory.light.value:
        if f == GetLightFunction.status.value:
            return decode_light_info(buffer)

    if c == GetBulbCategory.timer.value:
        if f == GetTimerFunction.auto_light.value \
                or f == GetTimerFunction.auto_music.value:
            return decode_time_auto(buffer)

        if f == GetTimerFunction.alarm_1.value \
                or f == GetTimerFunction.alarm_2.value \
                or f == GetTimerFunction.alarm_3.value:
            return decode_time_alarm(buffer)

    if c == GetBulbCategory.speaker.value:
        if f == GetSpeakerFunction.volume.value:
            return decode_speaker_volume(buffer)

        if f == GetSpeakerFunction.equalizer.value:
            return decode_speaker_equlizer(buffer)

    return []

# Light


def decode_light_info(buffer):
    """
    Decode a message with device info

    :param buffer: buffer to decode

    Light package
    0:  55  header
    1:  aa  header
    2:  09  data lenght
    3:  88  Catagory (88 light receive, 08 light send)
    4:  15  Function
    5:  00  R
    6:  00  G
    7:  00  B
    8:  75  white intensity cold. buffer 8 + 9; int(0x75)+int(0x8a) = 255; hex((7*16+5)+(8*16+10)) = 0xff
    9:  8a  white intensity warm. buffer 8 + 9; int(0x75)+int(0x8a) = 255; hex((7*16+5)+(8*16+10)) = 0xff
    10: 8d  brightness
    11: 01  on/off
    12: 00  effect
    13: 50  ?
    14: 7d  checksum
    """
    info = {
        'r':                buffer[5],
        'g':                buffer[6],
        'b':                buffer[7],
        'cold':             buffer[8],
        'warm':             buffer[9],
        'brightness':       buffer[10],
        'on':               buffer[11],
        'effect_raw':       buffer[12],
    }
    return info

# Timer


def decode_time_auto(buffer):
    """
    Decode a message with device info

    :param buffer: buffer to decode

    Timer package
    0:  55  header
    1:  aa  header
    2:  05  data lenght
    3:  85  Catagory (85 timer receive, 08 timer send)
    4:  23  Function (auto light 23, auto music 22)
    5:  00  on/off
    6:  0c  start hour
    7:  00  start minute
    8:  0c  stop hour
    9:  00  stop minute
    10: 3b  checksum
    """
    info = {
        'function':         buffer[4],
        'on':               buffer[5],
        'start_hour':       buffer[6],
        'start_minut':      buffer[7],
        'stop_hour':        buffer[8],
        'stop_minute':      buffer[9],
    }
    return info


def decode_time_alarm(buffer):
    """
    Decode a message with device info

    :param buffer: buffer to decode

    Timer package
    0:  55  header
    1:  aa  header
    2:  0a  data lenght
    3:  85  Catagory (85 timer receive, 08 timer send)
    4:  04  Function (04 alarm1, 08 alarm2, 0c alarm3)
    5:  00  ?
    6:  14  ?
    7:  10  ?
    8:  01  ?
    9:  01  ?
    10: 01  ?
    11: 06  hour
    12: 2d  minute
    13: 00  ?
    14: 01  on/off
    15: 12  checksum
    """
    info = {
        'alarm_no':     buffer[4],
        'alarm_hour':   buffer[11],
        'alarm_minute': buffer[12],
        'alarm_on':     buffer[14],
    }
    return info

# Speaker


def decode_speaker_volume(buffer):
    """
    Decode a message with device info

    :param buffer: buffer to decode

    Speaker package
    0:  55  header
    1:  aa  header
    2:  01  data lenght
    3:  84  Catagory (84 speaker receive, 08 speaker send)
    4:  04  Function (volume)
    5:  20  volume
    6:  57  checksum
    """
    info = {
        'volume':       buffer[5],
    }
    return info


def decode_speaker_equlizer(buffer):
    """
    Decode a message with device info

    :param buffer: buffer to decode

    Speaker package
    0:  55  header
    1:  aa  header
    2:  01  data lenght
    3:  84  Catagory (84 speaker receive, 08 speaker send)
    4:  14  Function (equlizer)
    5:  32  80_level
    6:  32  200_level
    7:  32  500_level
    8:  32  2k_level
    9:  32  8k_level
    10: 69  checksum
    """
    info = {
        'frequency_80':        buffer[5],
        'frequency_200':       buffer[6],
        'frequency_500':       buffer[7],
        'frequency_2k':        buffer[8],
        'frequency_8k':        buffer[9],
    }
    return info
