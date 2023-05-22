import json
import os
import time
import redis
import requests
from dotenv import load_dotenv
import logging 


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger()


load_dotenv()


class Stt:
    def __init__(self):
        self.client_id = os.getenv("VITO_CLIENT_ID")
        self.client_secret = os.getenv("VITO_CLIENT_SECRET")
        self.redis_client = redis.Redis(host=os.getenv("REDIS_HOST"), port=6379, db=0)

    # 파일을 Vito API에 전송하고 id를 받는다.
    def get_transcribe_id(self, voice_file):
        access_token = self.__get_access_token()
        headers = {'Authorization': 'bearer ' + access_token}
        data = {'config': json.dumps({'use_itn': True})}
        file = {'file': voice_file}
        response = requests.post('https://openapi.vito.ai/v1/transcribe', headers=headers, data=data, files=file)
        if response.status_code != 200:
            raise RuntimeError(f"변환에 실패했습니다: {response.text}")
        return response.json()['id']

    # id list를 통해 변환된 글을 순서대로 list로 받는다.
    def get_transcribe_msg_by_id_list(self, transcribe_id_list):
        access_token = self.__get_access_token()
        headers = {'Authorization': 'bearer ' + access_token}
        msg_list = []
        for transcribe_id in transcribe_id_list:
            result = self.__get_transcription_result(transcribe_id, headers)
            # 변환 성공
            if result['status'] == 'completed':
                logger.info(f'id: {transcribe_id}, result:{result}')
                
                if not result['results']['utterances']:
                    continue                
                msg_list.append(result['results']['utterances'][0]['msg'])

            # 변환 실패
            else:
                raise RuntimeError("STT 변환에 실패했습니다.")
        return msg_list

    # redis에서 token을 찾고 없으면 api 요청 후 redis에 저장한다.
    def __get_access_token(self):
        access_token = self.redis_client.get('access_token')
        if access_token is None:
            FIVE_HOUR = 60 * 60 * 5
            data = {'client_id': self.client_id, 'client_secret': self.client_secret}
            response = requests.post('https://openapi.vito.ai/v1/authenticate', data)
            if response.status_code != 200:
                raise RuntimeError(f"인증에 실패했습니다: {response.text}")
            access_token = response.json()['access_token']
            self.redis_client.set('access_token', access_token)
            self.redis_client.expire('access_token', FIVE_HOUR)
        else:
            access_token = access_token.decode()
        return access_token

    def __get_transcription_result(self, transcribe_id, headers):
        result = requests.get('https://openapi.vito.ai/v1/transcribe/' + transcribe_id, headers=headers).json()
        while result['status'] == 'transcribing':
            time.sleep(0.2)
            result = requests.get('https://openapi.vito.ai/v1/transcribe/' + transcribe_id, headers=headers).json()
        return result
