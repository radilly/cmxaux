#!/usr/bin/python3
# @@@
#
# Example usage:
#      ~/cmxaux/walker.py ~/CumulusMXDist3096 ~/CumulusMXDist3097 ~/CumulusMX
#
# This script attempts to support an update from one version of Cumulus MX to a newer one.
# There are 3 directories involved in the process.
#
# A script can be generated using the --script flag which requires a parameter for
# the target platform: "bash" or "dos".  The script should be inspected, particularly
# the lines where a WARNING is given.  It STRONGLY recommended that you do not run
# the script without checking it first.
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
# NOTE:
# NOTE: See if this might be useful to others...
# NOTE: https://cumulus.hosiene.co.uk/ucp.php?i=pm&mode=view&p=26041
# NOTE:
#
# NOTE: https://opensource.com/article/18/8/diffs-patches
#       Could we use patching to copy local updates to an install image??
#
# ----------------------------------------------------------------------------------------
# 20201221 The --script flag was added.  By default this prints a report. The --script
#          requires an argument, either "bash" or "dos".  This causes the report to
#          be issued as a set of comments, with appropriate commands interspersed.
# 20201219 Reorganize walk_tree() to make it a little more efficient by pulling things
#          out of loops where possible.  Added use_merged to walk_tree() to reduce the
#          the run time of this script, especially where there's a lot of historical
#          data.
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
#
# https://stackoverflow.com/questions/16874598/how-do-i-calculate-the-md5-checksum-of-a-file-in-python
#
# https://stackoverflow.com/questions/7585307/how-to-correct-typeerror-unicode-objects-must-be-encoded-before-hashing
#    File "./walker.py", line 14, in compute_md5
#      md5_returned = hashlib.md5(data).hexdigest()
#  TypeError: Unicode-objects must be encoded before hashing
#
# https://stackoverflow.com/questions/19699367/for-line-in-results-in-unicodedecodeerror-utf-8-codec-cant-decode-byte
#    File "/usr/lib/python3.7/codecs.py", line 322, in decode
#      (result, consumed) = self._buffer_decode(data, self.errors, final)
#  UnicodeDecodeError: 'utf-8' codec can't decode byte 0x94 in position 3: invalid start byte
# ----------------------------------------------------------------------------------------
copy = {
	'dos': 'COPY',
	'bash': 'cp -p'
}

remove = {
	'dos': 'DEL',
	'bash': 'rm'
}

comment = {
	'dos': '  REM - ',
	'bash': '  #  '
}

prt_prefix = ""
script_type = "none"

list = []
merged = []

reference = {}
new = {}
installed = {}

script_out = False

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
def add_to_list( list_name, value_str ) :

	if not value_str in list_name :
		list_name.append( value_str )



# ----------------------------------------------------------------------------------------
# Add a member to the dictionary.
#
# This could check that an existing member isn't replaced.
# ----------------------------------------------------------------------------------------
def add_member( dict_name, key_str, value_str ) :

	dict_name[ key_str ] = value_str


# ----------------------------------------------------------------------------------------
# Walk the directory tree to get all the file names.
# The "top" directory is trimed off each file so we can compare different trees.
#
# use_merged is used to avoid getting an MD5 where its not needed. It is fairly
# expensive, and many of the installed files are unique, and generated at runtime.
#
#  https://docs.python.org/3/library/stat.html
#  https://www.tutorialspoint.com/python/os_walk.htm
# ----------------------------------------------------------------------------------------
def walk_tree( base_dir, dict_name, use_merged ) :

	reflength = str(len(base_dir))   # Used by re.sub to trim base_dir off

	for root, dirs, files in os.walk(base_dir, topdown=False):
		short_root = re.sub("^.{" + reflength + "}[\\\/]*", "", root)
		for name in files:
			short_fp = os.path.join(short_root, name)

			if use_merged  and  not short_fp in merged :
				value = ""
			else :
				add_to_list( merged, short_fp )
				filepath = os.path.join(root, name)
				size = os.stat(filepath).st_size
#				mtime = os.stat(filepath).st_mtime
				md5 = compute_md5(filepath)
				value = "{} {}".format( md5, size )

			add_member( dict_name, short_fp, value )
			# NOTE:
			# It is possible for mtime to change but the file to be the same
			# so I removed is the the dictionary vaue.  It was ...
			# add_member( dict_name, short_fp, "{} {} {}".format( md5, size, mtime ), )

#	print( "DEBUG: len(merged) = {}  use_merged = {}".format( len(merged), use_merged ) )


# ----------------------------------------------------------------------------------------
#
# Print out a tree and checksums for a dictional we created for a directory.
#   Used in debugging and testing.
#
# ----------------------------------------------------------------------------------------
def dump_tree( dict_name ) :
	for key in dict_name.keys() :
		prt( "key = \"{}\"  value = \"{}\"".format( key, dict_name[key]) )


# ----------------------------------------------------------------------------------------
#
# Print with a prefir if we're scripting...
#
# ----------------------------------------------------------------------------------------
def prt( text ) :

	print( "{}{}".format( prt_prefix, text ) )

	return

	if script_type == "none" :
		print( "{}{}".format( prt_prefix, text ) )

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
# https://docs.python.org/3/library/argparse.html
# ----------------------------------------------------------------------------------------
parser = argparse.ArgumentParser(description="This assists in updating an existing Cumulus MX installtion.")
parser.add_argument("refdir", help="Path to the directory we will use as the reference version; the installed version as-shipped.")
parser.add_argument("newdir", help="Path to the directory with the new version.")
parser.add_argument("install", help="Path to the installed directory which is to be updated (from the version in refdir).")
parser.add_argument("--script", help="Generate output in script format.", choices=['dos', 'bash'], default="none")
args = parser.parse_args()


