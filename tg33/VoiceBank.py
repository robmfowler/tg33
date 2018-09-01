import mido
from .SysexByte import SysexByte

VOICE_BANK_BULK_COMMAND = "LM  0012VC"
_last_voice_start = 9999999

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
        print('')
        print("transmit complete!")

    def parse_expected_byte(self, sysex, expected_value):
        i, b = next(sysex)
        if b != expected_value:
            raise ValueError(F"Byte {i} is not {format(expected_value, 'x')}")
        return b

    def parse_byte(self, sysex, first_byte_of_voice = False):
        global _last_voice_start
        i, b = next(sysex)
        if first_byte_of_voice:
            _last_voice_start = i
            print('')
        if 0x0C <= (i - _last_voice_start) <= 0x13:
             print(str(chr(b)), end='')
        return b

    def calculate_voice_size(self, msb, lsb):
        return (msb << 7) + lsb
 
    def parse_voice_size(self, sysex, save):
        msb = self.parse_byte(sysex)
        save.append(msb)
        if (msb == 0xF7):
            return 0xF7 #end of sysex
        lsb = self.parse_byte(sysex)
        save.append(lsb)
        voice_size = self.calculate_voice_size(msb, lsb)
        return voice_size

    def extract_first_voice(self, sysex, save):
        voice_size = self.parse_voice_size(sysex, save)
        extracted_command = ''
        data_sum = 0
        for _ in range (10):
            b = self.parse_byte(sysex)
            extracted_command += str(chr(b))
            save.append(b)
            data_sum += b
            data_sum &= 0b01111111
        if extracted_command != VOICE_BANK_BULK_COMMAND:
            raise ValueError(F"extracted command not '{VOICE_BANK_BULK_COMMAND}''")
        self.extract_voice(sysex, voice_size - 10, data_sum, save)

    def extract_voice(self, sysex, voice_size, data_sum_so_far, save):
        data_sum = data_sum_so_far
        first_byte_of_voice = True
        for _ in range (voice_size):
            b = self.parse_byte(sysex, first_byte_of_voice)
            save.append(b)
            data_sum += b
            data_sum &= 0b01111111
            first_byte_of_voice = False
        checksum = self.parse_byte(sysex)
        save.append(checksum)
        result = (data_sum + checksum) % 128
        if (result != 0):
            raise ValueError("Checksum failed!")

    def extract_beginning(self, sysex, save):
        save.append(self.parse_expected_byte(sysex, SysexByte.START))
        save.append(self.parse_expected_byte(sysex, SysexByte.YAMAHA))
        save.append(self.parse_expected_byte(sysex, SysexByte.DEVICE))
        save.append(self.parse_expected_byte(sysex, SysexByte.MODEL))
        
