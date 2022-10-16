import json
import time
from urllib import request
from urllib.error import URLError
from EsportsCapsuleFarmer.Container.EnvUtils import is_containerized


def ensure_selenium_grid_readiness():
    def function(func):
        def wrapper(self, *args, **kwargs):
            wait_for_selenium_grid(self)
            return func(self, *args, **kwargs)
        return wrapper
    return function


def wait_for_selenium_grid(self):
    if not is_containerized():
        return
    while True:
        try:
            if is_selenium_grid_ready(self):
                self.log.info('Selenium grid is ready')
                return True
        except URLError:
            pass
        time.sleep(5)


def is_selenium_grid_ready(self):
    res = request.urlopen(self.remoteWdHubUrl + "/status")
    json_response = json.loads(res.read().decode())
    return json_response.get('value', {}).get('ready', False)
