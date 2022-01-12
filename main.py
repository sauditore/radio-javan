from core.check_mail import get_activation_link
from core.media import MP3
from core.user_auth import UserAuth


def start_account_creator(users_file):
    pass


if __name__ == '__main__':

    link: str = get_activation_link("65.21.103.11", "me@kara-sanaat.com", "4311Pi0042", "info@radiojavan.com")

    print(link)
    exit(1)
    z = UserAuth()
    print(z.login("kaxelet990@unigeol.com", "123123123"))
    print(z.user_profile())
    mp3 = MP3(z.get_session())
    print(mp3.get_playlist())
    info = mp3.info(103930)
    print(mp3.download_file(info.get("link")))

    # print(mp3.vote(103930))
    # print(z.logout())
