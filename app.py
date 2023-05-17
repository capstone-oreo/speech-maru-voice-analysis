from flask import Flask, request
from flask_restx import Resource, Api
from voice_analysis import audio_analysis

import speech_to_text

app = Flask(__name__)
api = Api(app)


# 배포 확인용
@api.route('/test')
class Test(Resource):
    def get(self):
        return 'flask'


# 음성을 글로 변환한다.
@api.route('/stt')
class SttRouter(Resource):
    stt = speech_to_text.Stt()

    def post(self):
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        # 나누기
        audio=audio_analysis.audio_analyzer(file)
        output_file=f"{file}"
        splitted_audios=audio.split_audio_by_silence(output_file=output_file)
        # vito get 요청 id를 받음
        ids=[]
        for audio in splitted_audios:
            transcribe_id = self.stt.get_transcribe_id(file)
            ids.append(transcribe_id)
        # 배열로 get_transcribe_msg_by_id_list 전달
        # stt.get_transcribe_id(file)만 for문 돌리기 (sentence append는 이미 get_transcribe_msg_by_id_list)
  
        #return self.stt.get_transcribe_msg_by_id_list([transcribe_id])
        return self.stt.get_transcribe_msg_by_id_list(ids)


if __name__ == '__main__':
    app.run()
