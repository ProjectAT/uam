# UAM Combined Grader -- a part of the UAM project at UofT
# Author: Kenneth Ma (2015), under supervision of Dr. Anya Tafliovich

# Grades a specified assignment rooted under submissions_dir and
# provides an aggregated report file in this directory named
# the specified report-name (along with individual reports).

# Also retrieves repo lists and checks out SVN repos if required.
# revision-time is the ISO-8601 standard (ie, 2015-05-01T00:00)

# If SVN retrieval is not specified, the grader will attempt to
# grade and aggregate all submissions in the
# course-dir/assignment-name/submissions folder, which requires
# groups.txt in the course-dir/assignment-name folder (or will
# crash).. as it's unable to match up Students to submissions

# REQ: course-dir/assignment-name contains groups.txt (containing
# Group->Student links)

# REQ: course-dir is a relative path

[ $# -lt 4 ] && { echo \
    "Usage: $0 report-name course-dir assignment-name student-list"\
    "[revision-time markus-username markus-password markus-assignment-number"\
    "commit]" 1>&2; exit 1; }

# path to assignment submissions and UAM folder
submissions_dir="$2/$3/submissions"
uam_dir=$(dirname $0)

# set permissions to uam scripts
chmod +x "$uam_dir/get.sh" "$uam_dir/commit.sh" "$uam_dir/getRepos.sh"

# if svn retrieval is required
[ -n "$5" ] && { "$uam_dir/getRepos.sh" "$6" "$7" "$8" "$2/$3"; \
    "$uam_dir/get.sh" "$2/$3/repos.txt" "$2/$3" "$3" "$5"; }

# generate a listing of all student directories
ls "$submissions_dir" | sed "s:^:$submissions_dir/:" >directories.txt

# run test_runner.py
echo "Grading submissions.."
/usr/local/cms/python-3.4.2/bin/python3.4 "$uam_dir/test_runner.py"

# aggregate everything
echo "Performing aggregation of resultant json strings.."
/usr/local/cms/python-3.4.2/bin/python3.4 "$uam_dir/aggregator.py" "$3"\
    "$submissions_dir" "$4" "$2/$3/groups.txt" "aggregated.json"

# apply txt template
echo "Transforming aggregation to human readable output.."
python3 "$uam_dir/templator.py" "aggregated.json" txt "$1"

# produce gf file
echo "Transforming aggregation to GF file for automated grade entry.."
python3 "$uam_dir/templator.py" "aggregated.json" gf "`echo $1 | cut -d'.' -f1`.gf"

# produce markus file
echo "Transforming aggregation to MarkUs file for automated grade entry.."
spython3 "$uam_dir/templator.py" "aggregated.json" markus "`echo $1 | cut -d'.' -f1`.markus"

# finally, commit if needed
[ -n "$9" ] && { "$uam_dir/commit.sh" "$submissions_dir" "$1"; }

# cleanup
echo "Cleaning up.."
rm -f directories.txt aggregated.json

echo "Done"
