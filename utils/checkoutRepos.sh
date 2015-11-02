# usage: ./checkoutRepos.sh repolistfile [dir [timestamp]]
# Provided the name of an appropriate text file, checks out all svn repositories
# that can be found in the following format:
#
# username1,svnrepourl1
# username2,svnrepourl2
#
# Intended for use with text files provided by MarkUs with the name:
#  package_svn_repo_list.txt
# however any similarly formatted text file should do
# dir is normally the name of an assignment, aka the directory in the
#     submissions structure that corresponds to an assignment
# timestamp is in the  ISO 8601 format  YYYY-MM-DD HH:MM
# NOTE: Unsure of behaviour if any information is required to access a repo

URL=http://markus.utsc.utoronto.ca/svn/cscb07f15/ # checkout from
TARGETDIR=/home/anya/b07/submissions              # checkout to

if [ $# -eq 0 ]; then
    echo Usage: $0 repolistfile [dir [timestamp]]
    exit 1
fi

repolistfile=$1

if [ $# -gt 1 ]; then
    dir=$2
else
    dir=""
fi

if [ $# -gt 2 ]; then
    timestamp=\{$3\}
else
    timestamp=HEAD
fi

for svnrepo in `awk -F'/' '{print $(NF)}' $repolistfile`; do
  pushd $TARGETDIR
  if [ -d "$svnrepo" ]; then
      pushd $svnrepo
      svn up -r "$timestamp" $dir
      popd
  else
      svn co $URL/$svnrepo
  fi
  popd
done
