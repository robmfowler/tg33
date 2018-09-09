#built in library imports
import os
#pipenv installed imports
from tg33.VoiceBank import VoiceBank

def test_syx_file_has_one_message():
    dirpath = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(dirpath, 'data', 'tg33_initial_backup.syx')
    voiceBank = VoiceBank(filepath)
