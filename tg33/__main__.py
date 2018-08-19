import sys
from .VoiceBank import VoiceBank

def main():
    args = sys.argv[1:]
    assert(len(args) == 1), "tg33 takes only one argument, a TG33 voice bank"

if __name__ == '__main__':
    main()