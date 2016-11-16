# Heathergraph

Python based text email printer for [Raspberry Pi](https://www.raspberrypi.org/) and [Pipsta](http://www.pipsta.co.uk/)

## Configuration

Configure your Raspberry Pi and Pipsta using as much of the instructions [here](https://bitbucket.org/ablesystems/pipsta/wiki/Pipsta%20First-Time%20Setup) as required.

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

