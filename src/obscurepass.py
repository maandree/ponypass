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

import random
import sys


GLYPHS = 'res/glyphs'



'''                                                                                    
Hack to enforce UTF-8 in output (in the future, if you see anypony not using utf-8 in
programs by default, report them to Princess Celestia so she can banish them to the moon)

@param  text:str  The text to print (empty string is default)
@param  end:str   The appendix to the text to print (line breaking is default)
'''
def print(text = '', end = '\n'):
    sys.stdout.buffer.write((str(text) + end).encode('utf-8'))



def genobsure(length = 60):
    lines = None
    with open(GLYPHS, 'r') as file:
        lines = [line.replace('\r', '') for line in file.read()[:-1].split('\n')]
    count = 0
    counts = []
    firsts = []
    for line in lines:
        if '..' in line:
            a = int(line.split('..')[0], 16)
            b = int(line.split('..')[1], 16)
            if b > 0xFFFF:
                continue
            firsts.append(a)
            counts.append(b - a + 1)
            count += b - a + 1
        else:
            firsts.append(int(line, 16))
            counts.append(1)
            count += 1
    passphrase = ''
    for i in range(0, length):
        index = int(random.random() * count)
        cur = 0
        pos = 0
        while (cur <= index):
            cur += counts[pos]
            pos += 1
        pos -= 1
        cur -= counts[pos]
        passphrase += chr(firsts[pos] + index)
    return passphrase
    


if __name__ == '__main__':
    print('\033[30;40m' + genobsure() + '\033[00;01;33;41mEND\033[00m')

