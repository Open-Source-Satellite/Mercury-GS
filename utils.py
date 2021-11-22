# Utility file for some useful functions.

def epoch_to_sec(unix_time):
    unix_time_seconds = int(unix_time)

    # Milliseconds takes 2 Bytes storage. So, to convert it into unsigned short, lets just take all the bits upto 16 bit.

    millisec_through_sec = round((unix_time - unix_time_seconds)*1000)
    milliseconds = (millisec_through_sec & 0xffff)

    return unix_time_seconds, milliseconds

