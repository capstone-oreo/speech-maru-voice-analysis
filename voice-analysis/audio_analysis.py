import librosa 
import matplotlib.pyplot as plt 
import librosa.display
import numpy as np
import soundfile as sf
import numpy as np 

class audio_preprocessor:
    def __init__(self, file):
        # y : audio time series 
        # sr : sampling rate of 'y'
        self.y,self.sr=librosa.load(file, sr=None)
        self.audio_file=file

    def concat_audio(self,y, sr):
        self.y=np.concatenate((self.y, y),axis=0)

    def trim_silence(self):
        # yt : trimmed signal
        # index : the interval of 'y' corresponding to the non-silent region
        self.yt,self.index=librosa.effects.trim(self.y)

    def get_info(self):
        return self.y, self.sr
    
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
        audio_time=librosa.get_duration(y=self.y, sr=self.sr) # len(y)/sr
        return audio_time
    
    def get_speech_intervals(self,top_db=40):
        speech_intervals=librosa.effects.split(self.y, top_db=top_db)
        return speech_intervals
 
    def get_silence_intervals(self,top_db=40):
        # silence_intervals=get_speech_intervals()
        # speech_intervals=self.get_speech_intervals(top_db=top_db)
        speech_intervals=librosa.effects.split(self.y, top_db=top_db)
        silence_intervals=[]
        prev_end=0
        for interval in speech_intervals:
            start, end=interval
            if start>prev_end :
                silence_intervals.append((prev_end,start))
            prev_end=end
        #마지막 음성 구간 추가
        if prev_end<len(self.y):
            silence_intervals.append((prev_end,len(self.y)))
        return silence_intervals

    def get_tempos(self):
        # dynamic tempo
        # librosa.beat.tempo was moved to 'librosa.feature.rhythm.tempo' in librosa version 0.10.0
        onset_env=librosa.onset.onset_strength(y=self.y,sr=self.sr)
        self.tempo_array=librosa.feature.tempo(onset_envelope=onset_env, sr=self.sr, aggregate=None)
        return self.tempo_array
    
    def get_decibels(self):
        self.decibel_array=librosa.amplitude_to_db(self.y)
        return self.decibel_array
    
    # 주어진 기준보다 오래 지속된 공백들로 split한 뒤 배열값으로 추출하기 
    # 음성 구간 사이사이에 (침묵) 구간을 추가하기 위한 기능 
    def split_audio_by_silence(self, output_file, top_db=10, min_silence_duration=3):

        #speech 구간 탐지
        intervals=librosa.effects.split(self.y, top_db=top_db)
        intervals_in_seconds=librosa.samples_to_time(intervals,sr=self.sr)
        # 1. 3초 이상인 silence 구간 
        # 2. silence 구간 제외 speech 구간 저장 

        # silence 인 구간만 추출하기 
        # ---- 시각화 예시 
        silence_intervals=intervals[np.where(np.diff(intervals)>=self.sr*min_silence_duration)[0]]
        silence_in_seconds=librosa.samples_to_time(silence_intervals, sr=self.sr)
        plt.figure()
        librosa.display.waveshow(self.y,sr=self.sr, alpha=0.5)
        for start,end in intervals_in_seconds:
            plt.vlines(start,-0.1,0.1, colors='red')
            plt.vlines(end,-0.1,0.1, colors='blue')
        plt.xlabel("Time(s)")
        plt.ylabel("Amplitude")
        plt.title("Waveform")
        plt.show()

        #----
        #filtered_intervals=[]
        #prev_end=0
        #prev_start=0
        #for interval in intervals:
                #start, end=interval
                # 현재 구간과 이전 구간 사이의 침묵 기간 계산 
                #silence_duration=(start-prev_end)/self.sr 

                #if prev_start!=0:
                    # 침묵구간 판단하기 
                    # 3초 넘어갔을 때 
                    #if silence_duration>=min_silence_duration:
                        #filtered_intervals.append(interval) 
                    #else :
                        #filtered_intervals.append((start, prev_end))
                #prev_end=end
                #prev_start=start 

        
        # split한 파일 저장 
        #for i, interval in enumerate(intervals):
        #    start_time, end_time=interval
        #    out_file=f"{output_file}_{i}.wav"
        #    sf.write(out_file, self.y[start_time:end_time], self.sr)
            # librosa doesn't support output anymore
            # librosa.output.write_wav(output_file, self.y[start_time:end_time],self.sr)



# 1. file path 선언 (filename=librosa.ex('brahms'))
# 2. audio_analyzer 객체 만들기 (audio=audio_analyzer(filename))
# 3. 원하는 함수 적용 (tmp=audio.get_tempos())

filename='voice-analysis\cnt.wav'
audio=audio_analyzer(filename)
#tmp=audio.get_speech_intervals()
#print(audio.get_silence_intervals())
#audio.trim_silence()
#speech_intervals=audio.get_speech_intervals()
#print(speech_intervals)

#print(len(audio.y),audio.sr)
audio.amplitude_visualize()

#audio.amplitud)e_visualize()
#audio.split_audio_by_silence('ex-sebasi')
#tmp=audio.get_silence_intervals()
#print(tmp)