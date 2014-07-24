ChinaDNS
=========

[![PyPI version]][PyPI] [![Build Status]][Travis CI]

A DNS forwarder that ignores incorrect(you knew it) responses.

Install
-------

* Linux / OS X

    * ```pip install chinadns```

* Windows

    * [Download]

Usage
-----

Run `sudo chinadns` on your local machine. ChinaDNS creates a DNS server at
`127.0.0.1:53`.

Set your DNS to 127.0.0.1 and you're done.

    $ nslookup www.youtube.com
    Server:		127.0.0.1
    Address:	127.0.0.1#53
    
    Non-authoritative answer:
    www.youtube.com	canonical name = youtube-ui.l.google.com.
    youtube-ui.l.google.com	canonical name = youtube-ui-china.l.google.com.
    Name:	youtube-ui-china.l.google.com
    Address: 173.194.72.102
    Name:	youtube-ui-china.l.google.com
    Address: 173.194.72.101
    Name:	youtube-ui-china.l.google.com
    Address: 173.194.72.113
    Name:	youtube-ui-china.l.google.com
    Address: 173.194.72.100
    Name:	youtube-ui-china.l.google.com
    Address: 173.194.72.139
    Name:	youtube-ui-china.l.google.com
    Address: 173.194.72.138

Advanced
--------

    usage: chinadns [-h] [-b BIND_ADDR] [-p BIND_PORT] [-s DNS]

    Forward DNS requests.

    optional arguments:
      -h, --help            show this help message and exit
      -b BIND_ADDR, --local_address BIND_ADDR
                            address that listens, default: 127.0.0.1
      -p BIND_PORT, --local_port BIND_PORT
                            port that listens, default: 53
      -s DNS, --dns DNS     DNS server to use, default:
                            114.114.114.114,208.67.222.222,8.8.8.8

License
-------
MIT

Bugs and Issues
----------------
Please visit [Issue Tracker]

Mailing list: http://groups.google.com/group/shadowsocks


[Build Status]:    https://img.shields.io/travis/clowwindy/ChinaDNS/master.svg?style=flat
[Download]:        http://sourceforge.net/projects/shadowsocksgui/files/dist/ChinaDNS-win32-0.1.11.rar/download
[Issue Tracker]:   https://github.com/clowwindy/ChinaDNS/issues?state=open
[PyPI]:            https://pypi.python.org/pypi/chinadns
[PyPI version]:    https://img.shields.io/pypi/v/chinadns.svg?style=flat
[Shadowsocks]:     https://github.com/clowwindy/shadowsocks
[Travis CI]:       https://travis-ci.org/clowwindy/ChinaDNS
