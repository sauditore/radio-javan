import email
import re

from imapclient import IMAPClient, imapclient
import logging

logger = logging.getLogger(__name__)


def get_activation_link(host, username, password, sender):
    activate_link = re.compile(r"<(https://rj-app.app.+)+>", re.IGNORECASE)
    with IMAPClient(host, ssl=False) as client:
        try:
            client.login(username, password)
            client.select_folder("INBOX")
            messages = client.search(["FROM", sender])
            response = client.fetch(messages, 'RFC822').items()
            for m in response:
                email_message = email.message_from_bytes(m[1][b"RFC822"])
                payloads = email_message.get_payload()
                text = payloads[0].get_payload()
                link = activate_link.findall(text)
                if len(link) > 0:
                    return link[0]
        except imapclient.exceptions.LoginError:
            logger.error(f"Login failed for {username}")

    #
    # imap = imaplib.IMAP4(host)
    # try:
    #     imap.login(username, password)
    #     logger.debug(f"{username} Login success")
    #     imap.select("inbox")
    #     _, data = imap.search(None, "ALL")
    #     for mail in data[0].split():
    #         _, data = imap.fetch(mail, '(RFC822)')
    #         print('Message %s\n%s\n' % (mail, data[0][1]))
    #     imap.logout()
    #     return True
    # except:
    #     logger.error(f"{username} failed to login")
    #     return False
    #
