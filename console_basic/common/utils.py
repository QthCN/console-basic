import json

from oslo_config import cfg
import requests

from console_basic import exception


CONF = cfg.CONF


class HTTPClient(object):

    def __init__(self):
        pass

    def _send_request(self, url, headers=None, data=None, method="GET"):
        response = None
        if data:
            data = json.dumps(data)
        if method.upper() == "GET":
            response = requests.get(url=url, headers=headers,
                                    data=data)
        elif method.upper() == "POST":
            response = requests.post(url=url, data=data, headers=headers)
        elif method.upper() == "DELETE":
            response = requests.delete(url=url, data=data, headers=headers)
        elif method.upper() == "PUT":
            response = requests.put(url=url, data=data, headers=headers)

        return response

    def get_v1_token(self, username, password):
        url = "{s}/v1/tokens".format(s=CONF.service.endpoint)
        payload = dict(auth=dict(username=username,
                                 password=password))
        headers = {"Content-Type": "application/json"}
        response = self._send_request(url=url, headers=headers,
                                      data=payload, method="POST")
        content = json.loads(response.content)
        return content.get("token", None)

    def send_request(self, url, headers=None, data=None, method="GET",
                     token_provided=False, admin_token=True,
                     username=None, password=None):
        if headers is None:
            headers = {}
        # 'token_provided' True means there is a token in headers already
        if token_provided is False:
            if admin_token:
                token = self.get_v1_token(username=username,
                                          password=password)
            else:
                token = self.get_v1_token(username=username,
                                          password=password)
            headers["X-Auth-Token"] = token
        headers["Content-Type"] = "application/json"
        response = self._send_request(url=url, headers=headers, data=data,
                                      method=method)
        return response

    def send_request_with_check(self, url, headers=None, data=None,
                                method="GET", token_provided=False,
                                admin_token=True):
        response = self.send_request(url=url, headers=headers, data=data,
                                     method=method,
                                     token_provided=token_provided,
                                     admin_token=admin_token)
        if response.status_code not in (200, 204):
            raise exception.HTTPCodeError(code=response.status_code)

        content = response.content
        try:
            c = json.loads(content)
            if "error" in c:
                raise exception.HTTPContentError(error=c["error"])
        except:
            # response has no content, so code check is enough
            pass

        return response

