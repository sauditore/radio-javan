from typing import Dict

from .base_request import RjBaseRequest

import logging

logger = logging.getLogger(__name__)


class UserAuth(RjBaseRequest):

    def signup(self,
               name: str,
               last_name: str,
               email: str,
               password: str
               ) -> bool:
        """
        Signup a new usr on radio javan.
        Mobile signup requires no special validation.

        :param name: name of the new user
        :param last_name: last name of the user
        :param email: email address
        :param password: a random password!
        :return: True if account created
        :rtype: bool
        """

        address = "https://d1gyyseacf3czm.cloudfront.net/api2/signup_mobile"
        post_data = {
                     "firstname": name,
                     "lastname": last_name,
                     "email": email,
                     "email_confirm": email,
                     "password": password,
                     "username": email.split("@")[0]+"."+last_name
                     }
        self.set_ajax()

        # init session
        result = self.post(address, post_data, True, enable_proxy=True, cookies={"_rj_web": "BAh7CUkiD3Nlc3Npb25faWQGOgZFVEkiJWMzN2RhOTg1ZTU4MmQyMzhjZDgzMmY1ZDVlZDQ0YTQ1BjsAVEkiDGdlb2luZm8GOwBGewg6D2lwX2FkZHJlc3NJIhI1LjExNy4xNTcuMjI1BjsAVDoMZXhwaXJlc0l1OglUaW1lDcmBHoCMJ78GCjoLb2Zmc2V0af6wuToJem9uZUkiCEVTVAY7AEY6DW5hbm9fbnVtaQJpAzoNbmFub19kZW5pBjoNc3VibWljcm8iB4cwOgdkYnsJOhFjb3VudHJ5X2NvZGVJIgdJUgY7AFQ6EWNvdW50cnlfbmFtZUkiCUlyYW4GOwBUOg1sYXRpdHVkZWYLMzUuNjk4Og5sb25naXR1ZGVmDDUxLjQxMTVJIg1hcHBfaG9tZQY7AEZUSSISYWRicmVha19jb3VudAY7AEZpBw==--bec9fb194d273879cbb6b8d88405b010054f3121;"})
        return result

    def login(self,
              username: str,
              password: str
              ) -> Dict:
        """
        Login to api service

        :param username: username
        :param password: password of user
        :return: data returned by server. Usually contains success parameter and a message
        :rtype: Dict
        """

        address = "https://r-j-app-desk.com/api2/login"
        data = {"login_email": username,
                "login_password": password
                }
        return self.post(address, data, True, False)

    def user_profile(self) -> Dict:
        """
        Dictionary contains data for the user profile and suggestions

        :return: User dashboard data
        :rtype: Dict
        """

        address = "https://r-j-app-desk.com/api2/user_profile?stats=1"
        res = self.get(address, True)
        return res

    def get_subscription(self) -> Dict:
        """
        Get user subscription information

        :return: Dict of user subscription
        :rtype: Dict
        """

        return self.get("https://r-j-app-desk.com/api2/user_subscription", True)
