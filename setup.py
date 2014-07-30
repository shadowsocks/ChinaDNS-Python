from setuptools import setup


with open('README.rst') as f:
    long_description = f.read()

setup(
    name="chinadns",
    version="0.2.0",
    license='MIT',
    description="A DNS forwarder that ignore incorrect responses",
    author='clowwindy',
    author_email='clowwindy42@gmail.com',
    url='https://github.com/clowwindy/ChinaDNS',
    packages=['chinadns'],
    package_data={
        'chinadns': ['README.rst', 'LICENSE', 'config.json']
    },
    install_requires=[
        'shadowsocks==2.0.11'
    ],
    entry_points="""
    [console_scripts]
    chinadns = chinadns.dnsrelay:main
    """,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: Proxy Servers',
    ],
    long_description=long_description,
)
