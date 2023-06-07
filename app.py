from flask import Flask, request, make_response
from flask_restx import Resource, Api

from stt_response import SttResponse
from voice_analysis import audio_analysis
from text_analysis import texts_analysis
import os
import uuid
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
        try:
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
            audio_tempos = audio.get_tempos()
            audio_decibels = audio.get_decibels()
            splitted_audios = audio.split_audio_by_silence(filename, save_file=True)

            # vito get 요청 id를 받음
            ids = []
            for i, audio in enumerate(splitted_audios):
                out_file = f"./temp_audio/{filename}_{i}.wav"
                transcribe_id = self.stt.get_transcribe_id(open(out_file, 'rb'))
                ids.append(transcribe_id)
                os.remove(out_file)

            """
            for i, audio in enumerate(splitted_audios): 
                out_file=f"/temp_audio/{filename}_{i}.wav"
                os.remove(out_file)
            """
            os.remove(filepath)

            texts = self.stt.get_transcribe_msg_by_id_list(ids)
            if not texts:
                raise RuntimeError("말이 인식되지 않았습니다. 음성을 녹음하신 후 다시 시도하세요")
            text = texts_analysis.text_analyzer(texts)
            try:
                response = SttResponse(texts, audio_tempos, audio_decibels, text.keyword_extract(),
                                       text.longsent_extract(), text.frequentword_extract())
            except Exception:
                raise RuntimeError("문장의 길이가 짧아 분석할 수 없습니다.")
            return response.__dict__
        except Exception as e:
            error_message = str(e)
            response = make_response(error_message)
            response.status_code = 500
            return response


if __name__ == '__main__':
    app.run()
