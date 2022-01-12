import asyncore
import datetime
import email
from pathlib import Path
from smtpd import SMTPServer
from uuid import uuid4

from models import Domain, Receiver, MailInformation, MailAttachment


class EmailServer(SMTPServer):

    email_number = 0

    HOME = Path(__file__).parent / "users"

    def process_message(self, peer, mail_from, tos, data, **kwargs):
        tos_list = tos[0].split("@")
        if len(tos_list) < 2:
            print("BAD")
            return "450 Bad Mailbox"
        domain = Domain.select().where(Domain.is_active == True, Domain.name.ilike(tos_list[1])).first()
        if not domain:
            print("BAD2")
            return "405 Bad Mailbox"
        rc = Receiver.select().where(Receiver.domain == domain.id, Receiver.mail.ilike(tos_list[0])).first()
        if not rc:
            print("BAD3")
            return "405 Bad Mailbox"
        # After validation and recovering data, now create message
        mail = email.message_from_bytes(data)
        subject = mail.get("Subject")
        sender = mail.get("From")

        if not subject:
            subject = ""
        if not sender:
            sender = mail_from
        message = MailInformation.create(id=uuid4(), sender=mail_from, subject=subject, sender_name=sender,
                                         receive_date=datetime.datetime.now(), receiver=rc)
        for part in mail.walk():
            pl = part.get_payload()
            if isinstance(pl, list):
                continue
            fn = str(uuid4())
            real_file_name = ""
            header_file_name = part.get("Content-Disposition")
            if header_file_name:
                name = header_file_name.split("filename=", maxsplit=1)
                if len(name) > 1:
                    real_file_name = name[1][1:-1]
            attach_file_name = self.HOME / fn
            attach_data = open(attach_file_name, "wb")
            attach_data.write(pl.encode())
            attach_data.close()
            content_type = part.get("Content-Type", "")
            real_type = content_type.split(";")[0]
            MailAttachment.create(id=uuid4(), file_path=fn, ct=real_type, mail=message,
                                  file_name=real_file_name)

        self.email_number += 1


def run():
    foo = EmailServer(('localhost', 25), None)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    run()
