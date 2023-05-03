import librosa 

class audio_preprocessor:
    def __init__(self, file):
        # y : audio time series
        # sr : sampling rate of 'y'
        self.y,self.sr=librosa.load(file, sr=None)
        self.audio_file=file

    def trim_silence(self):
        # yt : trimmed signal
        # index : the interval of 'y' corresponding to the non-silent region
        self.yt,self.index=librosa.effects.trim(self.y)

    def get_info(self):
        print(self.y, self.sr)


filename=librosa.ex('trumpet')
ex='.\audio_data\000216.wav'
audio1=audio_preprocessor(ex)


class audio_analyzer(audio_preprocessor):
    def __init__(self):
        pass 
    def get_speech_intervals(self):
        top_db=50
        intervals=librosa.effects.split(self.y, top_db=top_db)
    def get_silence_intervals(self):
        pass 
    def get_tempos(self):
        self.tempo_array=librosa.beat.tempo(self.y)
    def get_decibels(self):
        pass 
