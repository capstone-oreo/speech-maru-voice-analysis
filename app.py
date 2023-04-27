from flask import Flask, request, send_file
from flask_restx import Resource, Api
import tempfile

app = Flask(__name__)
api = Api(app)


# 배포 확인용
@api.route('/test')
class Test(Resource):
    def get(self):
        return 'flask'


# 업로드한 파일을 바로 다운로드한다.
@api.route('/upload')
class Upload(Resource):
    def post(self):
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            file.save(tmp_file.name)
            return send_file(tmp_file.name, attachment_filename=file.filename, as_attachment=True,
                             mimetype=file.content_type)


if __name__ == '__main__':
    app.run()
