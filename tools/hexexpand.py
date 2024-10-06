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


lines = None
with open('/dev/stdin', 'r') as file:
    lines = [line.replace('\r', '') for line in file.read()[:-1].split('\n')]
for line in lines:
    if '..' in line:
        a = int(line.split('..')[0], 16)
        b = int(line.split('..')[1], 16)
        for i in range(a, b + 1):
            s = hex(i).upper()[2:]
            while len(s) < 4:
                s = '0' + s
            print(s)
    else:
        print(line)

