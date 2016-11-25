# Heathergraph

Python based text email print server for [Raspberry Pi](https://www.raspberrypi.org/) and [Pipsta](http://www.pipsta.co.uk/)

## Configuration

Configure your Raspberry Pi and Pipsta using as many of the instructions [here](https://bitbucket.org/ablesystems/pipsta/wiki/Pipsta%20First-Time%20Setup) as required.

Create `heathergraph.ini` file in `heathergraph` folder containing:

```
[email]
*hostname: {imap server, default: imap.gmail.com}* 
username: {email address}
password: {email account password}
*folder: {email folder to watch, default: Inbox}*
*template: {message template to print, default: email.txt}*
```

## Startup

- Run the script directly from the terminal: `python heathergraph.py`
- Run the server script to create a background process: `python server.py start`
- Run the server on startup by adding `python {heathergraph path}/server.py start` to `/etc/rc.local`

## Templates

Emails are printed based on text templates containing field placeholders and formatting tags.

The default [email.txt](https://github.com/idiotandrobot/heathergraph/blob/master/templates/email.txt) template can be modified or new templates added and configured in `heathergraph.ini`.

The default [startup.txt](https://github.com/idiotandrobot/heathergraph/blob/master/templates/startup.txt) greeting template can also be customised.

The Pipsta prints 32 or 16 chars per line, depending on font, so templates should be formatted accordingly.

No wordwrapping is applied to any of the fields.

### Field Placeholders

Four fields are available for inclusion:-

- **from** - first name of sender
- **date** - message date formatted to `%a, %d %b %Y %H:%M:%S`
- **subject** - full subject of email
- **content** - text/plain content of email limited to printable ascii chars

```
--------------------------------
From: {from}
Date: {date}
Subject: {subject}
* * * * * * * * * * * * * * * * 
{content}
```

### Formatting Tags

Four tags are available for formatting. They do not stack so the last tag before some text will be applied.

- **reg** - Default regular font (32 chars per line)
- **tall** - Double height (32 chars per line, 57mm)
- **wide** - Double width (16 chars per line, 57mm)
- **u** - Underlined (32 chars per line) 

It's best practise to treat `reg` as a closing tag for the other three tags.

```
--------------------------------
<wide>{subject}<reg>
<tall>{content}<reg>

<u>from {from}
on {date}<reg> 
```

## Logging

Logging is configured in [logging.ini](https://github.com/idiotandrobot/heathergraph/blob/master/logging.ini). By default this will output DEBUG to the console and INFO to a `heathergraph.log` file in the run location.

Guide to Python logging [here](https://docs.python.org/2/howto/logging.html).