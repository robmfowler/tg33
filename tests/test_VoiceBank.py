from tg33.VoiceBank import VoiceBank

def test_str():
    voiceBank = VoiceBank("/srv/tg33/tests/data/tg33_initial_backup.syx")
    print(str(voiceBank))
    assert True