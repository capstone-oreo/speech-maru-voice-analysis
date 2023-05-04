from flask import Flask, request
from flask_restx import Resource, Api

import speech_to_text

app = Flask(__name__)
api = Api(app)


# 배포 확인용
@api.route('/test')
class Test(Resource):
    def get(self):
        return 'flask'


# 업로드한 파일을 바로 다운로드한다.
@api.route('/stt')
class SttRouter(Resource):
    stt = speech_to_text.Stt()

    def post(self):
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        transcribe_id = self.stt.get_transcribe_id(file)
        return self.stt.get_transcribe_msg_by_id_list([transcribe_id])


if __name__ == '__main__':
    app.run()
