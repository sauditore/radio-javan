## Python Radio Javan API
<hr/>

Basic Radio Javan (Persian Music App) python API with proxy support for bad guys!

### Install: 

To install this library you can choose one of these steps:

1- Install from pip:
```
pip install python-rj-app
```

2- Install from this source:

```
python setup.py install
```

### Usage:
```python
from rj_api.user_auth import UserAuth
from rj_api.media import MP3

# Login user and get some info from user profile
user = UserAuth()
login_data = user.login("kaxelet990@unigeol.com", "123123123")
user.user_profile()

# now let's download an MP3 file!
user_session = user.get_session()
mp3 = MP3(user_session)
print(mp3.get_playlist())

# and if you want to download MP3:
info = mp3.info(103930)

# prints the save path of MP3 file
print(mp3.download_file(info.get("link")))
```

<hr/>

### Other API endpoints:
You can use RjBaseRequest class to extend API endpoints. All you need is a URL with its parameters and then POST it 
to server. 

### Bad Guys:
You may use this on your own to create bulk accounts! It's on your own. but you want to use my chain proxy too :)

### Contribute?
You are always welcome
