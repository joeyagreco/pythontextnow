<div align="center">

<br>
<br>
<img src="https://raw.githubusercontent.com/joeyagreco/pythontextnow/main/img/textnow_logo__.png" alt="textnow logo" width="400"/>

Python wrapper for the MyFantasyLeague API.

[TextNow Website](https://www.textnow.com/)

![Last Commit](https://img.shields.io/github/last-commit/joeyagreco/pythontextnow)
</div>

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install.

```bash
pip install pythontextnow
```

## Usage

Make sure you have the following before you begin:

- TextNow username
- CSRF cookie
- SID cookie

For a guide on how to obtain these for your account, check [here](https://github.com/joeyagreco/pythontextnow#setup).

Before you can call any methods, you must first set up your client config.

```python3
from pythontextnow.api.Client import Client

USERNAME = "{your_username}"
SID_COOKIE = "{your_sid_cookie}"
CSRF_COOKIE = "{your_csrf_cookie}"

Client.set_client_config(username=USERNAME, sid_cookie=SID_COOKIE, csrf_cookie=CSRF_COOKIE)
```

The MessageService is how you will perform any action.

It takes a phone number which defines which conversation you would like to perform an action on.

```python3
from pythontextnow.service.MessageService import MessageService

PHONE_NUMBER = "{phone_number}"
message_service = MessageService(conversation_phone_number=PHONE_NUMBER)
```

## Setup

### Obtaining Your Cookies

You will need to know your TextNow username to utilize this library.

This is the same username that you would use to log in.

To find this username:

- Go to [TextNow's messaging page](https://www.textnow.com/messaging)
- Click "Settings"
- Your username will be listed under "Account"

### Obtaining Your Username

You will need a CSRF cookie and an SID cookie to utilize this library.

To find these cookies:

In **Chrome**:

- Go to [TextNow's messaging page](https://www.textnow.com/messaging)
- Access [Developer Tools](https://developer.chrome.com/docs/devtools/open/) in your browser
- Click on the "Application" tab
- Go to "Storage" -> "Cookies"
- Search for the "connect.sid" name, the value will be your SID cookie
- Search for the "_csrf" name, the value will be your CSRF cookie

In **Firefox**

Access [Developer Tools](https://firefox-source-docs.mozilla.org/devtools-user/#:~:text=You%20can%20open%20the%20Firefox,%2B%20Opt%20%2B%20I%20on%20macOS.)

- Click on the "Storage" tab
- Go to "Storage" -> "Cookies"
- Search for the "connect.sid" name, the value will be your SID cookie
- Search for the "_csrf" name, the value will be your CSRF cookie

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)