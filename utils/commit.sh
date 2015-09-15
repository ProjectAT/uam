# SVN Committer -- a part of the UAM project at UofT
# Author: Kenneth Ma (2015), under supervision of Dr. Anya Tafliovich

# Adds and commits the specified file in each of the folders in submission-dir.
# Overwrites whatever file was in the repo if it exists already.

[ $# -ne 4 ] && { echo "Usage: $0 submission-dir repo-list assignment-name report-name" 1>&2; exit 1; }

echo "Committing $4 back to student folders.."

for student in $( awk -F'/' '{print $(NF)}' $2 ); do
    echo "adding $student - $4"
    svn add "$1/$student/$3/$4"
    svn ci -m "" "$1/$student/$3/$4"

    # report already exists if commit failed.. so we want to overwrite
    [ $? -eq 1 ] && { svn up "$1/$student/$3/$4" --accept mine-conflict; \
        svn ci -m "" "$1/$student/$3/$4"; }
done
