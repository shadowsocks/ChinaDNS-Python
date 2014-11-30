#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, 'shadowsocks')
import os
import signal
import select
from subprocess import Popen, PIPE

with open(sys.argv[-1]) as f:
    dig_cmd = f.read()
p1 = Popen(['sudo', sys.executable, 'chinadns/dnsrelay.py'], shell=False,
           bufsize=0, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
p2 = None

try:
    local_ready = False
    server_ready = False
    fdset = [p1.stdout, p1.stderr]
    while True:
        r, w, e = select.select(fdset, [], fdset)
        if e:
            break

        for fd in r:
            line = fd.readline()
            sys.stdout.write(line)
            if line.find('starting dns') >= 0:
                local_ready = True

        if local_ready and p2 is None:
            p2 = Popen(dig_cmd.split(), shell=False, bufsize=0, close_fds=True)
            break

    if p2 is not None:
        r = p2.wait()
        if r == 0:
            print 'test passed'
        sys.exit(r)

finally:
    for p in [p1, p2]:
        try:
            os.kill(p.pid, signal.SIGTERM)
        except OSError:
            pass

sys.exit(-1)
