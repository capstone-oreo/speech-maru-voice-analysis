import librosa 
import matplotlib.pyplot as plt 
import librosa.display
import numpy as np

class audio_preprocessor:
    def __init__(self, file):
        # y : audio time series 
        # sr : sampling rate of 'y'
        # load : (해당 오디오파일의 길이를 sr기준으로 나눈 것) y : 각 point에서의 진폭 
        self.y,self.sr=librosa.load(file, sr=None)
        self.audio_file=file
        # self.yt,self.index=self.trim_silence()

    def concat_audio(self,y, sr):
        self.y=np.concatenate((self.y, y),axis=0)


    def trim_silence(self):
        # yt : trimmed signal
        # index : the interval of 'y' corresponding to the non-silent region
        self.yt,self.index=librosa.effects.trim(self.y)


    def get_info(self):
        print(self.y, self.sr)
    
    def amplitude_visualize(self):
        plt.figure()
        librosa.display.waveshow(self.y,sr=self.sr, alpha=0.5)
        plt.xlabel("Time(s)")
        plt.ylabel("Amplitude")
        plt.title("Waveform")
        plt.show()



class audio_analyzer(audio_preprocessor):
    # 오디오 데이터 길이 계산 (sec)
    def get_duration(self):
        audio_time=librosa.get_duration(y=self.y, sr=self.sr)
        return audio_time
    def get_speech_intervals(self):
        top_db=1
        speech_intervals=librosa.effects.split(self.y, top_db=top_db)
        return speech_intervals
    def get_silence_intervals(self):
        # silence_intervals=get_speech_intervals()
        silence_intervals=self.get_speech_intervals()
    def get_tempos(self):
        # dynamic tempo
        # librosa.beat.tempo was moved to 'librosa.feature.rhythm.tempo' in librosa version 0.10.0
        onset_env=librosa.onset.onset_strength(y=self.y,sr=self.sr)
        self.tempo_array=librosa.feature.tempo(onset_envelope=onset_env, sr=self.sr, aggregate=None)
        return self.tempo_array
    def get_decibels(self):
        self.decibel_array=librosa.amplitude_to_db(self.y)
        return self.decibel_array


# 1. file path 선언 (filename=librosa.ex('brahms'))
# 2. audio_analyzer 객체 만들기 (audio=audio_analyzer(filename))
# 3. 원하는 함수 적용 (tmp=audio.get_tempos())

#filename=librosa.ex('brahms')
filename='voice-analysis\sebasi.mp3'
audio=audio_analyzer(filename)
#tmp=audio.get_speech_intervals()

#print(len(audio.y))
#audio.amplitud)e_visualize()
