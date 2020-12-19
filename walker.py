#!/usr/bin/python3
#
# Example usage:
#      ~/cmxaux/walker.py ~/CumulusMXDist3096 ~/CumulusMXDist3097 ~/CumulusMX
#
# This script attempts to support an update from one version of Cumulus MX to a newer one.
# There are 3 directories involved in the process.
#
# There is a reference directory (refdir) which is the build as-shipped that is currently
# installed.  The installed directory (install) includes generated files specific to the
# installation, produced as CMX is running.  These will not have been in the distribution.
# However, everthing in reference directory should also be found in the installation.
# It is possible some of the shipped files were modified in the installed directory.
#
# The remaining directory is the new build as-shipped (newdir), presummably one wishes to
# update the installation to.  The differences between the reference and new builds
# informs how the installation needs to be altered.
#
# refdir - Path to the directory we will use as the reference version; the installed version.
# newdir - Path to the directory with the new version.
# install - Path to the installed directory which is to be updated.
#
# ----------------------------------------------------------------------------------------
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
# 20201218 RAD Reasonably working first cut.
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
# Get the MD5 checksum for a file.
#
# https://www.geeksforgeeks.org/python-check-whether-given-key-already-exists-in-a-dictionary/
#
# ----------------------------------------------------------------------------------------
def compute_md5( file_name ) :

	# Open,close, read file and calculate MD5 on its contents 
	with open(file_name,"r",encoding='ISO-8859-1') as file_to_check :
		# read contents of the file
#		data = file_to_check.read().encode('utf-8')
		data = file_to_check.read().encode('ISO-8859-1')
		# pipe contents of the file through
		md5_returned = hashlib.md5(data).hexdigest()
		return( hashlib.md5(data).hexdigest() )



# ----------------------------------------------------------------------------------------
# Add a member to the dictionary.
#
# This could check that an existing member isn't replaced.
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
			add_member( dict_name, short_fp, "{} {}".format( md5, size ), )
			# NOTE:
			# It is possible for mtime to change but the file to be the same.
			# add_member( dict_name, short_fp, "{} {} {}".format( md5, size, mtime ), )


# ----------------------------------------------------------------------------------------
#
# Print out a tree and checksums for a dictional we created for a directory.
#   Used in debugging and testing.
#
# ----------------------------------------------------------------------------------------
def dump_tree( dict_name ) :
	for key in dict_name.keys() :
		print( "key = \"{}\"  value = \"{}\"".format( key, dict_name[key]) )


# ----------------------------------------------------------------------------------------
#
# Consider an optn to output DOS or BASH...?
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
parser.add_argument("refdir", help="Path to the directory we will use as the reference version; the installed version.")
parser.add_argument("newdir", help="Path to the directory with the new version.")
parser.add_argument("install", help="Path to the installed directory which is to be updated.")
## parser.add_argument("--html", help="Output in HTML", action="store_true")
args = parser.parse_args()
#	if args.html:
#		print "html turned on"
## if not args.html:
##	print( "\n\n\n\n\n" )

## use_html = args.html

print( "INFO: Checking refdir  directory {}".format( args.refdir) )
walk_tree( args.refdir, reference )

# print( "Found {} files in directory {}".format( len(reference), args.refdir ) )
### dump_tree( reference )
# DEBUG: print( "\n\n\n" )

print( "INFO: Checking newdir  directory {}".format( args.newdir) )
walk_tree( args.newdir, new )

# print( "Found {} files in directory {}".format( len(new), args.newdir ) )
### dump_tree( new )
# DEBUG: print( "\n\n\n" )

print( "INFO: Checking install directory {}".format( args.install) )
walk_tree( args.install, installed )

print( "\n" )

print( "Found {} files in directory {}".format( len(reference), args.refdir ) )
print( "Found {} files in directory {}".format( len(new), args.newdir ) )
print( "Found {} files in directory {}".format( len(installed), args.install ) )


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Compare these lists to determine what actions are required.
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
local_mod = []
missing = []
same = []
changed = []
added = []
deleted = []


print( "\n" )
print( "INFO: Analysis:\n" )


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# See if anything was modified from the files in the 'reference" directory in the
#   'installed' copy.
#
# These probably have to be looked at by hand... and should not be overlayedi blindly.
#   There is a patching facility in Linux, but I've never used it.
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
for key in reference.keys() :
	if key in installed.keys() :
		if installed[key] != reference[key] :
			local_mod.append( key )
	else :
		missing.append( key )



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Compare files in the 'newdir' with those in 'refdir' which are either:
#    identical
#    changed
#    added
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
for key in new.keys() :
	if key in reference.keys() :
		if new[key] == reference[key] :
			same.append( key )
		else :
			changed.append( key )
	else :
		added.append( key )


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Compare files in the 'refdir' with those in 'newdir'.  If not found in 'newdir'
# it was deleted in in the 'newdir' buid.
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
for key in reference.keys() :
	if not key in new.keys() :
		deleted.append( key )
#		print( "DEBUG: Deleted file {}".format( key ) )

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Summarize the analysis
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
print( "INFO: Files in directory {} = {}".format( args.newdir, len(new) ) )
print( "INFO: Files same between refdir and newdir = {}".format( len(same) ) )
print( "INFO: Files changed between refdir and newdir = {}".format( len(changed) ) )
print( "INFO: Files added between refdir and newdir = {}".format( len(added) ) )
print( "DEBUG: Check: {} - {} - {} - {} = {}\n\n".format( len(new), len(same), len(changed), len(added), len(new) - len(same) - len(changed) - len(added) ) )
# print( "DEBUG: check = {}".format( len(new) - len(same) - len(changed) - len(added) ) )




# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Summarize the analysis
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
print( "INFO: Files missing from install relative to refdir = {}".format( len(missing) ) )
print( "INFO: These will have to be investigated.  This is unusual and potentially problematic." )
for filename in missing :
	print( "          {}".format( filename ) )



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Print the lists we compiled above.
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
print( "\n" )
print( "INFO: Files modified in install relative to refdir = {}".format( len(local_mod) ) )
print( "INFO: These will have to be inspected / compared." )
for filename in local_mod :
	print( "          {}".format( filename ) )
	print( "          *  {}".format( os.path.join( args.refdir, filename ) ) )
	print( "          *  {}\n".format( os.path.join( args.install, filename ) ) )



print( "\n" )
print( "INFO: Files changed between refdir and newdir = {}".format( len(changed) ) )
print( "INFO: These *potentially* might be replaced in install. Check for WARNINGs." )
for filename in changed :
	print( "          {}".format( filename ) )
	if filename in local_mod :
		print( "WARNING:          {} was modified in install".format( filename ) )


print( "\n" )
print( "INFO: Files added between refdir and newdir = {}".format( len(added) ) )
print( "INFO: These *potentially* may be copied in install, if they don't already exist (unusual)." )
for filename in added :
	print( "          {}".format( filename ) )
	if filename in installed.keys() :
		print( "WARNING:          {} already exists in install".format( filename ) )
		if filename in local_mod :
			print( "WARNING:          {} was also modified in install".format( filename ) )


print( "\n" )
print( "INFO: Files deleted in newdir = {}".format( len(deleted) ) )
print( "INFO: These *potentially* may be deleted from install.  Verify that are not referenced by anything." )
for filename in deleted :
	print( "          {}".format( filename ) )


print( "" )



exit()



