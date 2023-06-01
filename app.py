from flask import Flask, request
from flask_restx import Resource, Api

from stt_response import SttResponse
from voice_analysis import audio_analysis
import os
import uuid

import speech_to_text
import stt_response

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

    sttResponse=stt_response.SttResponse()

    def post(self):
        if 'file' not in request.files:
            raise RuntimeError('No file part')
        file = request.files['file']
        if file.filename == '':
            raise RuntimeError('No selected file')

        filename = str(uuid.uuid4())
        directory = './temp_audio/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        filepath = os.path.join(directory, filename)
        file.save(filepath)

        # librosa 이용해서 파일 자르기
        audio = audio_analysis.audio_analyzer(filepath)
        splitted_audios = audio.split_audio_by_silence(filename, save_file=True)

        # vito get 요청 id를 받음
        ids = []
        for i, audio in enumerate(splitted_audios):
            out_file = f"./temp_audio/{filename}_{i}.wav"
            transcribe_id = self.stt.get_transcribe_id(open(out_file, 'rb'))
            self.sttResponse.text.append(transcribe_id)
            #ids.append(transcribe_id)
            os.remove(out_file)

        """
        for i, audio in enumerate(splitted_audios): 
            out_file=f"/temp_audio/{filename}_{i}.wav"
            os.remove(out_file)
        """
        os.remove(filepath)
        response = SttResponse(self.stt.get_transcribe_msg_by_id_list(ids))
        return response.__dict__


if __name__ == '__main__':
    app.run()
