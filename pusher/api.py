import requests
from requests.exceptions import HTTPError, ConnectionError

_session = requests.Session()

_session.headers.update(
    {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate",
        "content-type": "application/json",
    }
)


def send(token, title, message=None, extra=None):
    try:
        response = _session.post(
            "https://pusher.vecinos.com.ar/api/v1/pusher/push",
            json={
                "token": token,  # to
                "title": title,
                "message": message
            }
        )
        if response.status_code == 200:
            print("success", response.json())
        else:
            print("error", response.status_code, response.json())

    except HTTPError as exc:
        print("http error", exc)
    except ConnectionError as exc:
        print("connection error", exc)

    pass
