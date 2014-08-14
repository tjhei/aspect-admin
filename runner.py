# timo.heister@gmail.com

import random
import re
import os
import sys
import subprocess
import simplejson
from datetime import datetime

repodir = os.path.abspath("aspect")
github_user = "geodynamics"
github_repo = "aspect"

color_green = "#99ff99"
color_red = "#ff0000"

def is_allowed(username):
    return True

def has_hotword(text):
    return False

def date_to_epoch(dt):
    epoch = datetime.utcfromtimestamp(0)
    return (dt-epoch).total_seconds()

def epoch_to_date(seconds):
    return datetime.utcfromtimestamp(seconds)

def text_to_html(text):
    lines = text.split("\n")
    outlines = []
    for l in lines:
        if l.endswith(" ... ok"):
            outlines.append("<p style='background-color:{0}'>{1}</p>".format(color_green, l))
        elif l.endswith(" ... FAIL"):
            outlines.append("<p style='background-color:{0}'>{1}</p>".format(color_red, l))
        else:
            outlines.append("{0}<br/>".format(l))
    
    return "".join(outlines)


class history:
    def __init__(self):
        # entry with sha1 as key
        # entry is dict() with "sha1", "time", "text", "good", "name"
        self.data = dict()
        self.dbname = "test.db"
        self.timeformat = "%Y-%m-%d %H:%M:%S"

    def load(self):
        f = open(self.dbname, 'r')
        text = f.read()
        f.close()
        self.data = simplejson.loads(text)
        #print "loading {0} entries...".format(len(self.data))

    def save(self):
        text = simplejson.dumps(self.data)
        print "saving {0} entries...".format(len(self.data))
        f = open(self.dbname, 'w')
        f.write(text)
        f.close()

    def sort_keys(self):
        keys = []
        for x in self.data.values():
            keys.append((x['sha1'], x['time']))
        
        return [ k[0] for k in sorted(keys, key=lambda x: x[1], reverse=True) ]

    def dump(self):
        print "dumping {0} entries".format(len(self.data))

        sorted_keys = self.sort_keys()

        print "SHA1 time good name:"
        for sha in sorted_keys:
            x = self.data[sha]
            timestr = "?"
            try:
                dt = epoch_to_date(x['time'])
                timestr = dt.strftime(self.timeformat)
            except:
                pass
            print "{} {} {} {}".format(x['sha1'], timestr, x['good'], x['name'])
    
    def render(self):
        f = open ("results.html", "w")

        f.write("<html><body><h1>Test Results</h1>\n")
        f.write("<p>Last update: {0}</p>".format(datetime.now().strftime(self.timeformat)))

        f.write("<script>function toggle(id) {var o = document.getElementById(id);if (o.style.display=='none') o.style.display='table-row'; else o.style.display='none'; }</script>\n")
        f.write("<table border=1 width='100%' style='border-collapse:collapse'>\n")
        
        sorted_keys = self.sort_keys()

        f.write("<tr><td width='1%'>SHA1</td><td>PASS</td><td>FAIL</td><td>Time</td><td>Comment</td><td>Details</td></tr>\n")
        for sha in sorted_keys:
            x = self.data[sha[0]]
            timestr = "?"
            try:
                dt = epoch_to_date(x['time'])
                timestr = dt.strftime(self.timeformat)
            except:
                pass
            
            sha1 = x['sha'].replace("\n","n")
            details = "<a href='#' onclick='toggle(\"sha{0}\")'>click</a>".format(sha1)
            failtext = "<p style='background-color:#99ff99'>{0}</p>".format(x['nfail'])
            if x['nfail']>0:
                failtext = "<p style='background-color:#ff0000'>{0}</p>".format(x['nfail'])
            comment = ""
            if 'comment' in x.keys():
                comment = x['comment']
            f.write("<tr><td>{0}</td><td>{2}</td><td>{3}</td><td>{1}</td><td>{4}</td><td>{5}</td></tr>\n".format(sha1[0:10], timestr, x['npass'], failtext, comment, details))
            text = text_to_html(x['text'])
            f.write("<tr id='sha{0}' style='display: none'><td colspan='6'>{0}<br/>{1}</td></tr>\n".format(sha1, text))

        f.write("</table>\n")

        f.write("</body></html>")

        f.close()

    def have(self, sha):
        return sha in self.data.keys()

    def delete(self, sha):
        if sha in self.data.keys():
            self.data.pop(sha)
            return

        count = 0
        for k in self.data.keys():
            if k.startswith(sha):
                count = count + 1

        if count==0:
            print "ERROR: sha1 not found."
        elif count==1:
            for k in self.data.keys():
                if k.startswith(sha):
                    self.data.pop(k)
                    return
        else:
            print "ERROR: sha1 is not unique."
            

    def add(self, sha, good, name, text):
        time = date_to_epoch(datetime.now())

        e = dict(sha1=sha, time=time, name=name, good=good, text=text)
        self.data[sha] = e

