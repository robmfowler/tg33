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

    def parse_expected_byte(self, sysex, expected_value, format_code='x'):
        i, b = next(sysex)
        if b != expected_value:
            raise ValueError(F"Byte {i} is not {format(expected_value, 'x')}")
        print(format(b, format_code))
        return b

    def parse_byte(self, sysex, format_code='x'):
        b = next(sysex)[1]
        print(format(b, format_code))
        return b

    def calculate_voice_size(self, msb, lsb):
        return lsb + (msb << 7)
 
    #def parse_voice_data(self, sysex, size):

    #def parse_bulk_type(self, sysex):

    #def parse_voice_checksum(self, sysex):

    def extract_first_voice(self, sysex):
        save = bytearray()
        msb = self.parse_byte(sysex, '08b')
        save.append(msb)
        lsb = self.parse_byte(sysex, '08b')
        save.append(lsb)
        voice_size = self.calculate_voice_size(msb, lsb)
        print(F"voice size (byte count) {format(voice_size, 'd')}")       

    #def extract_voice(self, sysex):

    def extract_beginning(self, sysex):
        save = bytearray()
        save.append(self.parse_expected_byte(sysex, SysexByte.START))
        save.append(self.parse_expected_byte(sysex, SysexByte.YAMAHA))
        save.append(self.parse_expected_byte(sysex, SysexByte.DEVICE))
        save.append(self.parse_expected_byte(sysex, SysexByte.MODEL))
        
