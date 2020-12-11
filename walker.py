#!/usr/bin/python3

# https://www.tutorialspoint.com/python/os_walk.htm
import os
import hashlib
import stat

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



for root, dirs, files in os.walk(".", topdown=False):
	print( "# dir {}".format( root ) )
	for name in files:
		filepath = os.path.join(root, name)
#		size = filepath.stat().st_size
		size = os.stat(filepath).st_size
		print( "{} {} {}".format( filepath, compute_md5(filepath), size ) )
#		print( "{} | {} | {}".format( filepath, compute_md5(filepath), size ) )

#		print( compute_md5( os.path.join(root, name)) )


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
