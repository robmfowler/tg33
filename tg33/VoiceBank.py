import mido
from .SysexByte import SysexByte

VOICE_BANK_BULK_COMMAND = "LM  0012VC"

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
        save = bytearray()
        self.extract_beginning(sysex, save)
        self.extract_first_voice(sysex, save)
        for _ in range(63):
            voice_size = self.parse_voice_size(sysex, save)
            if voice_size == 0xF7:
                break
            self.extract_voice(sysex, voice_size, 0, save)
        if (next(sysex, 0xF7) != 0xF7):
            raise ValueError("Sysex didn't end as expected")
        print("transmit complete!")

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
        return (msb << 7) + lsb
 
    #def parse_voice_data(self, sysex, size):

    #def parse_bulk_type(self, sysex):

    #def parse_voice_checksum(self, sysex):

    def parse_voice_size(self, sysex, save):
        msb = self.parse_byte(sysex)
        save.append(msb)
        if (msb == 0xF7):
            return 0xF7 #end of sysex
        lsb = self.parse_byte(sysex)
        save.append(lsb)
        voice_size = self.calculate_voice_size(msb, lsb)
        print(F"voice size (byte count) {format(voice_size, 'd')}")
        return voice_size

    def extract_first_voice(self, sysex, save):
        voice_size = self.parse_voice_size(sysex, save)
        extracted_command = ''
        data_sum = 0
        for _ in range (10):
            b = next(sysex)[1]
            extracted_command += str(chr(b))
            save.append(b)
            data_sum += b
            data_sum &= 0b01111111
        print(F"bulk command: {extracted_command}")
        if extracted_command != VOICE_BANK_BULK_COMMAND:
            raise ValueError(F"extracted command not '{VOICE_BANK_BULK_COMMAND}''")
        self.extract_voice(sysex, voice_size - 10, data_sum, save)

    def extract_voice(self, sysex, voice_size, data_sum_so_far, save):
        data_sum = data_sum_so_far
        for _ in range (voice_size):
            b = next(sysex)[1]
            save.append(b)
            data_sum += b
            data_sum &= 0b01111111
        print(F"data_sum {format(data_sum, '08b')}")
        checksum = next(sysex)[1]
        save.append(checksum)
        print(F"checksum {format(checksum, '08b')}")
        result = (data_sum + checksum) % 128
        if (result != 0):
            print(F"checksum failed; their sum {format(result, '08b')}")
            raise ValueError("Checksum failed!")

    def extract_beginning(self, sysex, save):
        save.append(self.parse_expected_byte(sysex, SysexByte.START))
        save.append(self.parse_expected_byte(sysex, SysexByte.YAMAHA))
        save.append(self.parse_expected_byte(sysex, SysexByte.DEVICE))
        save.append(self.parse_expected_byte(sysex, SysexByte.MODEL))
        
