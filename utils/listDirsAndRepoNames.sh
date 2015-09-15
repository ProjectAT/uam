# usage: ./listDirsAndRepoNames.sh dirpathfile
# Provided a file with a list of directories to be graded, produce output
# in the following format:
#
#  dipath,repo_name
# 
# Not really for general use.

if [ $# -ne 1 ]; then
    echo Usage: $0 dirpathfile
    exit 1
fi

dirpathfile=$1

for dirpath in `cat $dirpathfile`
do
    reponame=`echo $dirpath | awk -F/ '{print $2}'`
    echo $dirpath,$reponame
done
