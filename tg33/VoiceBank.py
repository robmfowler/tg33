import mido

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