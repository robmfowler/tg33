from time import sleep
import rtmidi
import readchar
from .SysexByte import SysexByte

VOICE_BANK_BULK_COMMAND = "LM  0012VC"
_last_voice_start = 9999999

class VoiceBank:
    def __init__(self, sysex_file):
        with open(sysex_file, "rb") as message:
            self.message = bytearray(message.read())

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return "\n".join([hexstr for hexstr in self.message.hex().split(' ')])

    def transmit(self):
        sysex = enumerate(self.message)
        voices = []
        voices.append(self.extract_first_voice(sysex))
        for _ in range(63):
            save = bytearray()
            voice_size = self.parse_voice_size(sysex, save)
            if voice_size == SysexByte.END:
                break
            save.extend(self.extract_voice(sysex, voice_size, 0))
            voices.append(save)
        if (next(sysex, SysexByte.END) != SysexByte.END):
            raise ValueError("Sysex didn't end as expected")
        print('')
        midiout = rtmidi.MidiOut()
        ports = midiout.get_ports()
        for index, port in enumerate(ports):
            print(F"—> {index}: {port}")
        print("The available ports are numbered above.")
        print("Type the number of the port to which the voice bank should be transmitted: ", end='')
        print("")
        c = readchar.readchar()
        print(c)
        midiout.open_port(int(c))
        for index, voice in enumerate(voices):
            print(F"Sending voice {index + 1}")
            self.transmit_bytes(midiout, voice)
            sleep(0.1)
        midiout.send_message([SysexByte.END])
        del midiout
        print("transmit complete!")

    def transmit_bytes(self, midiout, voice):
        for b in iter(voice):
            midiout.send_message([b])
            sleep(0.00033)

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
        if (msb == SysexByte.END):
            return SysexByte.END #end of sysex
        lsb = self.parse_byte(sysex)
        save.append(lsb)
        voice_size = self.calculate_voice_size(msb, lsb)
        return voice_size

    def extract_first_voice(self, sysex):
        voice_bytes = bytearray()
        voice_bytes.extend(self.extract_beginning(sysex)) 
        voice_size = self.parse_voice_size(sysex, voice_bytes)
        extracted_command = ''
        data_sum = 0
        for _ in range (10):
            b = self.parse_byte(sysex)
            extracted_command += str(chr(b))
            voice_bytes.append(b)
            data_sum += b
            data_sum &= 0b01111111
        if extracted_command != VOICE_BANK_BULK_COMMAND:
            raise ValueError(F"extracted command not '{VOICE_BANK_BULK_COMMAND}''")
        voice_bytes.extend(self.extract_voice(sysex, voice_size - 10, data_sum))
        return voice_bytes

    def extract_voice(self, sysex, voice_size, data_sum_so_far):
        voice_bytes = bytearray()
        data_sum = data_sum_so_far
        first_byte_of_voice = True
        for _ in range (voice_size):
            b = self.parse_byte(sysex, first_byte_of_voice)
            voice_bytes.append(b)
            data_sum += b
            data_sum &= 0b01111111
            first_byte_of_voice = False
        checksum = self.parse_byte(sysex)
        voice_bytes.append(checksum)
        result = (data_sum + checksum) % 128
        if (result != 0):
            raise ValueError("Checksum failed!")
        return voice_bytes

    def extract_beginning(self, sysex):
        voice_bytes = bytearray()
        voice_bytes.append(self.parse_expected_byte(sysex, SysexByte.START))
        voice_bytes.append(self.parse_expected_byte(sysex, SysexByte.YAMAHA))
        voice_bytes.append(self.parse_expected_byte(sysex, SysexByte.DEVICE))
        voice_bytes.append(self.parse_expected_byte(sysex, SysexByte.MODEL))
        return voice_bytes
        
