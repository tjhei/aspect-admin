import os
import re

# github access token to set commit status
# fill in here or create token.txt with it
token  = ""
if os.path.isfile('token.txt'):
    token = open('token.txt').read().replace("\n","")

# directory where the aspect git repo sits
repodir = os.path.abspath("aspect")

# name of the user/organization on github
github_user = "geodynamics"

# name of the repo on github
github_repo = "aspect"

# if a user that is_allowed() posts a comment that has
# has_hotword(text) return True, the PR is tested
def has_hotword(text):
    if "/run-tests" in text:
        return True
    return False

# return true if user is trusted
def is_allowed(username):
    trusted = ['tjhei', 'bangerth']

    if username in trusted:
        return True
    
    return False

# make a nice link for a test result:
def make_link(sha):
    return "http://www.math.clemson.edu/~heister/aspect-logs/{}/".format(sha)

def is_successful(lines):
    good = True
    for l in lines:
        r = re.match("^\s+(\d+) Compiler errors$", l)
        if r:
            n = int(r.group(1))
            if n>0:
                good = False
        r = re.match("^\d+% tests passed, (\d+) tests failed out of \d+$", l)
        if r:
            n = int(r.group(1))
            if n>0:
                good = False
        r = re.match("^Manual: FAILED$", l)
        if r:
            good = False

    return good
