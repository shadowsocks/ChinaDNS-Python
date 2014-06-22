from distutils.core import setup
import sys
import os

# require import
import py2exe

# require shadowsocks
sspath = os.path.abspath(os.path.join("..", "shadowsocks"))
if not os.path.isdir(sspath):
    raise IOError("require shadowsocks")

sys.path.append(sspath)

with open('README.rst') as f:
    long_description = f.read()

includes = ["shadowsocks"]
console = [os.path.join("chinadns", "dnsrelay.py")]


setup(
    name="chinadns",
    license="MIT",
    description="A DNS forwarder that ignore incorrect responses",
    author='clowwindy',
    author_email='clowwindy42@gmail.com',
    url='https://github.com/clowwindy/ChinaDNS',
    packages=['chinadns'],
    data_files=["README.md", "LICENSE", "config.json", "CHANGES"],
    options={'py2exe': {
        'includes': includes,
        'dll_excludes': ['w9xpopen.exe'],
        'bundle_files': 1,
        'compressed': True}},
    console=console,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: Proxy Servers',
    ],
    long_description=long_description,
)
