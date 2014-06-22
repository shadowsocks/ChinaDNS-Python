ChinaDNS
========

|PyPI version| |Build Status|

A DNS forwarder that ignores incorrect(you know it) responses.

Install
-------

::

    pip install chinadns

or

::

    easy_intall chinadns

Usage
-----

Run ``sudo chinadns`` on your local machine. ChinaDNS creates a DNS
server at ``127.0.0.1:53``.

Set your DNS to 127.0.0.1 and you're done.

::

    $ nslookup www.youtube.com
    Server:     127.0.0.1
    Address:    127.0.0.1#53

    Non-authoritative answer:
    www.youtube.com canonical name = youtube-ui.l.google.com.
    youtube-ui.l.google.com canonical name = youtube-ui-china.l.google.com.
    Name:   youtube-ui-china.l.google.com
    Address: 173.194.72.102
    Name:   youtube-ui-china.l.google.com
    Address: 173.194.72.101
    Name:   youtube-ui-china.l.google.com
    Address: 173.194.72.113
    Name:   youtube-ui-china.l.google.com
    Address: 173.194.72.100
    Name:   youtube-ui-china.l.google.com
    Address: 173.194.72.139
    Name:   youtube-ui-china.l.google.com
    Address: 173.194.72.138

License
-------

MIT

Bugs and Issues
---------------

Please visit `Issue
Tracker <https://github.com/clowwindy/ChinaDNS/issues?state=open>`__

Mailing list: http://groups.google.com/group/shadowsocks

.. |PyPI version| image:: https://img.shields.io/pypi/v/chinadns.svg?style=flat
   :target: https://pypi.python.org/pypi/chinadns
.. |Build Status| image:: https://img.shields.io/travis/clowwindy/ChinaDNS/master.svg?style=flat
   :target: https://travis-ci.org/clowwindy/ChinaDNS
