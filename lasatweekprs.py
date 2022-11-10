from github import Github
from datetime import datetime, timedelta
from tabulate import tabulate
from optparse import OptionParser
import os

# using an access token connecting to Github
home = os.path.expanduser("~")
filename = ".accesstoken.txt"
# print(home)
path = os.path.join(home, filename)
# print(path)
if not os.path.exists(path):
    print(" Access Token File doesn't exist, PLease create the file in the user home directory")
    exit()
access_token = open(path).read()
ghconn = Github(access_token)

# Function to get the PR Details


def get_lastweek_allprs(repository_full_name, toemail, fromemail):
    try:
        repo = ghconn.get_repo(repository_full_name)
        # print(repo)
        now = datetime.now()
        pullitems = []
        pulls = (repo.get_pulls(state='all', sort='created'))
        for pull in pulls:
            time_delta = now - pull.created_at
            if time_delta.days <= 7:
                pullitems.append([pull.created_at, pull.html_url,
                                 pull.user.login, pull.title, pull.state, pull.draft])
        if len(pullitems) > 0:
            print("From:", fromemail)
            print("To:", toemail)
            print("Subject: Summary of PR's in last 1 week")
            print("")
            print(tabulate(pullitems, headers=[
                "CREATED_DATE", "PR_URL", "PR_CREATED_BY", "DESCRIPTION", "PR_STATE", "IS_DRAFT"]))
        else:
            print(" No Open or Closed PR's in the last 1 week")
    except:
        print("Repository Not Found")


# Main Block
if __name__ == "__main__":
    usage = "Usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option('-r', '--repository',
                      dest='repository', help='repository name')
    parser.add_option('-f', '--fromemail',
                      dest='fromemail', help='from_email_address', default='noreply@email.com')
    parser.add_option('-t', '--toemail',
                      dest='toemail', help='to_email_address')
    (options, args) = parser.parse_args()
    if not (options.repository and options.toemail):
        raise Exception(" Please provide all the necessary arguments")
    repository = options.repository
    toemail = options.toemail
    fromemail = options.fromemail
    get_lastweek_allprs(repository, toemail, fromemail)
