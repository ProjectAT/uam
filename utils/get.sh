# SVN Checkout Utility -- a part of the UAM project at UofT
# Author: Kenneth Ma (2015), under supervision of Dr. Anya Tafliovich

# Batch checkouts student submissions from a text file containing
# SVN repo URLs.

# Obtained from MarkUs (Assignment Page -> Submissions -> Download Repo List)
# Generally automated with getRepos.sh

echo "Checking out repos from SVN.."

[ $# -ne 4 ] && { echo "Usage: $0 repo-list target assignment-name revision-time"; exit 1; }

# make submissions dir and purge it if it exists
rm -rf "$2/submissions"
mkdir "$2/submissions"

# checkout repos
for repo in `cat "$1"`; do
    echo "Checking out `echo $repo | cut -d',' -f2`/$3.."
    svn co -r {"$4"} "`echo $repo | cut -d',' -f2`/$3" "$2/submissions/`echo $repo | cut -d',' -f1`";

    # remove malformed characters (non-utf8)
    dir="$2/submissions/`echo $repo | cut -d',' -f1`"
    for file in `ls "$dir"`; do
        [ -f "$dir/$file" ] && iconv -f utf-8 -t utf-8 -c "$dir/$file" -o "$dir/$file"
    done
done
