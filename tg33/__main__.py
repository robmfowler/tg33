import sys
import mido
from .VoiceBank import VoiceBank

def main():
    args = sys.argv[1:]
    if len(args) != 1:
        raise ValueError("tg33 takes one argument, a TG33 voice bank")
    voice_bank = VoiceBank(args[0])
    for port_name in mido.get_output_names():
        print(port_name)
    #voice_bank.transmit()

if __name__ == '__main__':
    main()