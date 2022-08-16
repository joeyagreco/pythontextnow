<div align="center">

<br>
<br>
<img src="https://raw.githubusercontent.com/joeyagreco/pythontextnow/main/img/textnow_logo__.png" alt="textnow logo" width="400"/>

A Python wrapper for TextNow.

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

### Configure Client

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

### Get Messages

The `get_messages()` method will return a [generator object](https://docs.python.org/3/glossary.html#term-generator).

This will return the messages from most -> least recent.

You can call `next()` with the returned generator each time you want to get the next group of messages.

```python3
messages_generator = message_service.get_messages()

messages = next(messages_generator)
```

You can also use a for loop to get all messages in a conversation.

```python3
messages_generator = message_service.get_messages()

all_messages = list()
for message_list in messages_generator:
    all_messages += message_list
```

You can specify how many messages back you would like to be retrieved by using the `num_messages` keyword argument.

```python3
messages_generator = message_service.get_messages(num_messages=10)

all_messages = list()
for message_list in messages_generator:
    all_messages += message_list
```

### Send a Message

To send a text message, use the `send_message()` method.

```python3
message_service.send_message(message="Hello World!")
```

### Delete a Message

To delete a message, use the `delete_message()` method.

Delete a message by its ID.

```python3
message_service.delete_message(message_id="123456")
```

Delete a message with
its [Message](https://github.com/joeyagreco/pythontextnow/blob/main/pythontextnow/model/Message.py) object

```python3
# assume you had a Message object saved to the variable "message"

message_service.delete_message(message=message)
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