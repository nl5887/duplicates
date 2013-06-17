#!/usr/bin/env python
#
# duplicates.py
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA  02111-1307  USA

# https://github.com/nl5887/duplicates

import sys
import fnmatch

import os
import hashlib
import binascii
import struct
import zlib
import argparse

from collections import defaultdict

def md5sum(filename):
    md5 = hashlib.md5()
    with open(filename,'rb') as f: 
        for chunk in iter(lambda: f.read(128*md5.block_size), b''): 
             md5.update(chunk)
	     
    return md5.digest()

def main(argv):
    parser = argparse.ArgumentParser(
	prog='duplicates',
	description='Duplicates finds duplicate files in multiple directories.',
	formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('directories', nargs='+', help='')
    args = parser.parse_args()
    
    d = defaultdict(list)
    
    for directory in args.directories:
	for root, dirnames, filenames in os.walk(directory):
		for filename in fnmatch.filter(filenames, '*'):
			hash = binascii.hexlify(md5sum(os.path.join(root, filename)))	
			d[hash].append(os.path.join(root, filename))
    
    for k, v in d.iteritems():
	    if (len(v)>1):
		print ("{0} {1}".format(k, tuple(v)))
	    
if __name__ == "__main__":
    main(sys.argv)