# MarkUs Repo List & Group Scraper -- a part of the UAM project at UofT
# Author: Kenneth Ma (2015), under supervision of Dr. Anya Tafliovich

# Pulls repo and group lists from UTSC's markus with a given username and
# password to login with.

# Assignment-number is sequential (and not the same as assignment name)

# Target is where to place both files in.. UAM requires groups.txt in
# assignment folder

echo "Scraping repository and group lists from MarkUs.."

[ $# -lt 4 ] && { echo "Usage: $0 username password assignment-number target"\
    1>&2; exit 1; }

# config
course="csca20s15"
markus_url="http://markus.utsc.utoronto.ca/$course/en"

# logon to MarkUs and save cookies
echo "Logging on to MarkUs.."
curl -d "user_login=$1&user_password=$2&commit=Log+in" --dump-header \
    "$4/.markus" "$markus_url" &>/dev/null

# pull repo list
echo "Pulling repo list to $4/repos.txt.."
curl -L -b "$4/.markus"\
    "$markus_url/main/submissions/download_svn_repo_list/$3"\
    >"$4/repos.txt"

# repos for UTSC are missing course for some reason, fix it (patch)
sed -i "s:svn//:svn/$course/:" "$4/repos.txt"

# pull groups list
echo "Pull groups list to $4/groups.txt.."
curl -L -b "$4/.markus"\
    "$markus_url/main/groups/download_grouplist/$3"\
    >"$4/groups.txt"
