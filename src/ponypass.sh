#!/bin/sh

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


tempmount="/dev/shm"
id=$(cat "${HOME}/.ponypass/id")
wallet="${HOME}/.ponypass/wallet"
temp="${tempmount}/.$(uuidgen)-$(uuidgen)"

if [ ! "$(df -l -P -t tmpfs | grep -- "${tempmount}" | wc -l)" = "1" ]; then
    echo -e '\e[01;31m/dev/shm is not a tmpfs.\e[00m' 1>&2
    exit 10
fi

if [ ! -f "$wallet" ]; then
    echo -e '\e[01;34mCreating a wallet.\e[00m' 1>&2
    echo wallet | gpg --sign --local-user "$id" --encrypt --recipient "$id" > "$wallet" ||
        (rm -- "$wallet" ; exit 1)
fi

function _shred
{
    # but please also use disc encryption, such as LUKS
    shred --force --iterations=20 --zero --remove -- "$1"
}

if [ -f "$temp" ]; then
    _shred "$temp"
fi

rc=1

touch "$temp" &&
    chmod 600 "$temp" &&
    echo -e '\e[01;34mLoading wallet.\e[00m' 1>&2 &&
    gpg --decrypt < "$wallet" > "$temp" &&
    echo -e '\e[01;34mSaving wallet.\e[00m' 1>&2 &&
    gpg --sign --local-user "$id" --encrypt --recipient "$id" < "$temp" > "${wallet}.new" &&
    mv -- "${wallet}.new" "$wallet"

rc=$?

if [ -f "$temp" ]; then
    _shred "$temp"
fi

if [ -f "${wallet}.new" ]; then
    rm -- "${wallet}.new"
fi

exit $rc

