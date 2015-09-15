# usage: ./commitRepos.sh repolistfile "Message" [dir]
# Provided the name of an appropriate text file and a commit message, commits
# changes to all directories within the submissions directory that are checked
# out svn repos and are named in the file.
#
# username1,svnrepourl1
# username2,svnrepourl2
#
# Intended for use with text files provided by MarkUs with the name:
#  package_svn_repo_list.txt
# however any similarly formatted text file should do
# NOTE: Unsure of behaviour if any information is required to access a repo
# WARNING: Possibly undefined behaviour in the event of conflicts

if [ $# -lt 2 ]; then
    echo Usage: commitRepos.sh repolistfile \"message\" [dir [newfile1 newfile2 ...]]
    exit 1
fi

repolistfile=$1
message=$2

if [ $# -gt 2 ]; then
    dir=$3
else
    dir=""
fi

if [ $# -gt 3 ]; then
    svnadd=true
else
    svnadd=false
fi

for svnrepo in `awk -F'/' '{print $(NF)}' $repolistfile`; do
  echo Processing $svnrepo/$dir...  
  pushd submissions/$svnrepo/$dir
  if [ $svnadd = true ] ; then
      svn --force add "${@:4}"
  fi
  svn commit -m "$message"
  popd
done

