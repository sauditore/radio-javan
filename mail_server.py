import asyncore
import email
from smtpd import SMTPServer
import re

import requests
import logging

logger = logging.getLogger(__name__)


class EmailServer(SMTPServer):

    email_number = 0

    activate_link = re.compile(r"<(https://rj-app.app.+)+>", re.IGNORECASE)

    def process_message(self, peer, mail_from, tos, data, **kwargs):
        logger.info("A new mail is coming")
        tos_list = tos[0].split("@")
        if len(tos_list) < 2:
            logger.error("Bad Mailbox name")
            return "450 Bad Mailbox"

        email_message = email.message_from_bytes(data)
        payloads = email_message.get_payload()

        text = payloads[0].get_payload()
        print(text)
        link = self.activate_link.findall(text)
        if len(link) > 0:
            logger.info("Link detected.")
            try:
                requests.get(link[0])
                logger.info(f"User activated {tos[0]}")
                with open("active_user", "a") as f:
                    f.write(tos[0] + "\r\n")
            except Exception as e:
                logger.error(f"Failed to activate user {tos[0]}")
                logger.error(e.args)
                with open("errors.txt", "a") as error_file:
                    error_file.write(f"{tos[0]}\r\n")

        self.email_number += 1


def run():
    foo = EmailServer(('0.0.0.0', 25), None)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    run()
