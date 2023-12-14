from typing import List, Tuple

from pydantic import BaseModel

import requests

from requests.exceptions import HTTPError, ConnectionError, Timeout, TooManyRedirects

session = requests.Session()

session.headers.update({
    'Accepts': 'application/json',
    'Content-Type': 'application/json',
})

PUSHER_HOST = "https://pusher.vecinos.com.ar"
# PUSHER_HOST = "http://127.0.0.1:9035"

PUSH_ENDPOINT = f"{PUSHER_HOST}/api/v1/pusher/push"


class PushBatchForm(BaseModel):
    contacts: List[tuple[str, dict]]
    title_template: str
    message_template: str
    pass


class PushForm(BaseModel):
    token: str
    title: str
    message: str
    data: dict



class PusherClient:

    def push(self, pushForm: PushForm):
        """
        :param pushForm:
        :return:
        """
        try:
            print("PusherClient.push | ", pushForm)
            response = session.post(PUSH_ENDPOINT, json={
                "token": pushForm.token,
                "title": pushForm.title,
                "message": pushForm.message,
                "data":  pushForm.data
            })
            if response.status_code == 200:
                return response.json()
            else:
                print("PusherClient.push | response.status_code != 200", response.status_code)
                return None
        except (HTTPError, ConnectionError, Timeout, TooManyRedirects) as e:
            print("PusherClient.push | error ", e)
            return None
        pass

    def push_batch(self, pushForm: PushBatchForm):
        """
        make a titles from a template a dict of params
        :param pushForm:
        :return:
        """
        notifications: List[Tuple[str, str, str]] = []

        for token, params in pushForm.contacts:
            print("PusherClient.push_batch | ", token, params)
            title = pushForm.title_template.format(**params)
            message = pushForm.message_template.format(**params)
            notifications.append((token, title, message))

        for token, title, message in notifications:
            self.push(PushForm(token=token, title=title, message=message))

        pass


pusher_client = PusherClient()
