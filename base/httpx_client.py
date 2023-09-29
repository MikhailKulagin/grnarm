import logging

import httpx

import exceptions as exceptions

log = logging.getLogger("grnatm")


class AsyncBaseClient:
    def __init__(self, host_cfg):
        self.base_url = host_cfg.url
        self.timeout = host_cfg.get('timeout', 5.0)

    def _post(self, url, body, timeout=None):
        with httpx.Client(verify=False,
                          base_url=self.base_url,
                          timeout=timeout or self.timeout) as client:
            log.info(f"POST {self.base_url}{url}")
            try:
                response = client.post(url,
                                       json=body,
                                       headers={'content-type': 'application/json'},
                                       )
            except httpx.HTTPError as err:
                raise exceptions.HTTPError(str(err))
            log.debug(f"{response.status_code}")
            if response.status_code == 204:
                log.debug("response 204 no content")
                return {}
            elif 200 <= response.status_code < 300:
                return response.json()
            else:
                text = response.text
                log.error(f"{text}")
                raise exceptions.HTTPStatusError(response)
