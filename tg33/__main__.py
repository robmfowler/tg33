import sys
from .VoiceBank import VoiceBank

def main():
    args = sys.argv[1:]
    if len(args) != 1:
        raise ValueError("tg33 takes one argument, a TG33 voice bank")
    voice_bank = VoiceBank(args[0])
    voice_bank.transmit()

if __name__ == '__main__':
    main()