#!/usr/bin/env python3
#requires python>3.6
#Requires - pip install pyyaml

from urllib.parse import quote
import os
import sys
import subprocess
import shutil
import json
import requests
import csv
from shutil import copyfile
from xml.etree.ElementTree import ElementTree
try:
   import yaml
except ImportError:
   print('Error, yaml is required, please run pip install pyyaml')

tests=""
testsrun=""
run_id=""
proxy=""
username=""
password=""

def find(name):
    currentdir = os.getcwd() # using current dir, could change this to work with full computer search
    for root, dirs, files in os.walk(currentdir):
        if name in files:
            return os.path.join(os.path.relpath(root, currentdir), name) # for relative path
            #return os.path.join(root, name) # for full path - could also change the main search to search all folders



# inputs
# link to template used as the template
# will create copy of testsuite with all tests called temp.yaml
# list of tests with format testname,
# i.e. #teststorun = "path/testname,, path/testname"
def generate_opentest(teststocreate):
    #Copy xml file with all tests
    # Source path 
    source = testtemplatearg2

    full_path = os.path.realpath(source)
    
    # Destination path 
    destination = os.path.join(os.path.dirname(full_path),"temp.yaml")

    copyfile(source, destination)

    #remove tests not in test list
    teststorun = teststocreate
    testlist = teststorun.split(',,')
    data = ""

    with open(source) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)   

    #data = 
    tests = []
    k=0
    teststring = ""
    for test in testlist:
        #if k != 0:
        #    teststring = teststring + ","
        head_tail = os.path.split(test) 
        test_path = head_tail[0]
        test_name = head_tail[1]
        if test_path == "":
            test_path = "."
        #print("test_path = " + test_path)
        #print("test_name = " + test_name)
        testdic = {'name': test_name, 'path': test_path}
        tests.append(testdic)

    #print(tests)
    testsdic = {'tests' : tests}
    #print(testsdic) 
    data.update(testsdic)
    #print(data) 

    with open(destination, 'w') as f:   
        newdata = yaml.dump(data, f)

# Script to run Katalon tests with Appsurify

# inputs
# link to test suite with all tests
# will create copy of testsuite with all tests called temp.ts
# list of tests with format testname,
# i.e. #teststorun = "Test Cases/New Test Case 2, Test Cases/New Test Case"
def generate_katalon(teststocreate):
    
    #Copy xml file with all tests
    # Source path 
    source = os.path.join(testtemplatearg2, testtemplatearg3)

    full_path = os.path.realpath(source)
    
    # Destination path 
    destination = os.path.join(os.path.dirname(full_path),"temp.ts")

    print(destination)
    copyfile(source, destination)

    #remove tests not in test list
    teststorun = teststocreate
    testlist = teststorun.split(',,')

    tree = ElementTree()
    tree.parse(destination)
        
    root = tree.getroot()
    for test in root.findall('testCaseLink'):
        testids = test.findall('testCaseId')
        for testid in testids:
            print((testid.text))
            if testid.text not in testlist:
                root.remove(test)

    tree.write(destination)

# Function to run Sahi tests with Appsurify

# Will generate two files one called temp.dd.csv and anotehr called temp.suite.
# To run the tests execute testrunner.bat|.sh temp.dd.csv %additionalargs%

# inputs
# list of tests with format testsuitename#testname,
# i.e. #sahiteststorun = "ddcsv_dd_csv#test9.sah,ddcsv_dd_csv#test10.sah,sahi_demo_sah#sahi_demo.sah,demo_suite#getwin_popupWithParam.sah"

# Questions/TODO's
#should we get the first line comment?

# query to get which tests to run
# Can get - <testsuite name="ddcsv_dd_csv" tests="3" failures="3" errors="0" time="24.051">
# <testcase classname="ddcsv_dd_csv.test9" name="test9.sah" time="17.982">
# normal suite <?xml version="1.0" encoding="UTF-8"?><testsuite name="demo_suite" tests="138" failures="23" errors="0" time="2322.014">
# <testcase classname="demo_suite.204" name="204.sah" time="4.615"></testcase>
# single test
#<?xml version="1.0" encoding="UTF-8"?><testsuite name="sahi_demo_sah" tests="1" failures="0" errors="0" time="14.008">
#	<testcase classname="sahi_demo_sah.sahi_demo" name="sahi_demo.sah" time="9.967"></testcase></testsuite>
# find file before the . in classname
# open that file and find the row with test9.sah
# copy that row to new file

