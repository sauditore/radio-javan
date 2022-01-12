from core.base_request import RjBaseRequest

import logging

logger = logging.getLogger(__name__)


class UserAuth(RjBaseRequest):

    def signup(self, name, last_name, email, password):
        address = "https://www.radiojavan.com/signup"
        token_result = self.extract_token(address)
        if not token_result[0]:
            return False, None
        post_data = {"authenticity_token": token_result[1],
                     "firstname": name,
                     "lastname": last_name,
                     "email": email,
                     "email_confirm": email,
                     "password": password,
                     "agree_terms": "on",
                     "utf8": "✓"}
        self.set_ajax()
        result = self.post(address, post_data, True)
        return result

    def login(self, username, password):
        address = "https://r-j-app-desk.com/api2/login"
        # token_data = self.extract_token(address)
        # if not token_data[0]:
        #     return False
        data = {"login_email": username,
                "login_password": password
                }
        return self.post(address, data, True, False)

    def user_profile(self):
        address = "https://r-j-app-desk.com/api2/user_profile?stats=1"
        res = self.get(address, True)
        return res

    def get_subscription(self):
        return self.get("https://r-j-app-desk.com/api2/user_subscription", True)

    # def logout(self):
    #     address = "https://www.radiojavan.com/account/logout"
    #     res = self.post(address, {"logout": True}, as_json=True, as_ajax=True)
    #     if "success" not in res:
    #         return False
    #     return res["success"]
