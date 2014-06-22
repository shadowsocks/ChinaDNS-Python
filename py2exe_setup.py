from distutils.core import setup
import sys
import os
import py2exe # require

# require shadowsocks
sspath = os.path.abspath(os.path.join("..", "shadowsocks"))
sys.path.append(sspath)

with open('README.rst') as f:
    long_description = f.read()

includes = ["shadowsocks"]
console = [os.path.join("chinadns", "dnsrelay.py")]


setup(
    name="chinadns",
    version="0.1.4",
    license="MIT",
    description="A DNS forwarder that ignore incorrect responses",
    author='clowwindy',
    author_email='clowwindy42@gmail.com',
    url='https://github.com/clowwindy/ChinaDNS',
    packages=['chinadns'],
    options={'py2exe': {'includes': includes}},
    console=console,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: Proxy Servers',
    ],
    long_description=long_description,
)
