from construct import *
from sampleformat import *

# The response type returned by ProtocolWrapper
class ProtocolStatus(object):
    START_MSG = 'START_MSG'
    IN_MSG = 'IN_MSG'
    MSG_OK = 'MSG_OK'
    ERROR = 'ERROR'


class ProtocolWrapper(object):
    """ Wraps or unwraps a byte-stuffing header/footer protocol.

        First, create an object with the desired parameters.
        Then, to wrap a data block with a protocol, simply call
        wrap().
        To unwrap, the object is used as a state-machine that is
        fed a byte at a time by calling input(). After each byte
        a ProtocolStatus is returned:
         * ERROR: check .last_error for the message
         * MSG_OK: the received message is .last_message
         * START_MSG: a new message has just begun (header
           received)
         * IN_MSG: a message is in progress, so keep feeding bytes

        Bytes are binary strings one character long. I.e. 'a'
        means 0x61, '\x8B' means -0x8B.
        Messages - the one passed to wrap() and the one saved
        in .last_message, are strings.
    """

    def __init__(self,
                 header='\x81',
                 footer='\x83',
                 dle='\x90',
                 after_dle_func=lambda x: x,
                 keep_header=False,
                 keep_footer=False):
        """ header:
                The byte value that starts a message
            footer:
                The byte value that ends a message
            dle:
                DLE value (the DLE is prepended to any header,
                footer and DLE in the stream)
            after_dle_func:
                Sometimes the value after DLE undergoes some
                transormation. Provide the function that does
                so here (i.e. XOR with some known value)
            keep_header/keep_footer:
                Keep the header/footer as part of the returned
                message.
        """
        self.header = header
        self.footer = footer
        self.dle = dle
        self.after_dle_func = after_dle_func
        self.keep_header = keep_header
        self.keep_footer = keep_footer

        self.message_format = Struct(
            "header" / Const(b'\x55'),
            "reserved" / Array(4, Byte),
            "data_type" / data_type,
            "data_length" / Int32ub,
            "data" / Array(this.data_length, Byte),
        )

        self.state = self.AWAITING_HEADER
        self.last_message = ''
        self.message_buf = ''
        self.last_error = ''

    def wrap(self, message):
        """ Wrap a message with header, footer and DLE according
            to the settings provided in the constructor.
        """
        wrapped = self.header
        for b in message:
            if b in (self.header, self.footer, self.dle):
                wrapped += (self.dle + self.after_dle_func(b))
            else:
                wrapped += b
        wrapped += self.footer
        return wrapped

    # internal state
    (AWAITING_HEADER, RECEIVING_RESERVED_FIELD, RECEIVING_DATA_TYPE_FIELD,
     RECEIVING_DATA_LEN_FIELD, RECEIVING_DATA_FIELD, AFTER_DLE) = range(6)

    n_received_reserved_field = 0

    def input(self, incoming_byte):
        """ Call this method whenever a new byte is received. It
            returns a ProtocolStatus (see documentation of class
            for info).
        """
        last_state = self.AWAITING_HEADER

        if self.state == self.AWAITING_HEADER:
            if incoming_byte == self.header:
                if self.keep_header:
                    self.message_buf += incoming_byte
                self.state = self.RECEIVING_RESERVED_FIELD
                return ProtocolStatus.START_MSG
            else:
                self.last_error = 'Expected header (0x%02X), got 0x%02X' % (
                    ord(self.header), ord(incoming_byte))
                return ProtocolStatus.ERROR
        elif self.state == self.RECEIVING_RESERVED_FIELD:
            if incoming_byte == self.dle:
                # if it's the firs byte from reserved field, can't have escape value
                if(len(self.message_buf) == 1):
                    self.last_error = "Unexpected escape character (0x%02X) received" & (ord(self.dle))
                    return ProtocolStatus.ERROR
                else:
                    self.state = self.AFTER_DLE
                return ProtocolStatus.IN_MSG
            else:  # just a regular message byte
                idx_data_len = list(map(lambda msg_field: msg_field.name, message_format.subcons)).index('data')
                fixed_size_data_len = sum(map(lambda x: x.sizeof(data_length=0), message_format.subcons))
                self.message_buf += incoming_byte
                if len(self.message_buf) < fixed_size_data_len :#+ 
                    return ProtocolStatus.IN_MSG
        elif self.state == self.AFTER_DLE:
            self.message_buf += self.after_dle_func(incoming_byte)
            self.state = ProtocolStatus.IN_MSG

            return ProtocolStatus.IN_MSG
        else:
            raise AssertionError()

    def _finish_msg(self):
        self.state = self.AWAITING_HEADER
        self.last_message = self.message_buf
        self.message_buf = ''
        return ProtocolStatus.MSG_OK


if __name__ == '__main__':
    pass
