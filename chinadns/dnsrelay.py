#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2014 clowwindy
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import time
import socket
import errno
import logging

info = sys.version_info
if not (info[0] == 2 and info[1] >= 7):
    print 'Python 2.7 required'
    sys.exit(1)

import argparse
from shadowsocks import eventloop, asyncdns, lru_cache


BUF_SIZE = 16384

CACHE_TIMEOUT = 10

GFW_LIST = set(["74.125.127.102", "74.125.155.102", "74.125.39.102",
                "74.125.39.113", "209.85.229.138", "128.121.126.139",
                "159.106.121.75", "169.132.13.103", "192.67.198.6",
                "202.106.1.2", "202.181.7.85", "203.161.230.171",
                "203.98.7.65", "207.12.88.98", "208.56.31.43",
                "209.145.54.50", "209.220.30.174", "209.36.73.33",
                "211.94.66.147", "213.169.251.35", "216.221.188.182",
                "216.234.179.13", "243.185.187.39", "37.61.54.158",
                "4.36.66.178", "46.82.174.68", "59.24.3.173", "64.33.88.161",
                "64.33.99.47", "64.66.163.251", "65.104.202.252",
                "65.160.219.113", "66.45.252.237", "72.14.205.104",
                "72.14.205.99", "78.16.49.15", "8.7.198.45", "93.46.8.89"])


class DNSRelay(object):
    def __init__(self, config):
        self._loop = None
        self._config = config
        self._last_time = time.time()

        self._local_addr = (config['local_address'], 53)
        self._remote_addr = (config['dns'], 53)

    def add_to_loop(self, loop):
        if self._loop:
            raise Exception('already add to loop')
        self._loop = loop
        loop.add_handler(self.handle_events)

    def handle_events(self, events):
        pass


class UDPDNSRelay(DNSRelay):
    def __init__(self, config):
        DNSRelay.__init__(self, config)

        self._id_to_addr = lru_cache.LRUCache(CACHE_TIMEOUT)
        self._local_sock = None
        self._remote_sock = None
        self._create_sockets()

    def _create_sockets(self):
        sockets = []
        for addr in (self._local_addr, self._remote_addr):
            addrs = socket.getaddrinfo(addr[0], addr[1], 0,
                                       socket.SOCK_DGRAM, socket.SOL_UDP)
            if len(addrs) == 0:
                raise Exception("can't get addrinfo for %s:%d" % addr)
            af, socktype, proto, canonname, sa = addrs[0]
            sock = socket.socket(af, socktype, proto)
            sock.setblocking(False)
            sockets.append(sock)
        self._local_sock, self._remote_sock = sockets
        self._local_sock.bind(self._local_addr)

    def _rebuild_sockets(self):
        self._id_to_addr.clear()
        self._loop.remove(self._local_sock)
        self._loop.remove(self._remote_sock)
        self._local_sock.close()
        self._remote_sock.close()
        self._create_sockets()

    def add_to_loop(self, loop):
        DNSRelay.add_to_loop(self, loop)

        loop.add(self._local_sock, eventloop.POLL_IN)
        loop.add(self._remote_sock, eventloop.POLL_IN)

    def _handle_local(self, sock):
        try:
            data, addr = sock.recvfrom(BUF_SIZE)
        except (OSError, IOError) as e:
            logging.error(e)
            if eventloop.errno_from_exception(e) == errno.ECONNRESET:
                # just for Windows lol
                self._rebuild_sockets()
            return
        header = asyncdns.parse_header(data)
        if header:
            try:
                req_id = header[0]
                req = asyncdns.parse_response(data)
                self._id_to_addr[req_id] = addr
                self._remote_sock.sendto(data, self._remote_addr)
                logging.info('request %s', req.hostname)
            except Exception as e:
                import traceback

                traceback.print_exc()
                logging.error(e)

    def _handle_remote(self, sock):
        try:
            data, addr = sock.recvfrom(BUF_SIZE)
        except (OSError, IOError) as e:
            logging.error(e)
            if eventloop.errno_from_exception(e) == errno.ECONNRESET:
                # just for Windows lol
                self._rebuild_sockets()
            return
        if data:
            try:
                header = asyncdns.parse_header(data)
                if header:
                    req_id = header[0]
                    res = asyncdns.parse_response(data)
                    logging.info('response %s', res)
                    addr = self._id_to_addr.get(req_id, None)
                    if addr:
                        for answer in res.answers:
                            if answer and answer[0] in GFW_LIST:
                                return
                        self._local_sock.sendto(data, addr)
                        del self._id_to_addr[req_id]
            except Exception as e:
                import traceback
                traceback.print_exc()
                logging.error(e)
                if eventloop.errno_from_exception(e) == errno.EACCES:
                    # when we have changed our ip
                    self._rebuild_sockets()

    def handle_events(self, events):
        for sock, fd, event in events:
            if sock == self._local_sock:
                self._handle_local(sock)
            elif sock == self._remote_sock:
                self._handle_remote(sock)
        now = time.time()
        if now - self._last_time > CACHE_TIMEOUT / 2:
            self._id_to_addr.sweep()


