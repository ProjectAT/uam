# usage: ./listDirs.sh repolistfile asst
# Provided the name of an appropriate text file of all svn repositories,
# print out a list of directories to be graded. Intended for use with 
# pam. asst is the assignment to be graded.
#
# The repolist file must ne in the following format:
#
# username1,svnrepourl1
# username2,svnrepourl2
#
# Intended for use with text files provided by MarkUs with the name:
#  package_svn_repo_list.txt
# however any similarly formatted text file should do
# dir is normally the name of an assignment, aka the directory in the
#     submissions structure that corresponds to an assignment
# 

if [ $# -ne 2 ]; then
    echo Usage: $0 repolistfile asst
    exit 1
fi

repolistfile=$1
asst=$2

for svnrepo in `awk -F'/' '{print $(NF)}' $repolistfile`; do
  echo submissions/$svnrepo/$asst
done
