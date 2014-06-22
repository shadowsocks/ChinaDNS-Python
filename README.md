ChinaDNS
=========

[![PyPI version]][PyPI] [![Build Status]][Travis CI]

A DNS forwarder that ignores incorrect(you know it) responses.

Install
-------

    pip install chinadns
    
Usage
-----

Run `sudo chinadns` on your local machine. ChinaDNS creates a DNS server at `127.0.0.1:53`.

Set your DNS to 127.0.0.1 and you're done.

    $ dig @127.0.0.1 www.youtube.com
    
    ; <<>> DiG 9.8.3-P1 <<>> @127.0.0.1 www.youtube.com
    ; (1 server found)
    ;; global options: +cmd
    ;; Got answer:
    ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 22375
    ;; flags: qr rd ra; QUERY: 1, ANSWER: 8, AUTHORITY: 0, ADDITIONAL: 0
    
    ;; QUESTION SECTION:
    ;www.youtube.com.		IN	A
    
    ;; ANSWER SECTION:
    www.youtube.com.	21599	IN	CNAME	youtube-ui.l.google.com.
    youtube-ui.l.google.com. 899	IN	CNAME	youtube-ui-china.l.google.com.
    youtube-ui-china.l.google.com. 179 IN	A	173.194.72.102
    youtube-ui-china.l.google.com. 179 IN	A	173.194.72.139
    youtube-ui-china.l.google.com. 179 IN	A	173.194.72.113
    youtube-ui-china.l.google.com. 179 IN	A	173.194.72.100
    youtube-ui-china.l.google.com. 179 IN	A	173.194.72.138
    youtube-ui-china.l.google.com. 179 IN	A	173.194.72.101
    
    ;; Query time: 264 msec
    ;; SERVER: 127.0.0.1#53(127.0.0.1)
    ;; WHEN: Sun Jun 22 12:58:41 2014
    ;; MSG SIZE  rcvd: 194

License
-------
MIT

Bugs and Issues
----------------
Please visit [Issue Tracker]

Mailing list: http://groups.google.com/group/shadowsocks


[Build Status]:    https://img.shields.io/travis/clowwindy/ChinaDNS/master.svg?style=flat
[Issue Tracker]:   https://github.com/clowwindy/ChinaDNS/issues?state=open
[PyPI]:            https://pypi.python.org/pypi/chinadns
[PyPI version]:    https://img.shields.io/pypi/v/chinadns.svg?style=flat
[Shadowsocks]:     https://github.com/clowwindy/shadowsocks
[Travis CI]:       https://travis-ci.org/clowwindy/ChinaDNS
