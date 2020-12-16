#!/usr/bin/python3
#
# Example usage:
#      ~/cmxaux/walker.py ~/CumulusMXDist3096 ~/CumulusMXDist3097 ~/CumulusMX
#
#
# NOTE:
# NOTE: See if this might be useful to others...
# NOTE: https://cumulus.hosiene.co.uk/ucp.php?i=pm&mode=view&p=26041
# NOTE:
#
# NOTE: https://opensource.com/article/18/8/diffs-patches
#       Could we use patching to copy local updates to an install image??
#
# https://www.tutorialspoint.com/python/os_walk.htm
# ----------------------------------------------------------------------------------------
#
#
# ----------------------------------------------------------------------------------------
import os
import hashlib
import stat
import argparse
import re

# ----------------------------------------------------------------------------------------
# https://stackoverflow.com/questions/46605842/executing-bashs-complex-find-command-in-python-shell
# os.walk()

# https://stackoverflow.com/questions/16874598/how-do-i-calculate-the-md5-checksum-of-a-file-in-python

# https://stackoverflow.com/questions/7585307/how-to-correct-typeerror-unicode-objects-must-be-encoded-before-hashing
#    File "./walker.py", line 14, in compute_md5
#      md5_returned = hashlib.md5(data).hexdigest()
#  TypeError: Unicode-objects must be encoded before hashing



# https://stackoverflow.com/questions/19699367/for-line-in-results-in-unicodedecodeerror-utf-8-codec-cant-decode-byte
#    File "/usr/lib/python3.7/codecs.py", line 322, in decode
#      (result, consumed) = self._buffer_decode(data, self.errors, final)
#  UnicodeDecodeError: 'utf-8' codec can't decode byte 0x94 in position 3: invalid start byte
# ----------------------------------------------------------------------------------------

list = []

reference = {}
new = {}
installed = {}


# ----------------------------------------------------------------------------------------
#
# https://www.geeksforgeeks.org/python-check-whether-given-key-already-exists-in-a-dictionary/
#
#
#
#
#
# ----------------------------------------------------------------------------------------

def compute_md5( file_name ):

	# Open,close, read file and calculate MD5 on its contents 
#	with open(file_name,"r",encoding='utf-8') as file_to_check:
	with open(file_name,"r",encoding='ISO-8859-1') as file_to_check:
		# read contents of the file
#		data = file_to_check.read().encode('utf-8')
		data = file_to_check.read().encode('ISO-8859-1')
		# pipe contents of the file through
		md5_returned = hashlib.md5(data).hexdigest()
		return( hashlib.md5(data).hexdigest() )



# ----------------------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------------------
def add_member( dict_name, key_str, value_str ) :

	dict_name[ key_str ] = value_str


# ----------------------------------------------------------------------------------------
#
#
#  https://docs.python.org/3/library/stat.html
# ----------------------------------------------------------------------------------------
def walk_tree( base_dir, dict_name ) :
	reflength = str(len(base_dir) + 1)

	for root, dirs, files in os.walk(base_dir, topdown=False):
###		print( "DEBUG: dir {}".format( root ) )
		for name in files:
			filepath = os.path.join(root, name)
			size = os.stat(filepath).st_size
			mtime = os.stat(filepath).st_mtime
			md5 = compute_md5(filepath)

			if len(root) - len(base_dir) > 0 :
				short_fp = os.path.join( re.sub("^.{" + reflength + "}", "", root), name )
			else :
				short_fp = name

###			print( "DEBUG: {} {} {}".format( short_fp, md5, size ) )
			add_member( dict_name, short_fp, "{} {} {}".format( md5, size, mtime ), )


# ----------------------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------------------
def dump_tree( dict_name ) :
	for key in dict_name.keys() :
		print( "key = \"{}\"  value = \"{}\"".format( key, dict_name[key]) )


# ----------------------------------------------------------------------------------------
#
# Option to output HTML???
#   https://docs.python.org/2/howto/argparse.html
#   http://zetcode.com/python/argparse/
#
# Maybe DOS vs BASH...?
#
# ----------------------------------------------------------------------------------------
# refdir
# - Every file in here should be in 'install'. It may be modified.
#
# newdir
# - Files in here, but not in 'refdir' (or 'install') need to be copied in; new files.
#      It is possible but unlikely, but if in 'install' diffs need to be examined.
# - Any file in 'refdir' but not here were removed, and can be deleted from 'install'.
#
# install
# - Any files not in 'refdir' are generated or local additions, and should not touched.
# - Files here which were modified from refdir need to be protected.
#      These probably need to examimed manually.
#
# ----------------------------------------------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument("refdir", help="Path to the directory we will use as the reference version.")
parser.add_argument("newdir", help="Path to the directory with the new version.")
parser.add_argument("install", help="Path to the installed directory to be updated.")
## parser.add_argument("--html", help="Output in HTML", action="store_true")
args = parser.parse_args()
#	if args.html:
#		print "html turned on"
## if not args.html:
##	print( "\n\n\n\n\n" )

## use_html = args.html

print( "INFO: Checking direcotry {}".format( args.refdir) )
walk_tree( args.refdir, reference )

print( "Found {} files in directory {}".format( len(reference), args.refdir ) )

dump_tree( reference )

print( "\n\n\n\n\n" )

print( "INFO: Checking direcotry {}".format( args.newdir) )
walk_tree( args.newdir, new )

print( "Found {} files in directory {}".format( len(new), args.newdir ) )

dump_tree( new )

print( "\n\n\n\n\n" )

print( "INFO: Checking direcotry {}".format( args.install) )
walk_tree( args.install, installed )

print( "\n\n\n\n\n" )

print( "Found {} files in directory {}".format( len(reference), args.refdir ) )
print( "Found {} files in directory {}".format( len(new), args.newdir ) )
print( "Found {} files in directory {}".format( len(installed), args.install ) )

exit()



