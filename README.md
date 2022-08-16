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

## Setup

### Obtaining Your Cookies

You will need to know your TextNow username to utilize this library.

This is the same username that you would use to log in.

To find this username:

- Go to [TextNow's messaging page](https://www.textnow.com/messaging)
- Click "Settings"
- Your username will be listed under "Account"

### Obtaining Your Username

You will need a CSRF cookie and a SID cookie to utilize this library.

To find these cookies:

In Chrome:

- Go to [TextNow's messaging page](https://www.textnow.com/messaging)
- Access [Developer Tools](https://developer.chrome.com/docs/devtools/open/) in your browser
- Click on the "Application" tab
- Go to "Storage" -> "Cookies"
- Search for the "connect.sid" name, the value will be your SID cookie
- Search for the "_csrf" name, the value will be your CSRF cookie

In Firefox

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