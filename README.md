<div align="center">

<br>
<br>
<img src="https://raw.githubusercontent.com/joeyagreco/pythontextnow/main/img/pythontextnow_logo_.png" alt="pythontextnow logo" width="450"/>

A Python wrapper for TextNow.

[TextNow Website](https://www.textnow.com/)

![Main Build](https://github.com/joeyagreco/pythontextnow/actions/workflows/main-build.yml/badge.svg)
![Last Commit](https://img.shields.io/github/last-commit/joeyagreco/pythontextnow)
</div>

### Table of Contents

- [Installation](https://github.com/joeyagreco/pythontextnow#installation)
- [Usage](https://github.com/joeyagreco/pythontextnow#usage)
    - [Configure Client](https://github.com/joeyagreco/pythontextnow#configure-client)
    - [Get Messages](https://github.com/joeyagreco/pythontextnow#get-messages)
    - [Send a Message](https://github.com/joeyagreco/pythontextnow#send-a-message)
    - [Send Media](https://github.com/joeyagreco/pythontextnow#send-media)
    - [Delete a Message](https://github.com/joeyagreco/pythontextnow#delete-a-message)
    - [Delete a Conversation](https://github.com/joeyagreco/pythontextnow#delete-a-conversation)
    - [Mark a Message as Read](https://github.com/joeyagreco/pythontextnow#mark-a-message-as-read)
- [Setup](https://github.com/joeyagreco/pythontextnow#setup)
    - [Obtaining Your Username](https://github.com/joeyagreco/pythontextnow#obtaining-your-username)
    - [Obtaining Your Cookies](https://github.com/joeyagreco/pythontextnow#obtaining-your-cookies)
- [Running Tests](https://github.com/joeyagreco/pythontextnow#running-tests)
- [Contributing](https://github.com/joeyagreco/pythontextnow#contributing)
- [License](https://github.com/joeyagreco/pythontextnow#license)

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
from pythontextnow import Client

USERNAME = "{your_username}"
SID_COOKIE = "{your_sid_cookie}"
CSRF_COOKIE = "{your_csrf_cookie}"

Client.set_client_config(username=USERNAME, sid_cookie=SID_COOKIE, csrf_cookie=CSRF_COOKIE)
```

The ConversationService is how you will perform any action.

It takes a list of phone numbers which defines which conversation you would like to perform your actions on.

```python3
from pythontextnow import ConversationService

PHONE_NUMBER_1 = "{some_phone_number}"
PHONE_NUMBER_2 = "{some_other_phone_number}"
conversation_service = ConversationService(conversation_phone_numbers=[PHONE_NUMBER_1, PHONE_NUMBER_2])
```

### Get Messages

The `get_messages()` method will return a [generator object](https://docs.python.org/3/glossary.html#term-generator).

This will return the messages from most -> least recent.

You can call `next()` with the returned generator each time you want to get the next group of messages.

```python3
messages_generator = conversation_service.get_messages()

messages = next(messages_generator)
```

You can also use a for loop to get all messages in a conversation.

```python3
messages_generator = conversation_service.get_messages()

all_messages = list()
for message_list in messages_generator:
    all_messages += message_list
```

You can specify how many messages back you would like to be retrieved by using the `num_messages` keyword argument.

```python3
messages_generator = conversation_service.get_messages(num_messages=10)

last_10_messages = list()
for message_list in messages_generator:
    last_10_messages += message_list
```

### Send a Message

To send a text message, use the `send_message()` method.

```python3
conversation_service.send_message(message="Hello World!")
```

### Send Media

To send media, use the `send_media()` method.

You can send:

- Images
- Videos
- GIFs

```python3
conversation_service.send_message(file_path="C:\\my_media.png")
```

### Delete a Message

To delete a message, use the `delete_message()` method.

Delete a message by its ID.

```python3
conversation_service.delete_message(message_id="123456")
```

<!---
// @formatter:off
-->
Delete a message with its [Message](https://github.com/joeyagreco/pythontextnow/blob/main/pythontextnow/model/Message.py) object.
<!---
// @formatter:on
-->

```python3
# assume you had a Message object saved to the variable "message_obj"

conversation_service.delete_message(message=message_obj)
```

### Delete a Conversation

To delete a conversation, use the `delete_conversation()` method.

```python3
conversation_service.delete_conversation()
```

### Mark a Message as Read

To mark a message as read, use the `mark_as_read()` method.

Mark a single message as read.

```python3
# assume you had a Message object saved to the variable "message_obj"

conversation_service.mark_as_read(message=message_obj)
```

Mark a list of messages as read.

```python3
# assume you had a list of Message objects saved to the variable "message_list"

conversation_service.mark_as_read(messages=message_list)
```

## Setup

### Obtaining Your Username

You will need to know your TextNow username to utilize this library.

This is the same username that you would use to log in.

To find this username:

- Go to [TextNow's messaging page](https://www.textnow.com/messaging) (make sure you are logged in)
- Click "Settings"
- Your username will be listed under "Account"

### Obtaining Your Cookies

You will need a CSRF cookie and an SID cookie to utilize this library.

To find these cookies:

- Go to [TextNow's messaging page](https://www.textnow.com/messaging)

> In **Chrome**:
> - Access [Developer Tools](https://developer.chrome.com/docs/devtools/open/) in your browser
> - Click on the "Application" tab
> - Go to "Storage" -> "Cookies"

> In **Firefox**
> - Access [Developer Tools](https://firefox-source-docs.mozilla.org/devtools-user/) in your browser
> - Click on the "Storage" tab
> - Go to "Storage" -> "Cookies"

- Search for the "connect.sid" name, the value will be your SID cookie
- Search for the "_csrf" name, the value will be your CSRF cookie

## Running Tests

To run tests, run the following command:

```bash
  pytest
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)