script_type = args.script
if script_type == "none" :
	prt( "INFO: script output is off\n" )
else :
	script_out = True
	prt_prefix = comment[ script_type ]

prt( "INFO: script output is set to \"{}\"\n".format(args.script) )

# If we need the "join" character...
sep = os.path.join("x", "x")
sep = re.sub("x", "", sep)


prt( "INFO: Checking refdir  directory {}".format( args.refdir) )
walk_tree( args.refdir, reference, False )

# prt( "Found {} files in directory {}".format( len(reference), args.refdir ) )
### dump_tree( reference )
# DEBUG: prt( "\n\n\n" )

prt( "INFO: Checking newdir  directory {}".format( args.newdir) )
walk_tree( args.newdir, new, False )

# prt( "Found {} files in directory {}".format( len(new), args.newdir ) )
### dump_tree( new )
# DEBUG: prt( "\n\n\n" )

prt( "INFO: Checking install directory {}".format( args.install) )
walk_tree( args.install, installed, True )

print( "\n" )

prt( "INFO: Summary:" )
prt( "INFO: Found {} files in directory {}".format( len(reference), args.refdir ) )
prt( "INFO: Found {} files in directory {}".format( len(new), args.newdir ) )
prt( "INFO: Found {} files in directory {}".format( len(installed), args.install ) )
prt( "INFO: Accumulated MD5 checksums for {} files".format( len(merged) ) )


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
prt( "INFO: Analysis:\n" )


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
#		prt( "DEBUG: Deleted file {}".format( key ) )


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Summarize the analysis
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
prt( "INFO: Files in directory {} = {}".format( args.newdir, len(new) ) )
prt( "INFO: Files same between refdir and newdir = {}".format( len(same) ) )
prt( "INFO: Files changed between refdir and newdir = {}".format( len(changed) ) )
prt( "INFO: Files added between refdir and newdir = {}".format( len(added) ) )
prt( "DEBUG: Check: {} - {} - {} - {} = {}\n\n".format( len(new), len(same), len(changed), len(added), len(new) - len(same) - len(changed) - len(added) ) )
# prt( "DEBUG: check = {}".format( len(new) - len(same) - len(changed) - len(added) ) )


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Summarize the analysis
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
prt( "INFO: Files missing from install relative to refdir = {}".format( len(missing) ) )
prt( "INFO: These will have to be investigated.  This is unusual and potentially problematic." )
for filename in missing :
	prt( "          {}".format( filename ) )


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Print the lists we compiled above.
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
print( "\n" )
prt( "INFO: Files modified in install relative to refdir = {}".format( len(local_mod) ) )
prt( "INFO: These will have to be inspected / compared." )
for filename in local_mod :
	prt( "          {}".format( filename ) )
	prt( "          *  {}".format( os.path.join( args.refdir, filename ) ) )
	prt( "          *  {}\n".format( os.path.join( args.install, filename ) ) )


print( "\n" )
prt( "INFO: Files changed between refdir and newdir = {}".format( len(changed) ) )
prt( "INFO: These *potentially* might be replaced in install. Check for WARNINGs." )
for filename in changed :
	prt( "          {}".format( filename ) )
	if filename in local_mod :
		prt( "WARNING:          {} was modified in install\n".format( filename ) )
	else :
		if script_out :
			print( "{} {} {}".format( copy[script_type], os.path.join( args.newdir, filename ),
				os.path.join( args.install, filename ) ) )


print( "\n" )
prt( "INFO: Files added between refdir and newdir = {}".format( len(added) ) )
prt( "INFO: These *potentially* may be copied in install, if they don't already exist (unusual)." )
for filename in added :
	prt( "          {}".format( filename ) )
	if filename in installed.keys() :
		prt( "WARNING:          {} already exists in install".format( filename ) )
		if filename in local_mod :
			prt( "WARNING:          {} was also modified in install".format( filename ) )
		print( "" )
	else :
		if script_out :
			print( "{} {} {}".format( copy[script_type], os.path.join( args.newdir, filename ),
				os.path.join( args.install, filename ) ) )



print( "\n" )
prt( "INFO: Files deleted in newdir = {}".format( len(deleted) ) )
prt( "INFO: These *potentially* may be deleted from install.  Verify that they are not referenced by anything." )
for filename in deleted :
	prt( "          {}".format( filename ) )
	if filename in installed.keys() :
		if script_out :
			print( "{} {}".format( remove[script_type], os.path.join( args.install, filename ) ) )
	else :
		prt( "WARNING:          {} does NOT exist in install\n".format( filename ) )


print( "\n" )

prt( "INFO: Summary:" )
prt( "INFO: Files modified in install relative to refdir = {}".format( len(local_mod) ) )
prt( "INFO: Files changed between refdir and newdir = {}".format( len(changed) ) )
prt( "INFO: Files added between refdir and newdir = {}".format( len(added) ) )
prt( "INFO: Files deleted in newdir = {}".format( len(deleted) ) )


print( "\n" )
if script_type == "none" :
	prt( "INFO: script output is off" )
else :
	prt( "DEBUG: copy command = {}".format( copy[ script_type ] ) )
	prt( "DEBUG: remove command = {}".format( remove[ script_type ] ) )

exit()



