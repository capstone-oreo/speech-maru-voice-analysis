import librosa 
import matplotlib.pyplot as plt 
import numpy as np
import soundfile as sf

class audio_preprocessor:
    def __init__(self, file):
        # y : audio time series 
        # sr : sampling rate of 'y'
        #self.y,self.sr=sf.read(file)
        self.y,self.sr=librosa.load(file, sr=None)
        self.audio_file=file
        self.duration=librosa.get_duration(y=self.y, sr=self.sr)

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
    
    """
    def trim_audio_data(self, sec=1):
        audio_array=[]
        time_series=1*self.sr 
        total=len(self.y)
        samples_wrote=0
        counter=1

        while samples_wrote<total:
                if time_series>(total-samples_wrote):
                        time_series=total-samples_wrote
                block=self.y[samples_wrote:(samples_wrote+time_series)]
                audio_array.append(block)
    """


class audio_analyzer(audio_preprocessor):
    # 오디오 데이터 길이 계산 (sec)
    def get_duration(self):
        audio_time=librosa.get_duration(y=self.y, sr=self.sr) # len(y)/sr
        return audio_time
    

    def get_speech_intervals(self,top_db=40, by_sec=True):
        speech_intervals=librosa.effects.split(self.y, top_db=top_db)
        if by_sec:
            return speech_intervals/self.sr
        else:
            return speech_intervals
        
 
    def get_silence_intervals(self,top_db=40):
        speech_intervals=librosa.effects.split(self.y, top_db=top_db)
        silence_intervals=[]
        prev_end=0
        for interval in speech_intervals:
            start, end=interval
            if start>prev_end :
                # 오디오 잘리는 것 방지
                silence_intervals.append((prev_end+5,start-5))
            prev_end=end
        #마지막 음성 구간 추가
        if prev_end<len(self.y):
            silence_intervals.append((prev_end+5,len(self.y)))
        return silence_intervals
    
    # return tempo per sec 
    def get_tempos(self, sec=1):
        tempo_array=[]
        audio_cnt=0
        interval_duration=sec
        total_duration=self.duration 
        if total_duration%interval_duration==0:
                audio_cnt=total_duration//interval_duration
        else :
                audio_cnt=total_duration//interval_duration+1 

        for i in range(int(audio_cnt)): 
            tmp=self.y[self.sr*interval_duration*i:self.sr*interval_duration*(i+1)]
            tempo,beats=librosa.beat.beat_track(y=tmp,sr=self.sr)
            tempo_array.append(tempo)
        
        # 시각화
        """
        plt.figure()
        plt.plot(list(range(len(tempo_array))),tempo_array)
        plt.xlabel("Time(s)")
        plt.ylabel("Tempo")
        plt.title("Tempo")
        plt.show()
        """
        
       
        return tempo_array
             
    
    def get_decibels(self):
        frames=librosa.util.frame(self.y, frame_length=2048, hop_length=512)
        decibel_frames=librosa.amplitude_to_db(frames, ref=np.max)
        decibel_per_second=np.mean(decibel_frames,axis=0)
        print(len(decibel_per_second))
        
        # 시각화
        """
        plt.figure()
        plt.plot(list(range(len(decibel_per_second))),decibel_per_second)
        plt.xlabel("Time(s)")
        plt.ylabel("Decibels")
        plt.title("Decibels")
        plt.show()
        """

        return decibel_per_second
    
    
    # 음성 구간 사이사이에 (침묵) 구간을 추가하기 위한 기능 
    def split_audio_by_silence(self, output_file, top_db=40, min_silence_duration=1, save_file=False):
        intervals=librosa.effects.split(self.y, top_db=top_db)
        
        filtered_intervals=[]
        prev_end=0
        for interval in intervals:
                start, end=interval
                # 현재 구간과 이전 구간 사이의 침묵 기간 계산 
                silence_duration=(start-prev_end)/self.sr 
                # 침묵구간 판단하기 
                if silence_duration>=min_silence_duration:
                        filtered_intervals.append([prev_end,end])
                        prev_end=end
        if prev_end < len(self.y):
            filtered_intervals.append([prev_end,len(self.y)])       
        
        # 파일 저장 후 결과 반환
        # split한 파일 저장 
        if save_file==True:
            for i, interval in enumerate(filtered_intervals):
                start_time, end_time=interval
                out_file=f"tmp_{i}.wav"
                sf.write(out_file, self.y[start_time:end_time], self.sr)

         # 시각화
        """
        plt.figure()
        librosa.display.waveshow(self.y,sr=self.sr, alpha=0.5)
        for start,end in librosa.samples_to_time(filtered_intervals,sr=self.sr):
            plt.vlines(start,-0.1,0.1, colors='red')
            plt.vlines(end,-0.1,0.1, colors='blue')
        plt.xlabel("Time(s)")
        plt.ylabel("Amplitude")
        plt.title("Waveform")
        plt.show()
         """
        

        return filtered_intervals
    
        

        

# 1. file path 선언 (filename=librosa.ex('brahms'))
# 2. audio_analyzer 객체 만들기 (audio=audio_analyzer(filename))
# 3. 원하는 함수 적용 (tmp=audio.get_tempos())


filename='voice_analysis\sebasi.mp3'

audio=audio_analyzer(filename)
#audio.amplitude_visualize()
#print(audio.get_decibels())
print(audio.get_tempos())
#audio.split_audio_by_silence('sebasi',save_file=True)
#print('get_speech_intervals : ',audio.get_speech_intervals(),'\n')
#print('get_silence_intervals : ',audio.get_silence_intervals(),'\n')

