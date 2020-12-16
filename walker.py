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
# ----------------------------------------------------------------------------------------
def walk_tree( base_dir, dict_name ) :
	reflength = str(len(base_dir) + 1)

	for root, dirs, files in os.walk(base_dir, topdown=False):
###		print( "DEBUG: dir {}".format( root ) )
		for name in files:
			filepath = os.path.join(root, name)
			size = os.stat(filepath).st_size
			md5 = compute_md5(filepath)

			if len(root) - len(base_dir) > 0 :
				short_fp = os.path.join( re.sub("^.{" + reflength + "}", "", root), name )
			else :
				short_fp = name

###			print( "DEBUG: {} {} {}".format( short_fp, md5, size ) )
			add_member( dict_name, short_fp, "{} {}".format( md5, size ), )


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

print( "\n\n\n\n\n" )

walk_tree( args.refdir, reference )

print( "Found {} files in directory {}.".format( len(reference), args.refdir ) )

dump_tree( reference )

print( "\n\n\n\n\n" )

walk_tree( args.newdir, new )

print( "Found {} files in directory {}.".format( len(new), args.newdir ) )

dump_tree( new )

print( "\n\n\n\n\n" )

walk_tree( args.install, installed )


print( "Found {} files in directory {}.".format( len(reference), args.refdir ) )
print( "Found {} files in directory {}.".format( len(new), args.newdir ) )
print( "Found {} files in directory {}.".format( len(installed), args.install ) )

exit()
exit()
exit()
exit()
exit()
exit()
exit()


reflength = str(len(args.refdir) + 1)

for root, dirs, files in os.walk(args.refdir, topdown=False):
	print( "# dir {}".format( root ) )
	for name in files:
		filepath = os.path.join(root, name)
#		size = filepath.stat().st_size
		size = os.stat(filepath).st_size
		md5 = compute_md5(filepath)
#		print( "DEBUG: {} {} {}".format( filepath, md5, size ) )
# @@@
		if len(root) - len(args.refdir) > 0 :
			short_fp = os.path.join( re.sub("^.{" + reflength + "}", "", root), name )
		else :
			short_fp = name

#		print( "DEBUG: root = {}   name = {}   short_fp = {}".format( re.sub("^.{" + reflength + "}", "", root), name, short_fp ) )

		print( "{} {} {}".format( short_fp, md5, size ) )
		list.append( "{} {} {}".format( short_fp, md5, size ) )
# @@@		reference[ short_fp ] = "{} {}".format( md5, size )
		add_member( reference, short_fp, "{} {}".format( md5, size ), )
#		print( "{} | {} | {}".format( filepath, compute_md5(filepath), size ) )

#		print( compute_md5( os.path.join(root, name)) )

	print( "Found {} files.".format( len(list) ) )

	print( reference )

exit()



import os

for root, dirs, files in os.walk(".", topdown=False):
	for name in files:
		print( "file: {}".format( os.path.join(root, name)) )

	for name in dirs:
#      print(os.path.join(root, name))
		print( "dir: {}".format( os.path.join(root, name)) )


	exit()

#   cd ~/webcamwatcher/
#   grep '/home/' *
#   grep -n '/home/' *
#   grep -l '/home/' *
#   grep -l '/home/pi/' *
#   grep -l '/home/pi/' * | xargs ls -altr
#   ttttt
#   wxstatus
#   cd
#   cd webcamwatcher/
#   ls *sh
#   ls -altr *sh
#   cd
#   ls -altr *sh
#   vi UPDATER.sh 
#   find . -name '*sh' -ls
#   vi ./interface_mods/scanner.sh
#   ls -altr
#   vi 3096_changes.txt 
#   vi CumulusMXDist3095_diffs.txt
#   diff -rq  CumulusMXDist3096 CumulusMX
#   ls -al tr */Updates*
#   ls -al tr */Updates.txt
#   cksum */Updates.txt
#   cp -p CumulusMXDist3096/Updates.txt CumulusMX
#   cksum */Updates.txt
#   diff -rq  CumulusMXDist3096 CumulusMX
#   diff -rq  CumulusMXDist3096 CumulusMX | sed 's/:*//'
#   diff -rq  CumulusMXDist3096 CumulusMX | sed 's/:.*//' | sort | uniq
#   diff -rq  CumulusMXDist3096 CumulusMX | grep CumulusMXDist3096
#   less CumulusMXDist3096/Updates_RAD.txt
#   diff -rq CumulusMXDist3097 CumulusMXDist3096
#   diff -rq CumulusMXDist3097 CumulusMXDist3096 | sed 's/Files /Files   /'
#   diff -rq CumulusMXDist3097 CumulusMXDist3096 | sed 's/Files /Files   /' | sort
#   diff -rq CumulusMXDist3097 CumulusMXDist3096 | sed 's/Files /Files   /' | sort | grep 3096
#   ls -altr webcamwatcher/*.py
#   ls ~/webcamwatcher/walker.py
#   cd CumulusMXDist3097
#   ~/webcamwatcher/walker.py
#   diff -rq CumulusMXDist3097 CumulusMXDist3096 | sed 's/Files /Files   /' | sort | grep 3096
#   diff -rq ~/CumulusMXDist3097 ~/CumulusMXDist3096 | sed 's/Files /Files   /' | sort | grep 3096
#   cd
#   diff -rq CumulusMXDist3097 CumulusMXDist3096 | sed 's/Files /Files   /' | sort | grep 3096
#   diff -rq CumulusMXDist3097 CumulusMXDist3096 | sed 's/Files /Files   /' | sort | cut -c 8-
#   diff -rq CumulusMXDist3097 CumulusMXDist3096 | sed 's/Files /Files   /' | sort | cut -c 9-
#   diff -rq CumulusMXDist3097 CumulusMXDist3096 | sed 's/Files /Files   /' | sort | cut -c 9- | sed 's/ and .* differ/ differ/'
#   diff -rq CumulusMXDist3097 CumulusMXDist3096 | sed 's/Files /Files   /' | sort | cut -c 9- | sed 's/ and .* differ//'
#   diff -rq CumulusMXDist3097 CumulusMXDist3096 | sed 's/Files /Files   /' | sort | cut -c 9- | sed 's/ and .* differ//' | xargs -i dirname {}
#   diff -rq CumulusMXDist3097 CumulusMXDist3096 | sed 's/Files /Files   /' | sort | cut -c 9- | sed 's/ and .* differ//' | xargs -i dirname {} | sort
#   diff -rq CumulusMXDist3097 CumulusMXDist3096 | sed 's/Files /Files   /' | sort | cut -c 9- | sed 's/ and .* differ//' | xargs -i dirname {} | sort | uniq
#   ls -altr
#   diff -rq CumulusMXDist3097 CumulusMXDist3096 | sed 's/Files /Files   /' | sort | cut -c 9- | sed 's/ and .* differ//' | xargs -i dirname {} | sort | uniq
#   cd webcamwatcher/
#   ls -latr | tail
#   history | tail -n 55 >> walker.py 