def generate_sahi(teststocreate):
    sahiteststorun = sys.argv[1]
    datarows = []
    sahitests = sahiteststorun.split(",,")
    print(sahitests)
    standalonetests = []
    suitetests = []
    datatests = []
    rows = []
    standalonerows = []

    if os.path.exists("temp.dd.csv"):
        os.remove("temp.dd.csv")
    if os.path.exists("temp.suite"):
        os.remove("temp.suite")

    for test in sahitests:
        testsuitename = test[0:(test.find("#"))]
        testsuitename=testsuitename.replace("_",".")
        testname=test[(test.find("#"))+1:]
        if testsuitename[-4:] == ".sah":
            standalonetests.append(testname)
        if testsuitename[-4:] == ".csv":
            datatests.append(test)
        if testsuitename[-6:] == ".suite":
            suitetests.append(test)

    print("printing standalone then data then suite")
    print(standalonetests)
    print(datatests)
    print(suitetests)
    print("printed sets")

    for test in suitetests:
        print(test)

        testsuitename = test[0:(test.find("#"))]
        testsuitename=testsuitename.replace("_",".")
        testname=test[(test.find("#"))+1:]
        print(testname)
        print(testsuitename)

        f=open(testsuitename, "r")
        fl =f.readlines()
        for line in fl:
            #print(line)
            if testname in line:
                values = line.split()
                for i, value in enumerate(values):
                    if testname in value:
                        values[i] = find(testname)

                print(values)
                row = " ".join(values)
                print(row)
                standalonerows.append(row)
                print(('Found {}'.format(row)))

    print(standalonerows)

    f= open("temp.suite","w+")
    for row in standalonerows:
        f.write(row + '\n')

    print(standalonetests)
    for test in standalonetests:
        f.write(find(test) + '\n')

    f.close()

    for test in datatests:
        print(test)
        testsuitename = test[0:(test.find("#"))]
        testsuitename=testsuitename.replace("_",".")
        testname=test[(test.find("#"))+1:]
        print(testname)
        print(testsuitename)

        with open(testsuitename, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                #print(row)
                if testname in row:
                    print(('Found: {}'.format(row)))
                    for i, column in enumerate(row):
                        if testname in column:
                            row[i] = find(testname)
                    rows.append(row)

    with open('temp.dd.csv', 'w') as outf:
        writer = csv.writer(outf)
        for row in rows:
            writer.writerow(row)
        tempsuite = ["temp.suite"]
        writer.writerow(tempsuite)

###############################################################################################################################
###############################################################################################################################
###############################################################################################################################
#Main Script

def urlencode(name):
    return quote(name, safe='')

def echo(stringtoprint):
    print (stringtoprint)

def runcommand(command):
    echo("platform = " + sys.platform)
    result = subprocess.run(command,  shell=True, capture_output=True)
    #subprocess.run(['ls', '-l'])stdout=subprocess.PIPE,
    print((result.stdout.decode('utf-8')))
    print((result.stderr.decode('utf-8')))
    return result.stdout.decode('utf-8')

def delete_reports():
    if reporttype == "directory":
        folder = report
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(('Failed to delete %s. Reason: %s' % (file_path, e)))
    if reporttype == "file":
        os.remove(report)


def execute_tests(testlist, testset):
    if deletereports == "true":
        delete_reports()
    command = ""

    endrunpostfix
    if generatefile == "false":
        if testset == 0:
            command = startrunall + startrunpostfix + testlist + endrunprefix + endrunall + endrunpostfix
        else:
            command = startrunspecific + startrunpostfix + testlist + endrunprefix + endrunspecific + endrunpostfix

    if generatefile == "sahi":
        generate_sahi(testlist)
        if testset == 0:
            command = startrunall + startrunpostfix + endrunprefix + endrunall + endrunpostfix
        else:
            command = startrunspecific + startrunpostfix + endrunprefix + endrunspecific + endrunpostfix

    if generatefile == "katalon":
        generate_katalon(testlist)
        if testset == 0:
            command = startrunall + startrunpostfix + endrunprefix + endrunall + endrunpostfix
        else:
            command = startrunspecific + startrunpostfix + endrunprefix + endrunspecific + endrunpostfix
    
    if generatefile == "opentest":
        generate_opentest(testlist)
        if testset == 0:
            command = startrunall + startrunpostfix + endrunprefix + endrunall + endrunpostfix
        else:
            command = startrunspecific + startrunpostfix + endrunprefix + endrunspecific + endrunpostfix

    echo("run command = " + command)
    runcommand(command)
    echo(os.getcwd())
    push_results()


def get_tests(testpriority):
    echo("getting test set "+ str(testpriority))
    tests=""
    valuetests=""
    finalTestNames=""
    #echo("runfrequency = " + runfrequency)
    #echo("apikey = " + apikey)
    #echo("importtype = " + importtype)
    #echo("commit = "+ commit)
    #echo("projectencoded = "+ projectencoded)
    #echo("testsuiteencoded = "+ testsuiteencoded)
    #echo("testpriority = "+ str(testpriority))
    #echo("addclassname = "+ addclassname)
    #echo("addtestsuitename = "+ addtestsuitename)
    #echo("testsuitesnameseparator = "+ testsuitesnameseparator)
    #echo("classnameseparator = "+ classnameseparator)
    #echo("repository = "+ repository)
    #echo("url = "+ url)
    #echo("branch = "+ branch)

    #apiendpoint=f"{url}/api/external/prioritized-tests/?project_name={projectencoded}&priority={testpriority}&testsuitename_separator={testsuitesnameseparator}&testsuitename={addtestsuitename}&classname={addclassname}&classname_separator={classnameseparator}&test_suite_name={testsuiteencoded}&first_commit={commit}"
    #headers={'token': apikey}
    headers = {
        'token': apikey,
    }

    params = {
        'name_type': importtype,
        'commit': commit,
        'project_name': projectencoded,
        'test_suite_name': testsuiteencoded,
        'priority': testpriority,
        'classname': addclassname,
        'testsuitename': addtestsuitename,
        'testsuitename_separator': testsuitesnameseparator,
        'classname_separator': classnameseparator,
        'repo': repository,
    }

    if runfrequency == "single":
        params["commit_type"] = "Single"
    if runfrequency == "multiple":
        params["commit_type"] = "LastRun"
        params["target_branch"] = branch
    if runfrequency == "betweenexclusive":
        params["commit_type"] = "BetweenExclisuve"
        params["target_branch"] = branch
        params["from_commit"] = fromcommit
    if runfrequency == "betweeninclusive":
        params["commit_type"] = "BetweenInclusive"
        params["target_branch"] = branch
        params["from_commit"] = fromcommit

    print(params)

    if proxy == "":
        response = requests.get(url+'/api/external/prioritized-tests/', headers=headers, params=params)
    else:
        httpproxy = "http://"+proxy
        httpsproxy = "https://"+proxy
        proxies = {"http": httpproxy,"https": httpsproxy}
        if username == "":
            response = requests.get(url+'/api/external/prioritized-tests/', headers=headers, params=params, proxies=proxies)
        else:
            auth = HTTPProxyAuth(username, password)
            response = requests.get(url+'/api/external/prioritized-tests/', headers=headers, params=params, proxies=proxies, auth=auth)
    print("request sent to get tests")
    print((response.status_code))

    if response.status_code >= 500:
        print(('[!] [{0}] Server Error'.format(response.status_code)))
        return None
    elif response.status_code == 404:
        print(('[!] [{0}] URL not found: [{1}]'.format(response.status_code,api_url)))
        return None  
    elif response.status_code == 401:
        print(('[!] [{0}] Authentication Failed'.format(response.status_code)))
        return None
    elif response.status_code == 400:
        print(('[!] [{0}] Bad Request'.format(response.status_code)))
        return None
    elif response.status_code >= 300:
        print(('[!] [{0}] Unexpected Redirect'.format(response.status_code)))
        return None
    elif response.status_code == 200:
        testset = json.loads(response.content.decode('utf-8'))
        return testset
    else:
        print(('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content)))
    return None

def get_and_run_tests(type):
    testset = get_tests(type)
    count=0
    
    tests = ""
    try:    
        for element in testset:
            count = count + 1
            if count == 1:
                tests = prefixtest+element["name"]+postfixtest
            else:
                tests = tests+testseparator+prefixtest+element["name"]+postfixtest
            
            if count == maxtests:
                execute_tests(tests, type)
                count = 0
                tests = ""
                failfast_tests()
    except:
        print("No tests to run")
        
    if tests != "":
        execute_tests(tests, type)
        failfast_tests

    return tests
    
    #doesn't work as it will run on high, medium and low then if there are none for any it will run all
    #if type != 5 and tests == "":
    #        print("executing all tests")
    #        execute_tests("", 0)

def failfast_tests(tests):
    if failfast == "true":
        rerun_tests()
        getresults()

def rerun_tests_execute():
    get_and_run_tests(5)

def rerun_tests():
    if rerun == "true": 
        numruns = 1
        while numruns <= maxrerun:
            echo("rerun " + str(numruns))
            rerun_tests_execute()
            numruns = numruns+1

def getresults():
    echo("getting results")
    headers = {
    'token': apikey,
    }

    params = (
        ('test_run', run_id),
    )
    print(params)
    print(headers)
    if proxy == "":
        response = requests.get(url+'/api/external/output/', headers=headers, params=params)
    else:
        httpproxy = "http://"+proxy
        httpsproxy = "https://"+proxy
        proxies = {"http": httpproxy,"https": httpsproxy}
        if username == "":
            response = requests.get(url+'/api/external/output/', headers=headers, params=params, proxies=proxies)
        else:
            auth = HTTPProxyAuth(username, password)
            response = requests.get(url+'/api/external/output/', headers=headers, params=params, proxies=proxies, auth=auth)
    print("result request sent")
    resultset = ""
    if response.status_code >= 500:
        print(('[!] [{0}] Server Error'.format(response.status_code)))
        return None
    elif response.status_code == 404:
        print(('[!] [{0}] URL not found: [{1}]'.format(response.status_code,api_url)))
        return None  
    elif response.status_code == 401:
        print(('[!] [{0}] Authentication Failed'.format(response.status_code)))
        return None
    elif response.status_code == 400:
        print(('[!] [{0}] Bad Request'.format(response.status_code)))
        return None
    elif response.status_code >= 300:
        print(('[!] [{0}] Unexpected Redirect'.format(response.status_code)))
        return None
    elif response.status_code == 200:
        resultset = json.loads(response.content.decode('utf-8'))
        echo(resultset)
    else:
        print(('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content)))


    if resultset["new_defects"] and "newdefects" in fail:
        exit(1)
    if resultset["reopened_defects"] != 0 and "reopeneddefects" in fail:
        exit(1)
    if resultset["flaky_defects"] != 0 and "newflaky" in fail:
        exit(1)
    if resultset["reopened_flaky_defects"] != 0 and "reopenedflaky" in fail:
        exit(1)
    if resultset["flaky_failures_breaks"] != 0 and "flakybrokentests" in fail:
        exit(1)
    if resultset["failed_test"] != 0 and "failedtests" in fail:
        exit(1)
    if resultset["broken_test"] != 0 and "brokentests" in fail:
        exit(1)    

def push_results():
    echo("pushing test results")
    if reporttype == "directory":
        filetype = ".xml"
        if importtype == "trx":
            filetype = ".trx"
        for file in os.listdir(report):
            if file.endswith(filetype):
                echo(file)
                call_import(os.path.abspath(os.path.join(report, file)))
    if reporttype == "file":
        call_import(report)

def call_import(filepath):
    apiurl = url+"/api/external/import/"

    payload = {'type': importtype,
            'commit': commit,
            'project_name': projectencoded,
            'test_suite_name': testsuiteencoded,
            'repo': repository}
    files = {
        'file': open(filepath, 'rb'),
    }
    headers = {
        'token': apikey,
    }
    print(headers)
    print(payload)
    print(apiurl)
    if proxy == "":
        response = requests.post(apiurl, headers=headers, data=payload, files=files)
    else:
        httpproxy = "http://"+proxy
        httpsproxy = "https://"+proxy
        proxies = {"http": httpproxy,"https": httpsproxy}
        if username == "":
            response = requests.post(apiurl, headers=headers, data=payload, files=files, proxies=proxies)
        else:
            auth = HTTPProxyAuth(username, password)
            response = requests.post(apiurl, headers=headers, data=payload, files=files, proxies=proxies, auth=auth)
    
    print("file import sent")
    if response.status_code >= 500:
        print(('[!] [{0}] Server Error {1}'.format(response.status_code, response.content.decode('utf-8'))))
    elif response.status_code == 404:
        print(('[!] [{0}] URL not found: []'.format(response.status_code)))
    elif response.status_code == 401:
        print(('[!] [{0}] Authentication Failed'.format(response.status_code)))
    elif response.status_code == 400:
        print(('[!] [{0}] Bad Request'.format(response.status_code)))
    elif response.status_code >= 300:
        print(('[!] [{0}] Unexpected Redirect'.format(response.status_code)))
    elif response.status_code == 200 or response.status_code == 201:
        resultset = json.loads(response.content.decode('utf-8'))
        echo(resultset)
        echo("report url = " + resultset["report_url"])
        echo("run url = " + str(resultset["test_run_id"]))
        global run_id
        run_id = str(resultset["test_run_id"])
    else:
        print(('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content)))

url = ""
apikey =""
project =""
testsuite =""
report = ""
maxtests=1000000 #default 10000000
fail="newdefects, reopeneddefects" #default new defects and reopened defects  #options newdefects, reopeneddefects, flakybrokentests, newflaky, reopenedflaky, failedtests, brokentests
additionalargs="" #default ''
testseparator="" #default ' '
postfixtest="" #default ''
prefixtest="" #default ''
fullnameseparator="" #default ''
fullname="false" #default false
failfast="false" #defult false
maxrerun=3 #default 3
rerun="true" #default false
importtype="junit" #default junit
reporttype="directory" #default directory other option file, when directory needs to end with /
teststorun="all" #options include - high, medium, low, unassigned, ready, open, none
deletereports="false" #options true or false, BE CAREFUL THIS WILL DELETE THE SPECIFIC FILE OR ALL XML FILES IN THE DIRECTORY
startrunall = "" #startrun needs to end with a space sometimes
endrunall = ""#endrun needs to start with a space sometimes
startrunspecific = "" #startrun needs to end with a space sometimes
endrunspecific = ""#endrun needs to start with a space sometimes
commit=""
scriptlocation="./"
branch=""
#runfrequency="single" #options single for single commits, lastrun for all commits since the last run, betweeninclusive or betweenexclusive for all commits between two commits either inclusive or exclusive
runfrequency="multiple" #options single for ['Single', 'LastRun', 'BetweenInclusive', 'BetweenExclusive']
fromcommit=""
repository="git"
scriptlocation="./"
generatefile="false"
template="none"
addtestsuitename="false"
addclassname="false"
runtemplate=""
testsuitesnameseparator=""
testtemplate=""
classnameseparator=""
testseparatorend=""
testtemplatearg1=""
testtemplatearg2=""
testtemplatearg3=""
testtemplatearg4=""
startrunpostfix=""
endrunprefix=""
endrunpostfix=""
#--testsuitesnameseparator and classnameseparator need to be encoded i.e. # is %23


#Templates

c=0

if len(sys.argv) > 1 :
    c=len(sys.argv)
    for k in range(1,c):
        if sys.argv[k] == "--runtemplate":
            runtemplate = sys.argv[k+1]
        if sys.argv[k] == "--testtemplate":
            testtemplate = sys.argv[k+1]
        if sys.argv[k] == "--testtemplatearg1":
            testtemplatearg1 = sys.argv[k+1]
        if sys.argv[k] == "--testtemplatearg2":
            testtemplatearg2 = sys.argv[k+1]
        if sys.argv[k] == "--testtemplatearg3":
            testtemplatearg3 = sys.argv[k+1]
        if sys.argv[k] == "--testtemplatearg4":
            testtemplatearg4 = sys.argv[k+1]

#####Test Run Templates######

if runtemplate == "prioritized tests with unassigned":
    teststorun="high,medium,unassigned"

if runtemplate == "prioritized tests without unassigned":
    teststorun="high,medium,unassigned"

if runtemplate == "no tests":
    teststorun="none"
    fail="newdefects, reopeneddefects, failedtests, brokentests"

if testtemplate == "all tests":
    teststorun="all"
    fail="newdefects, reopeneddefects, failedtests, brokentests"

if len(sys.argv) > 1 :
    for k in range(1,c):
        if sys.argv[k] == "--teststorun":
            teststorun = sys.argv[k+1]

#Template Sahi
#testsuitename#testname
#addtestsuitename=true
#testsuitesnameseparator=%23
#Sahi Setup
#testrunner.bat demo/demo.suite http://sahitest.com/demo/ firefox
#startrun testrunner.bat temp.dd.csv 
#endrun as per setup
#SET LOGS_INFO=junit:<LOCATION>
#https://sahipro.com/docs/using-sahi/playback-commandline.html

#Sahi Ant
#https://sahipro.com/docs/using-sahi/playback-desktop.html#Playback%20via%20ANT
#startrun ant -f demo.xml
#<property name="scriptName" value="demo/ddcsv/temp.dd.csv"/>
#<report type="junit" logdir="<LOCATION>"/>

# To run tests with sahi
# edit testrunner.bat or .sh - add line "SET LOGS_INFO=junit:<Directory of your choice>"
# startrun = 'testrunner.bat or .sh temp.dd.csv' 
# endrun = ' <additional arguments>'
# report = directory set when editing the testrunner/index.xml - we only want the index file

if testtemplate == "sahi ant":
    testseparator=",,"
    addtestsuitename="true"
    testsuitesnameseparator="#"
    generatefile="sahi"
    startrunall="ant -f "+testtemplatearg2
    startrunspecific="ant -f "+testtemplatearg3
    report = testtemplatearg1


#set endrun to being final command for test runner i.e. browser etc
if testtemplate == "sahi testrunner":
    testseparator=",,"
    addtestsuitename="true"
    testsuitesnameseparator="#"
    generatefile="sahi"
    startrunspecific="testrunner temp.dd.csv"
    startrunall="testrunner " + testtemplatearg2
    report=testtemplatearg1

if testtemplate == "mvn":
    testseparator=","
    addtestsuitename="true"
    testsuitesnameseparator="#"
    startrunspecific="mvn -Dtest="
    endrunspecific=" test"
    startrunall="mvn test"
    report="./target/surefire-reports/"
    reporttype="directory"
    deletereports="true"


#mvn test -Dcucumber.options="--name 'another scenario' --name '^a few cukes$'"
if testtemplate == "cucmber mvn":
    testseparator=" "
    startrunspecific="mvn test -Dcucumber.options=\""
    endrunspecific="\" "
    postfixtest="$'"
    prefixtest="--name '^"
    startrunall="mvn test"
    report="./target/surefire-reports/"
    reporttype="directory"
    deletereports="true"

if testtemplate == "rspec":
    testseparator=" "
    startrunspecific="rspec --format RspecJunitFormatter --out rspec.xml "
    prefixtest = "-e '"
    postfixtest="'"
    startrunall="rspec --format RspecJunitFormatter --out rspec.xml"
    reporttype="file"
    report="rspec.xml"

#startrun should be how your tests are executed i.e. java -jar robotframework.jar or robot
#then -x robot.xml to create the output file
#then --test ' if you are running specific tests
#endrun should be the location of your tests
if testtemplate == "robotframework":
    prefixtest=" --test '"
    postfixtest="'"
    testseparator=" "
    reporttype="file"
    report=testtemplatearg3
    startrunall=testtemplatearg1 + " -x " + testtemplatearg3 + " "
    endrunall=testtemplatearg2
    startrunspecific=testtemplatearg1 +" -x " + testtemplatearg3 + " "
    endrunall=testtemplatearg2


#mocha
#install https://www.npmjs.com/package/mocha-junit-reporter
#https://github.com/mochajs/mocha/issues/1565
if testtemplate == "mocha":
    testseparator="|"
    reporttype="file"
    report="test-results.xml"
    startrunspecific="mocha test --reporter mocha-junit-reporter -g "
    postfixtest="$"
    prefixtest="^"
    startrunall="mocha test --reporter mocha-junit-reporter "

#pytest
#https://stackoverflow.com/questions/36456920/is-there-a-way-to-specify-which-pytest-tests-to-run-from-a-file
if testtemplate == "pytest":
    testseparator=" or "
    reporttype="file"
    report="test-results.xml"
    startrunspecific="python -m pytest --junitxml=test-results.xml -k '"
    endrunspecific="'"
    startrunall="python -m pytest --junitxml=test-results.xml"

#testim
#https://help.testim.io/docs/the-command-line-cli
if testtemplate == "testim":
    testseparator=" --name '"
    reporttype="file"
    report="test-results.xml"
    startrunspecific="testim --report-file test-results.xml --name '"
    postfixtest="'"
    startrunall="testim --report-file test-results.xml"


#testcomplete
#TestComplete.exe "C:\My Projects\MySuite.pjs" /run /p:MyProj /ExportSummary:"C:\TestLogs\report.xml"
#/test""ProjectTestItem1"
#https://support.smartbear.com/testcomplete/docs/working-with/automating/command-line-and-exit-codes/command-line.html
if testtemplate == "testcomplete":
    testseparator="|"
    reporttype="file"
    report=testtemplatearg2
    startrunspecific="TestComplete.exe "+testtemplatearg1 + " "
    endrunspecific = testtemplatearg2
    startrunall="TestComplete.exe "+testtemplatearg1 + " "
    endrunall=+ " /ExportSummary:"+testtemplatearg2

#ranorex webtestit
#https://discourse.webtestit.com/t/running-ranorex-webtestit-in-cli-mode/152
if testtemplate == "ranorex webtestit":
    testseparator="|"
    reporttype="file"
    report=testtemplatearg2
    startrunspecific="TestComplete.exe "+testtemplatearg1 + " "
    endrunspecific = testtemplatearg2
    startrunall="TestComplete.exe "+testtemplatearg1 + " "
    endrunall=+ " /ExportSummary:"+testtemplatearg2

#cypress
#https://github.com/bahmutov/cypress-select-tests
#cypress run --reporter junit --reporter-options mochaFile=result.xml
if testtemplate == "cyprus":
    testseparator="|"
    reporttype="file"
    report="results.xml"
    startrunspecific="cypress run --reporter junit --reporter-options mochaFile=result.xml grep="
    postfixtest="'"
    prefixtest="'"
    startrunall="cypress run --reporter junit --reporter-options mochaFile=result.xml"

#mstest
#/Tests:TestMethod1,testMethod2
#mstest.exe"  /testcontainer:"%WORKSPACE%\MYPROJECT\bin\debug\MYTEST.dll" /test:"ABC" /resultsfile:"%WORKSPACE%\result_%BUILD_NUMBER%.xml"
if testtemplate == "mstest":
    testseparator=","
    reporttype="file"
    startrunspecific="mstest /resultsfile:'" + testtemplatearg1 + "' /testcontainer:'" + testtemplatearg2 + "'" + "/tests:"
    postfixtest="'"
    prefixtest="'"
    startrunall="mstest /resultsfile:'" + testtemplatearg1 + "' /testcontainer:'" + testtemplatearg2 + "'"
    report=testtemplatearg1
    importtype="trx"


#vstest
#/Tests:TestMethod1,testMethod2
#vstest.console.exe"  /testcontainer:"%WORKSPACE%\MYPROJECT\bin\debug\MYTEST.dll" /test:"ABC" /resultsfile:"%WORKSPACE%\result_%BUILD_NUMBER%.xml"
if testtemplate == "vstest":
    testseparator=","
    reporttype="file"
    startrunspecific="vstest.console.exe /resultsfile:'" + testtemplatearg1 + "' /testcontainer:'" + testtemplatearg2 + "'" + "/tests:"
    postfixtest="'"
    prefixtest="'"
    startrunall="vstest.console.exe /resultsfile:'" + testtemplatearg1 + "' /testcontainer:'" + testtemplatearg2 + "'"
    report=testtemplatearg1
    importtype="trx"

#Jasmine3
#npm install -g jasmine-xml-reporter for jasmine 2.x then use --junitreport and --output to determine where to output the report.
#npm install -g jasmine-junit-reporter requires jasmine --reporter=jasmine-junit-reporter creates file junit_report
if testtemplate == "mocha":
    testseparator="|"
    reporttype="file"
    report="junit_report.xml"
    startrunspecific="jasmine --reporter=jasmine-junit-reporter --filter='"
    endrunspecific="'"
    postfixtest="$"
    prefixtest="^"
    startrunall="jasmine test --reporter=jasmine-junit-reporter "

#tosca
#https://support.tricentis.com/community/article.do?number=KB0013693
#https://documentation.tricentis.com/en/1000/content/continuous_integration/execution.htm
#https://documentation.tricentis.com/en/1030/content/continuous_integration/configuration.htm
#testset = https://documentation.tricentis.com/en/1010/content/tchb/tosca_executor.htm


#katalon
#katalonc -noSplash -runMode=console -projectPath="C:\Katalon\Test\Test Project\Test Project.prj" -retry=0 -testSuitePath="Test Suites/New Test Suite"
# -executionProfile="default" -browserType="Chrome" -apiKey="ee04de44-b3c7-4c9e-b8cd-741157fd4324" -reportFolder="c:\katalon" -reportFileName="report"
#JUnit_Report.xml gets generated
# Has apiKey - https://forum.katalon.com/t/how-to-use-katalon-plugin-for-jenkins-on-windows/20326/3
#-projectPath=<path>	Specify the project location (include .prj file). The absolute path must be used in this case.	Y
#-testSuitePath=<path>	Specify the test suite file (without extension .ts). The relative path (root being project folder) must be used in this case.
#-reportFolder=<path>	Specify the destination folder for saving report files. Can use absolute path or relative path (root being project folder).	N
#-reportFileName=<name>	Specify the name for report files (.html, .csv, .log). If not provide, system uses the name "report" (report.html, report.csv, report.log). This option is only taken into account when being used with "-reportFolder" option.
if testtemplate == "katalon":
    testseparator=",,"
    reporttype="file"
    report = testtemplatearg1
    head_tail = os.path.split(testtemplatearg1) 
    report_folder = head_tail[0]
    report_file = head_tail[1]
    head_tail = os.path.split(testtemplatearg3) 
    startrunspecific="katalonc -noSplash -runMode=console -projectPath='" + testtemplatearg2 + "' -testSuitePath='" + "'" + os.path.join(head_tail[0], "temp.ts") + "' -apiKey='" + testtemplatearg4 +"' -reportFolder='" + report_folder + " -reportFileName='" + report_file + "'"
    startrunall="katalonc -noSplash -runMode=console -projectPath='" + testtemplatearg2 + "' -testSuitePath='" + "'" + testtemplatearg3 + "' -apiKey='" + testtemplatearg4 +"' -reportFolder='" + report_folder + " -reportFileName='" + report_file + "'"
    generatefile="katalon"
    
    
#opentest
#testtemplatearg1 = report
#testtemplatearg2 = template of template with no tests
#testtemplatearg3 = template with all tests
if testtemplate == "opentest":
    testseparator=",,"
    reporttype="file"
    report = testtemplatearg1
    full_path = os.path.realpath(source)
    destination = os.path.join(os.path.dirname(full_path),"temp.yaml")
    startrunspecific="opentest session create --out '"+testtemplatearg1+ "' --template '" + destination + "' "
    startrunall="opentest session create --out '"+testtemplatearg1+ "' --template '" + testtemplatearg3 + "' "
    generatefile="opentest"


#Todo
#mstest
#nunit
#xunit
#gradle/ant?
#c?
#c++
#clojure
#eunit
#go
#haskell
#javascript
#objective c
#perl
#php
#scala
#swift
#htmlunit
#ranorex
#qmetry
#leapwork
#experitest
#katalon
#testsigma - currently not possible
#lambdatest
#smartbear crossbrowsertesting
#uft
#telerik test studio
#perfecto
#tosca test suite
#mabl - currently not possible
#test craft
#squish
#test cafe


if len(sys.argv) > 1 :
    for k in range(1,c):
        if sys.argv[k] == "--url":
            url = sys.argv[k+1]
        if sys.argv[k] == "--apikey":
            apikey = sys.argv[k+1]
        if sys.argv[k] == "--project":
            project = sys.argv[k+1]
        if sys.argv[k] == "--testsuite":
            testsuite = sys.argv[k+1]
        if sys.argv[k] == "--report":
            report = sys.argv[k+1]
        if sys.argv[k] == "--reporttype":
            reporttype = sys.argv[k+1]
        if sys.argv[k] == "--teststorun":
            teststorun = sys.argv[k+1]
        if sys.argv[k] == "--importtype":
            importtype = sys.argv[k+1]
        if sys.argv[k] == "--addtestsuitename":
            addtestsuitename = sys.argv[k+1]
        if sys.argv[k] == "--testsuitesnameseparator":
            testsuitesnameseparator = sys.argv[k+1]
        if sys.argv[k] == "--addclassname":
            addclassname = sys.argv[k+1]
        if sys.argv[k] == "--classnameseparator":
            classnameseparator = sys.argv[k+1]
        if sys.argv[k] == "--rerun":
            rerun = sys.argv[k+1]
        if sys.argv[k] == "--maxrerun":
            maxrerun = sys.argv[k+1]
        if sys.argv[k] == "--failfast":
            failfast = sys.argv[k+1]
        if sys.argv[k] == "--fullname":
            fullname = sys.argv[k+1]
        if sys.argv[k] == "--fullnameseparator":
            fullnameseparator = sys.argv[k+1]
        if sys.argv[k] == "--startrunall":
            startrunall = sys.argv[k+1]
        if sys.argv[k] == "--startrunspecific":
            startrunspecific = sys.argv[k+1]
        if sys.argv[k] == "--prefixtest":
            prefixtest = sys.argv[k+1]
        if sys.argv[k] == "--postfixtest":
            postfixtest = sys.argv[k+1]
        if sys.argv[k] == "--testseparator":
            testseparator = sys.argv[k+1]
        if sys.argv[k] == "--testseparatorend":
            testseparatorend = sys.argv[k+1]
        if sys.argv[k] == "--endrunspecific":
            endrunspecific = sys.argv[k+1]
        if sys.argv[k] == "--endrunall":
            endrunall = sys.argv[k+1]
        if sys.argv[k] == "--additionalargs":
            additionalargs = sys.argv[k+1]
        if sys.argv[k] == "--fail":
            fail = sys.argv[k+1]
        if sys.argv[k] == "--commit":
            commit = sys.argv[k+1]
        if sys.argv[k] == "--branch":
            branch = sys.argv[k+1]
        if sys.argv[k] == "--maxtests":
            maxtests = sys.argv[k+1]
        if sys.argv[k] == "--scriptlocation":
            scriptlocation = sys.argv[k+1]
        if sys.argv[k] == "--runfrequency":
            runfrequency = sys.argv[k+1]
        if sys.argv[k] == "--fromcommit":
            fromcommit = sys.argv[k+1]
        if sys.argv[k] == "--repository":
            repository = sys.argv[k+1]
        if sys.argv[k] == "--generatefile":
            generatefile = sys.argv[k+1]
        if sys.argv[k] == "--startrunpostfix":
            startrunpostfix = sys.argv[k+1]
        if sys.argv[k] == "--endrunprefix":
            endrunprefix = sys.argv[k+1]
        if sys.argv[k] == "--endrunpostfix":
            endrunpostfix = sys.argv[k+1]
        if sys.argv[k] == "--proxy":
            proxy = sys.argv[k+1]
        if sys.argv[k] == "--username":
            username = sys.argv[k+1]
        if sys.argv[k] == "--password":
            password = sys.argv[k+1]
        if sys.argv[k] == "--help":
            echo("please see url for more details on this script and how to execute your tests with appsurify - https://github.com/Appsurify/AppsurifyCIScript")

if "http://" in proxy:
    proxy = proxy.replace("http://","")

if "https://" in proxy:
    proxy = proxy.replace("https://","")

if url[-1:] == "/":
    url = url[:-1]
    echo("url = "+ url)

if repository == "p4":
    repository = "perforce"

if report[-4:].find(".") >= 0:
    reporttype="file"
else:
    reporttype="directory"

if len(sys.argv) > 1 :
    for k in range(1,c):
        if sys.argv[k] == "--reporttype":
            reporttype = sys.argv[k+1]

testsuiteencoded=urlencode(testsuite)
projectencoded=urlencode(project)
testsuiteencoded=testsuite
projectencoded=project

if commit == "":
    commit=runcommand("git log -1 --pretty=\"%H\"")
    commit = commit.rstrip().rstrip("\n\r")
    print(("commit id = " + commit))

#git branch | grep \* | cut -d ' ' -f2
#git rev-parse --abbrev-ref HEAD
#https://stackoverflow.com/questions/6245570/how-to-get-the-current-branch-name-in-git

if branch == "":
    branch=runcommand("git rev-parse --abbrev-ref HEAD").rstrip("\n\r").rstrip()
    print(("branch = " + branch))

if url == "":
    echo("no url specified")
    exit(1)
if apikey == "":
    echo("no apikey specified")
if project == "":
    echo("no project specified")
    exit(1)
if testsuite == "":
    echo("no testsuite specified")
    exit(1)
if report == "":
    echo("no report specified")
    exit(1)
if runfrequency == "betweeninclusive" and fromcommit == "":
    echo("no from commit specified and runfrequency set to betweeninclusive")
    exit(1)
if runfrequency == "betweenexclusive" and fromcommit == "":
    echo("no from commit specified and runfrequency set to betweenexclusive")
    exit(1)

if startrunspecific == "" and teststorun != "all":
    if teststorun != "none":
        echo("startrunspecific needs to be set in order to execute tests")
        exit(1)
if startrunall == "" and teststorun == "all":
    echo("startrunall needs to be set in order to execute tests")
    exit(1)
if startrunspecific == "" and teststorun == "all" and rerun == "true":
    echo("startrunspecific needs to be set in order to rerun tests, either set rerun to false or set startrunaspecific")
    exit(1)

#if [[ $teststorun == "" ]] ; then echo "no teststorun specified" ; exit 1 ; fi
#if [[ $startrun == "" ]] ; then echo "no command used to start running tests specified" ; exit 1 ; fi

####example RunTestsWithAppsurify.sh --url "http://appsurify.dev.appsurify.com" --apikey "MTpEbzhXQThOaW14bHVQTVdZZXNBTTVLT0xhZ00" --project "Test" --testsuite "Test" --report "report" --teststorun "all" --startrun "mvn -tests" 
#example RunTestsWithAppsurify.sh --url "http://appsurify.dev.appsurify.com" --apikey "MTpEbzhXQThOaW14bHVQTVdZZXNBTTVLT0xhZ00" --project "Test" --testsuite "Test" --report "report" --teststorun "all" --startrun "C:\apache\apache-maven-3.5.0\bin\mvn tests " 
#./RunTestsWithAppsurify.sh --url "https://demo.appsurify.com" --apikey "MTU6a3Q1LUlTU3ZEcktFSTFhQUNoYy1DU3pidkdz" --project "Spirent Demo" --testsuite "Unit" --report "c:\testresults\GroupedTests1.xml" --teststorun "all" --commit "44e9b51296e41e044e45b81e0ef65e9dc4c3bc23"
#python RunTestsWithAppsurify.py --url "http://appsurify.dev.appsurify.com" --apikey "MTpEbzhXQThOaW14bHVQTVdZZXNBTTVLT0xhZ00" --project "Test" --testsuite "Test" --runtemplate "no tests" --testtemplate "mvn"

#run_id=""

#$url $apiKey $project $testsuite $fail $additionalargs $endrun $testseparator $postfixtest $prefixtest $startrun $fullnameseparator $fullname $failfast $maxrerun $rerun $importtype $teststorun $reporttype $report $commit $run_id
echo("Getting tests to run")

valuetests=""
finalTestNames=""
testsrun = ""
if teststorun == "all":
    execute_tests("", 0)
    testsrun="all"

if teststorun == "none":
    testsrun="none"
    push_results()

testtypes=[]

if "high" in teststorun:
    testtypes.append(1)
if "medium" in teststorun:
    testtypes.append(2)
if "low" in teststorun:
    testtypes.append(3)
if "unassigned" in teststorun:
    testtypes.append(4)

####start loop
for i in testtypes:
    print(("testsrun1 = " + testsrun))
    testsrun = get_and_run_tests(i) + testsrun

if testsrun == "":
        print("executing all tests")
        execute_tests("", 0)

if failfast == "false" and rerun == "true" and teststorun != "none":
    rerun_tests()

getresults()