#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ponypass – Secure superultraawesomemasing passphrase wallet
# 
# Copyright © 2013  Mattias Andrée (maandree@member.fsf.org)
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
from subprocess import Popen, PIPE


HOME = os.environ['HOME']
WALLET_DIR = '%s/.ponypass'
WALLET = '%s/wallet' % WALLET_DIR
GPG_ID = '%s/id' % WALLET_DIR


def gpg_encrypt(data, file):
    id = None
    if not os.path.exists(GPG_ID):
        print('\e[01;34mPlease enter your GPG key ID.\e[00m')
        id = input()
        with open(GPG_ID, 'wb') as idfile:
            idfile.write((id + '\n').encode('utf-8'))
    elif not os.path.isfile(GPG_ID):
        print('%s: %s is not a regular file or link to a regular file' % (sys.argv[0], GPG_ID), file = sys.stderr)
        sys.exit(1)
    
    if id is None:
        with open(GPG_ID, 'rb') as idfile:
            id = idfile.read().decode('utf-8', 'error')
        while id.endswith('\n'):
            id = id[:-1]
    
    while True:
        gpg = Popen(['gpg', '--encrypt', '--recipient', id], stdin = PIPE, stdout = PIPE)
        out = gpg.communicate(data)[0]
        if gpg.returncode != 0:
            print('\e[01;34mGPG failed, press enter to retry or C-c to abort.\e[00m')
        else:
            with open(file, 'wb') as wfile:
                wfile.write(out)
            break


def gpg_decrypt(file):
    while True:
        data = None
        with open(file, 'rb') as wfile:
            data = wfile.read()
        gpg = Popen(['gpg', '--decrypt'], stdin = PIPE, stdout = PIPE)
        out = gpg.communicate(data)[0]
        if gpg.returncode != 0:
            print('\e[01;34mGPG failed, press enter to retry or C-c to abort.\e[00m')
        else:
            return out.decode('utf-8', 'error')


if not os.path.exists(WALLET):
    os.makedirs(WALLET_DIR, exist_ok = True)
    print('\e[01;34mCreating a wallet.\e[00m', file = sys.stderr)
    gpg_encrypt('()\n'.encode('utf-8'), WALLET)
elif not os.path.isfile(WALLET):
    print('%s: %s is not a regular file or link to a regular file' % (sys.argv[0], WALLET), file = sys.stderr)
    sys.exit(1)


print('\e[01;34mLoading wallet.\e[00m', file = sys.stderr)
wallet = gpg_decrypt(WALLET)

# TODO

print('\e[01;34mSaving wallet.\e[00m', file = sys.stderr)
gpg_crypt(wallet, WALLET)