def test(repodir, h, name=""):
    sha1 = subprocess.check_output("cd {0};git rev-parse HEAD".format(repodir),
                                   shell=True).replace("\n","")
    print "running", sha1
    
    try:
        answer = subprocess.check_output("./test.sh {}".format(sha1),
                                     shell=True,stderr=subprocess.STDOUT)
    except:
        print "failed"
        return

    print answer

    good = True
    import re
    for l in answer.split("\n"):
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

    print good
    h.add(sha1, good, name, answer)
    h.save()


whattodo = ""

if len(sys.argv)<2:
    print "usage:"
    print "runner.py newdb"
    print "runner.py dump"
    print "runner.py testdata"
    print "runner.py run-all"
    print "runner.py pullrequests"
    print "runner.py do-current"
    print "runner.py test user/repo:ref"

#    print "test.py delete <sha1>"
#    print "test.py render it"    
#    print "test.py pull requests"
else:
    whattodo = sys.argv[1]
    arg1 = ""
    if len(sys.argv)>2:
        arg1 = sys.argv[2]

if whattodo=="newdb":
    h = history()
    h.save()

if whattodo != "":
    h = history()
    h.load()

if whattodo == "dump":
    h.dump()

if whattodo == "testdata":    
    h.add("r"+str(random.randrange(10000,99999)), True, "test", "this is some text")
    h.save()
    
if whattodo == "delete":
    h.delete(arg1)
    h.save()

if whattodo == "run-all":
    ret = subprocess.check_call("cd {0} && git checkout master -q".format(repodir), shell=True)
    ret = subprocess.check_call("cd {0} && git pull origin -q".format(repodir), shell=True)

    answer = subprocess.check_output("cd {0} && git log --format=oneline --first-parent -n 10".format(repodir),
                                     shell=True,stderr=subprocess.STDOUT)
    lines = answer.split("\n")
    for l in lines[::-1]:
        sha1 = l.split(" ")[0]
        if len(sha1)!=40:
            continue
        print "discovered {}".format(sha1)
        if not h.have(sha1):
            print "  testing"
            
            ret = subprocess.check_call("cd {0} && git checkout {1} -q".format(repodir, sha1),
                                        shell=True)

            test(repodir, h, "")
        
        else:
            pass

    ret = subprocess.check_call("cd {0} && git checkout master -q".format(repodir), shell=True)
    
if whattodo == "do-current":
    test(repodir, h, "manual")


