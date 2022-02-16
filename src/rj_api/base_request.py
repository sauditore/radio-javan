import logging

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class RjBaseRequest(object):

    # We need to change the port for all sub-classes.
    proxy_port = 2000

    def __init__(self, session=None):
        if session is None:
            self.session = requests.Session()
            self.session.headers["User-Agent"] = "Radio Javan/16.9.1 (iPhone; iOS 15.2; Scale/3.00) com.RadioJavan.RJ"
            self.session.headers["Sec-Fetch-Site"] = "cross-site"
            self.session.headers["Sec-Fetch-Mode"] = "cors"
            self.session.headers["Sec-Fetch-Dest"] = "empty"
            self.session.headers["Sec-Fetch-Dest"] = "empty"
            self.session.headers["Referer"] = "https://d2ztbi9tgqidw4.cloudfront.net/"
            self.session.headers["Accept-Language"] = "en-US"
            # self.session.get("https://r-j-app-desk.com/api2/app_config")
        else:
            self.session = session

    def _get_next_proxy_port(self):
        if self.proxy_port >= 2179:
            self.proxy_port = 2000
        return self.proxy_port

    def read_config(self):
        return self.session.get("https://r-j-app-desk.com/api2/app_config").json()

    def get_session(self):
        return self.session

    def download_file(self, address):
        local_filename = address.split('/')[-1]

        # NOTE the stream=True parameter below
        with self.session.get(address, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return local_filename

    def set_ajax(self):
        self.session.headers["X-Requested-With"] = "XMLHttpRequest"

    def unset_ajax(self):
        del self.session.headers["X-Requested-With"]

    def extract_token(self, address):
        data = self.get(address, False, True)
        if not data:
            logger.error("Load error! No data returned")
            return False, None
        html_data = BeautifulSoup(data, 'html.parser')
        token = html_data.find_all("input", {'name': 'authenticity_token'})
        if len(token) < 1:
            logger.error("Load Error! Token not found.")
            return False, None
        token_data = token[0].get("value")
        if not token_data:
            logger.error("Load Error! Token data is not valid.")
            return False, None
        return True, token_data

    def _get_proxy(self):
        px = self._get_next_proxy_port()
        res = {"http": f"socks4://127.0.0.1:{px}", "https": f"socks4://127.0.0.1:{px}"}
        return res

    def get(self, address, as_json=False, enable_proxy=False):
        if enable_proxy:
            response = self.session.get(address, proxies=self._get_proxy())
        else:
            response = self.session.get(address)
        if response.status_code == 200:
            if as_json:
                return response.json()
            return response.content
        logger.warning(f"Expected status 200 but got other data : {response.status_code}")

    def post(self, address, data: dict, as_json=False, as_ajax=False, enable_proxy=False, cookies={}):
        if as_ajax:
            self.set_ajax()
        try:
            if enable_proxy:
                response = self.session.post(address, data=data, proxies=self._get_proxy(), cookies=cookies)
            else:
                response = self.session.post(address, data=data, cookies=cookies)
        except:
            return {}
        if as_ajax:
            self.unset_ajax()
        if response.status_code == 200:
            if as_json:
                try:
                    return response.json()
                except Exception as e:
                    logger.error(e.args)
                    return {}
            return response.content
        logger.warning(f"Expected status 200 but got other data : {response.status_code}")
