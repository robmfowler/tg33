import mido
from .SysexByte import SysexByte

class VoiceBank:
    def __init__(self, sysex_file):
        messages = mido.read_syx_file(sysex_file)
        message_count = len(messages)
        if message_count != 1:
            raise ValueError(F"tg33 expects one voicebank (found {message_count}).")
        self.message = messages[0]

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return "\n".join([hexstr for hexstr in self.message.hex().split(' ')])

    def transmit(self):
        sysex = enumerate(self.message.bytes())
        self.extract_beginning(sysex)
        self.extract_first_voice(sysex)

    def parse_expected_byte(self, sysex, expected_value):
        i, b = next(sysex)
        if b != expected_value:
            raise ValueError(F"Byte {i} is not {format(expected_value, 'x')}")
        print(format(b, 'x'))
        return b

    def parse_byte(self, sysex):
        i, b = next(sysex)
        print(format(b, 'x'))
        return b

    def parse_voice_size(self, sysex):
        save = bytearray()
        msb_size = self.parse_byte(sysex)
        print(F"msb_size {format(msb_size, 'd')}")
        save.append(msb_size)
        lsb_size =  self.parse_byte(sysex)
        print(F"lsb_size {format(lsb_size, 'd')}")
        save.append(lsb_size)

    #def parse_voice_data(self, sysex, size):

    #def parse_bulk_type(self, sysex):

    #def parse_voice_checksum(self, sysex):

    def extract_first_voice(self, sysex):
        self.parse_voice_size(sysex)

    #def extract_voice(self, sysex):

    def extract_beginning(self, sysex):
        save = bytearray()
        save.append(self.parse_expected_byte(sysex, SysexByte.START))
        save.append(self.parse_expected_byte(sysex, SysexByte.YAMAHA))
        save.append(self.parse_expected_byte(sysex, SysexByte.DEVICE))
        save.append(self.parse_expected_byte(sysex, SysexByte.BULK))
        