if whattodo == "pullrequests":
    import urllib2
    #r = urllib2.urlopen("https://api.github.com/repos/burnman-project/burnman/pulls").read()
    #r = urllib2.urlopen("https://api.github.com/repos/tjhei/aspect/pulls").read()
    r = urllib2.urlopen("https://api.github.com/repos/{0}/{1}/pulls".format(github_user, github_repo)).read()
    data = simplejson.loads(r)
    print "found {0} pull requests...".format(len(data))
    for pr in data:
        by = pr['user']['login']
        title = pr['title']
        sha = pr['head']['sha']
        print "PR{}: {} '{}' by {}".format(pr['number'], sha, title, by)
        print "  use: python runner.py test {0}:{1}".format(pr['head']['repo']['full_name'],pr['head']['ref'])
        #print simplejson.dumps(pr, sort_keys=True, indent=4, separators=(',', ': '))
        if h.have(sha):
            print "  already tested"
            result = h.data[sha]
            print "  ", result['good'], result['name'], result['text']
        else:
            allowed = False
            if is_allowed(by):
 #               print "  allowed owner"
                allowed = True
            else:
                r = urllib2.urlopen("https://api.github.com/repos/{0}/{1}/issues/{2}/comments".format(github_user, github_repo, pr['number'])).read()
                comments = simplejson.loads(r)
                for comment in comments:
                    user = comment['user']['login']
                    text = comment['body']
                    if is_allowed(user) and has_hotword(text):
                        print "  allowed by hotword from ", user
                        allowed = True
            
            if allowed:
                pass
#                print "TODO: testing"
                
                                
if whattodo == "test":
    #arg1
    r = re.match("^(\w+)/(\w+):([\w-]+)$", arg1)
    if r:
        user = r.group(1)
        repo = r.group(2)
        ref = r.group(3)
        print user, repo, ref
        
        ret = subprocess.check_call("cd {0} && git fetch https://github.com/{1}/{2} {3} -q".format(repodir, user, repo, ref), shell=True)
        ret = subprocess.check_call("cd {0} && git checkout FETCH_HEAD -q".format(repodir), shell=True)
    
        test(repodir, h, arg1)
    
        ret = subprocess.check_call("cd {0} && git checkout master -q".format(repodir), shell=True)
    



if whattodo == "pull  " and arg1 == "requests":
    import urllib2
    #r = requests.get("https://api.github.com/repos/burnman-project/burnman/pulls").content
    r = urllib2.urlopen("https://api.github.com/repos/burnman-project/burnman/pulls").read()
    data = simplejson.loads(r)
    print "found {0} pull requests...".format(len(data))
    for pr in data:
        by = pr['user']['login']
        title = pr['title']
        print "PR/{0}: '{2}' by {1} ".format(pr['number'], by, title)
        print "  use: python test.py test {0}:{1}".format(pr['head']['repo']['full_name'],pr['head']['ref'])
        #print pr['id']
    #for pr in data:
    #    print pr['id']

if whattodo =="test  ":
    userrepo, ref = arg1.split(":")
    ret = subprocess.check_call("cd {0} && git fetch https://github.com/{1} {2}".format(repodir, userrepo, ref), shell=True)
    ret = subprocess.check_call("cd {0} && git checkout FETCH_HEAD".format(repodir), shell=True)
    
    test(repodir, h, arg1)
    
    ret = subprocess.check_call("cd {0} && git checkout master -q".format(repodir), shell=True)

if whattodo == "run  " and arg1=="all":
    print repodir

    ret = subprocess.check_call("cd {0} && git checkout master -q".format(repodir), shell=True)
    ret = subprocess.check_call("cd {0} && git pull origin -q".format(repodir), shell=True)

    answer = subprocess.check_output("cd {0};git log --format=oneline -n 10".format(repodir),
                                     shell=True,stderr=subprocess.STDOUT)
    lines = answer.split("\n")
    for l in lines[::-1]:
        sha1 = l.split(" ")[0]
        if len(sha1)!=40:
            continue
        if not h.have(sha1):
            
            ret = subprocess.check_call("cd {0};git checkout {1} -q".format(repodir, sha1),
                                        shell=True)

            test(repodir, h)
        
        else:
            pass

    ret = subprocess.check_call("cd {0} && git checkout master -q".format(repodir), shell=True)







    


    