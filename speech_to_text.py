import os
import redis
import requests
from dotenv import load_dotenv

load_dotenv()


class STT:
    def __init__(self):
        self.access_token = None
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.redis_client = redis.Redis(host='redis', port=6379, db=0)

    def get_access_token(self):
        self.access_token = self.redis_client.get('access_token')
        if self.access_token is None:
            FIVE_HOUR = 60 * 60 * 5
            data = {'client_id': self.client_id, 'client_secret': self.client_secret}
            response = requests.post('https://openapi.vito.ai/v1/authenticate', json=data)
            self.access_token = response.json()['access_token']
            self.redis_client.set('access_token', self.access_token)
            self.redis_client.expire('access_token', FIVE_HOUR)