class TCPDNSRelay(DNSRelay):
    def __init__(self, config):
        DNSRelay.__init__(self, config)

        self._local_to_remote = {}
        self._remote_to_local = {}

        addrs = socket.getaddrinfo(self._local_addr[0], self._local_addr[1], 0,
                                   socket.SOCK_STREAM, socket.SOL_TCP)
        if len(addrs) == 0:
            raise Exception("can't get addrinfo for %s:%d" % self._local_addr)
        af, socktype, proto, canonname, sa = addrs[0]
        self._listen_sock = socket.socket(af, socktype, proto)
        self._listen_sock.setblocking(False)
        self._listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._listen_sock.bind(self._local_addr)
        self._listen_sock.listen(1024)

    def _handle_conn(self, sock):
        try:
            local, addr = sock.accept()
            addrs = socket.getaddrinfo(self._remote_addr[0],
                                       self._remote_addr[1], 0,
                                       socket.SOCK_STREAM, socket.SOL_TCP)
            if len(addrs) == 0:
                raise Exception("can't get addrinfo for %s:%d" %
                                self._remote_addr)
            af, socktype, proto, canonname, sa = addrs[0]
            remote = socket.socket(af, socktype, proto)
            local.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
            remote.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
            self._local_to_remote[local] = remote
            self._remote_to_local[remote] = local

            self._loop.add(local, 0)
            self._loop.add(remote, eventloop.POLL_OUT)
            try:
                remote.connect(self._remote_addr)
            except (OSError, IOError) as e:
                if eventloop.errno_from_exception(e) in (errno.EINPROGRESS,
                                                         errno.EAGAIN):
                    pass
                else:
                    raise
        except (OSError, IOError) as e:
            logging.error(e)

    def _destroy(self, local, remote):
        if local in self._local_to_remote:
            self._loop.remove(local)
            self._loop.remove(remote)
            del self._local_to_remote[local]
            del self._remote_to_local[remote]
            local.close()
            remote.close()
        else:
            logging.error('already destroyed')

    def _handle_local(self, local, event):
        remote = self._local_to_remote[local]
        if event & (eventloop.POLL_ERR | eventloop.POLL_HUP):
            self._destroy(local, remote)
        elif event & eventloop.POLL_IN:
            try:
                data = local.recv(BUF_SIZE)
                if not data:
                    self._destroy(local, remote)
                else:
                    remote.send(data)
            except (OSError, IOError) as e:
                self._destroy(local, self._local_to_remote[local])
                logging.error(e)

    def _handle_remote(self, remote, event):
        local = self._remote_to_local[remote]
        if event & (eventloop.POLL_ERR | eventloop.POLL_HUP):
            self._destroy(local, remote)
        elif event & eventloop.POLL_OUT:
            self._loop.modify(remote, eventloop.POLL_IN)
            self._loop.modify(local, eventloop.POLL_IN)
        elif event & eventloop.POLL_IN:
            try:
                data = remote.recv(BUF_SIZE)
                if not data:
                    self._destroy(local, remote)
                else:
                    try:
                        res = asyncdns.parse_response(data[2:])
                        if res:
                            logging.info('response %s', res)
                    except Exception as e:
                        logging.error(e)
                    local.send(data)
            except (OSError, IOError) as e:
                self._destroy(local, remote)
                logging.error(e)

    def add_to_loop(self, loop):
        DNSRelay.add_to_loop(self, loop)
        loop.add(self._listen_sock, eventloop.POLL_IN)

    def handle_events(self, events):
        for sock, fd, event in events:
            if sock == self._listen_sock:
                self._handle_conn(sock)
            elif sock in self._local_to_remote:
                self._handle_local(sock, event)
            elif sock in self._remote_to_local:
                self._handle_remote(sock, event)
                # TODO implement timeout


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S', filemode='a+')

    parser = argparse.ArgumentParser(description='Forward DNS requests.')
    parser.add_argument('-b', '--local_address', metavar='BIND_ADDR', type=str,
                        help='address that listens, default: 127.0.0.1',
                        default='127.0.0.1')
    parser.add_argument('-s', '--dns', metavar='DNS', type=str,
                        help='DNS server to use, default: 8.8.8.8',
                        default='8.8.8.8')

    config = vars(parser.parse_args())

    logging.info("starting dns at %s:%d" % (config['local_address'], 53))

    loop = eventloop.EventLoop()

    try:
        udprelay = UDPDNSRelay(config)
        udprelay.add_to_loop(loop)
        tcprelay = TCPDNSRelay(config)
        tcprelay.add_to_loop(loop)
        loop.run()
    except (OSError, IOError) as e:
        logging.error(e)
        if eventloop.errno_from_exception(e) == errno.EACCES:
            logging.info('please use sudo to run this program')
        exit(1)


if __name__ == '__main__':
    main()
