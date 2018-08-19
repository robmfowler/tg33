import mido

class VoiceBank:
    def __init__(self, sysex_file):
        self.messages = mido.read_syx_file(sysex_file)
        assert (len(self.messages) == 2), "This program expects one voicebank."

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return "\n".join([str(message) for message in self.messages])