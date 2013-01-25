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


UNICODE_VERSION=6.2.0

unicode:
	mkdir -p res
	if [ -f PropList.txt ]; then rm PropList.txt; fi
	wget 'http://www.unicode.org/Public/$(UNICODE_VERSION)/ucd/PropList.txt'
	grep -v '^$$' < PropList.txt | grep -v '^#' | sed -e 's_#_;_g' | cut -d ';' -f 1,3 > glyphs~
	i=0; while (( $$i < 10 )); do sed -i 's_  _ _g' glyphs~; (( i++ )); done
	sed -e 's_ ; _ _g' < glyphs~ | cut -d ' ' -f 1,2 > glyphs
	grep -v ' Mn$$' < glyphs | grep -v ' Z.$$' | grep -v ' C.$$' > glyphs~
	grep -v '^...... ..$$' < glyphs~ | grep -v '^......\.\....... ..$$' > glyphs
	grep -v '^..... ..$$' < glyphs | grep -v '^.....\.\...... ..$$' > glyphs~
	grep -v '^.....\.\....... ..$$' < glyphs~ | cut -d ' ' -f 1 > glyphs
	mv glyphs res
	rm PropList.txt glyphs~

.PHONY: clean
clean:
	rm PropList.txt glyphs~ glyphs res/glyphs || exit 0

