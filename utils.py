# Utility file for some useful functions.

from datetime import datetime


def epoch_to_sec(unix_time):
    unix_time_seconds = int(unix_time)

    # Milliseconds takes 2 Bytes storage. So, to convert it into unsigned short, lets just take all the bits upto 16 bit.

    millisec_through_sec = round((unix_time - unix_time_seconds)*1000)
    milliseconds = (millisec_through_sec & 0xffff)

    return unix_time_seconds, milliseconds


def unix_to_datetime(unix_time):
    unix_timestamp = unix_time / 1000

    date_time = datetime.fromtimestamp(unix_timestamp)
    date_time.strftime('%d/%m/%Y %H:%M:%S.%f')

    return date_time

