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

import random
import sys
import os
from subprocess import Popen, PIPE



CORRECTPONY_LIST = '/usr/share/correctpony'



'''                                                                                    
Hack to enforce UTF-8 in output (in the future, if you see anypony not using utf-8 in
programs by default, report them to Princess Celestia so she can banish them to the moon)

@param  text:str  The text to print (empty string is default)
@param  end:str   The appendix to the text to print (line breaking is default)
'''
def print(text = '', end = '\n'):
    sys.stdout.buffer.write((str(text) + end).encode('utf-8'))



def gensimple(length = 20, words = 5, lists = []):
    options = [['-j', '-u'], ['-s', ' '], ['-s', '.']]
    params = random.choice(options)
    params += ['-p', '-c', str(length), '-w', str(words)]
    for list in lists:
        params += ['-l', list]
    return Popen(['correctpony'] + params, stdout=PIPE).communicate()[0].decode('utf-8', 'replace')[:-1]


def listsimple():
    return os.listdir(CORRECTPONY_LIST)


if __name__ == '__main__':
    print(listsimple())
    print('\033[30;40m' + gensimple() + '\033[00;01;33;41mEND\033[00m')

