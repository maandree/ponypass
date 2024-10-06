#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ponypass – Secure superultraawesomemasing passphrase wallet
# 
# Copyright © 2013  Mattias Andrée (m@maandree.se)
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

import correctpony
import obscurepass


HOME = os.environ['HOME']
WALLET_DIR = '%s/.ponypass'
WALLET = '%s/wallet' % WALLET_DIR
GPG_ID = '%s/id' % WALLET_DIR


def gpg_encrypt(data, file):
    id = None
    if not os.path.exists(GPG_ID):
        print('\033[01;34mPlease enter your GPG key ID.\033[00m')
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
            print('\033[01;34mGPG failed, press enter to retry or C-c to abort.\033[00m')
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
            print('\033[01;34mGPG failed, press enter to retry or C-c to abort.\033[00m')
        else:
            return out.decode('utf-8', 'error')


if not os.path.exists(WALLET):
    os.makedirs(WALLET_DIR, exist_ok = True)
    print('\033[01;34mCreating a wallet.\033[00m', file = sys.stderr)
    gpg_encrypt('()\n'.encode('utf-8'), WALLET)
elif not os.path.isfile(WALLET):
    print('%s: %s is not a regular file or link to a regular file' % (sys.argv[0], WALLET), file = sys.stderr)
    sys.exit(1)


print('\033[01;34mLoading wallet.\033[00m', file = sys.stderr)
wallet = eval(gpg_decrypt(WALLET))
passphrase = None
user = None
email = None


if len(sys.argv) == 1:
    (entry, _) = pass ## TODO
    user = entry['user']
    passphrase = entry['pass']
    email = entry['email']
    
elif sys.argv[1] == 'edit':
    (entry, parent) = pass ## TODO
    user = entry['user']
    passphrase = entry['pass']
    email = entry['email']
    print('\033[01;34mUsername (current: %s):\033[00m  ' % user, end = '')
    sys.stdout.flush()
    _user = input()
    if _user != '':
        user = _user
    print('\033[01;34mE-mail (current: %s):\033[00m  ' % email, end = '')
    sys.stdout.flush()
    email = input()
    if _email != '':
        email = _email
    passwordmenu = [{'title' : 'Create random passphrase', 'description' : 'Using correctpony', 'value' : 0},
                    {'title' : 'Create random obscure password', 'description' : 'Not typeable nor fully visible', 'value' : 1},
                    {'title' : 'Enter passphrase manually', 'description' : 'Correctpony will give a suggestion', 'value' : 2}
                    {'title' : 'Do not edit', 'description' : 'Keep the current passphrase', 'value' : -1}]
    (passwordoption, _) = pass ## TODO
    if passwordoption = 0:
        passphrase = correctpony.gensimple()
    elif passwordoption = 1:
        passphrase = obscurepass.genobsure()
    elif passwordoption = 2:
        saved_tty = Popen(['stty', '--save'], stdout=PIPE, stderr=sys.stderr).communicate()[0].decode('utf-8', 'error')[:-1]
        try:
            Popen(['stty', '-echo'], stdin=sys.stdout).wait()
            print('\033[01;34mSuggested passphrase:\033[00m %s' % correctpony.gensimple())
            while True:
                print('\033[01;34mPassphrase:\033[00m  ', end = '')
                sys.stdout.flush()
                passphrase = input()
                print('\033[01;34mRetype passphrase:\033[00m  ', end = '')
                sys.stdout.flush()
                passphrase_re = input()
                if passphrase_re == passphrase:
                    break
                print('\033[01;31mPassphrases did not match eachother!\033[00m')
        finally:
            Popen(['stty', saved_tty], stdin=sys.stdout).wait()
    entry['user'] = user
    entry['pass'] = passphrase
    entry['email'] = email
    (wallet if parent is None else parent['inner']).sort(key = lambda item : item['title'])
    
elif sys.argv[1] == 'delete':
    (entry, parent) = pass ## TODO
    (wallet if parent is None else parent['inner']).remove(entry)
    if (parent is not None) and (len(parent['inner']) == 1):
        entry = parent[0]
        parent['user'] = entry['user']
        parent['pass'] = entry['pass']
        parent['email'] = entry['email']
        del parent['inner']
    
elif sys.argv[1] == 'add':
    print('\033[01;34mSite:\033[00m  ', end = '')
    sys.stdout.flush()
    site = input()
    print('\033[01;34mUsername:\033[00m  ', end = '')
    sys.stdout.flush()
    user = input()
    print('\033[01;34mE-mail:\033[00m  ', end = '')
    sys.stdout.flush()
    email = input()
    passwordmenu = [{'title' : 'Create random passphrase', 'description' : 'Using correctpony', 'value' : 0},
                    {'title' : 'Create random obscure password', 'description' : 'Not typeable nor fully visible', 'value' : 1},
                    {'title' : 'Enter passphrase manually', 'description' : 'Correctpony will give a suggestion', 'value' : 2}]
    (passwordoption, _) = pass ## TODO
    if passwordoption = 0:
        passphrase = correctpony.gensimple()
    elif passwordoption = 1:
        passphrase = obscurepass.genobsure()
    else:
        saved_tty = Popen(['stty', '--save'], stdout=PIPE, stderr=sys.stderr).communicate()[0].decode('utf-8', 'error')[:-1]
        try:
            Popen(['stty', '-echo'], stdin=sys.stdout).wait()
            print('\033[01;34mSuggested passphrase:\033[00m %s' % correctpony.gensimple())
            while True:
                print('\033[01;34mPassphrase:\033[00m  ', end = '')
                sys.stdout.flush()
                passphrase = input()
                print('\033[01;34mRetype passphrase:\033[00m  ', end = '')
                sys.stdout.flush()
                passphrase_re = input()
                if passphrase_re == passphrase:
                    break
                print('\033[01;31mPassphrases did not match eachother!\033[00m')
        finally:
            Popen(['stty', saved_tty], stdin=sys.stdout).wait()
    append_to = wallet
    for entry in wallet:
        if entry['title'] == site:
            if 'inner' in entry:
                append_to = entry['inner']
            else:
                inner = [entry['value']]
                del entry['value']
                entry['inner'] = inner
                append_to = entry['inner']
            break
    append_to.append({'title' : site if append_to is wallet else user,
                      'user' : user, 'pass' : passphrase, 'email' : email})
    append_to.sort(key = lambda item : item['title'])


print('\033[01;34mSaving wallet.\033[00m', file = sys.stderr)
gpg_crypt(str(wallet), WALLET)

if user is not None:
    print('\033[01;34mYour username:\033[00m')
    print(user)
if email is not None:
    print('\033[01;34mYour e-mail:\033[00m')
    print(email)
if passphrase is not None:
    print('\033[01;34mYour passphrase in invisible text:\033[00m')
    print('\033[30;40m%s\033[00;01;33;41mEND\033[00m' % passphrase)

