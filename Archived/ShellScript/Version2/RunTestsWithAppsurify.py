#requires python>3.6

from urllib.parse import quote
import os
import sys
import subprocess
import shutil
import json
import requests
import csv

tests=""

def find(name):
    currentdir = os.getcwd() # using current dir, could change this to work with full computer search
    for root, dirs, files in os.walk(currentdir):
        if name in files:
            return os.path.join(os.path.relpath(root, currentdir), name) # for relative path
            #return os.path.join(root, name) # for full path - could also change the main search to search all folders

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
    sahitests = sahiteststorun.split(",")
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
                print('Found {}'.format(row))

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
                    print ('Found: {}'.format(row))
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
    return subprocess.run(command, stdout=subprocess.PIPE).stdout.decode('utf-8')

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
                print('Failed to delete %s. Reason: %s' % (file_path, e))
    if reporttype == "file":
        os.remove(report)


def execute_tests(testlist):
    if deletereports == "true":
        delete_reports()

    if generatesfile == "false":
       runcommand(startrun+testlist+endrun)

    if generatesfile == "sahi":
        generate_sahi(testlist)
        runcommand(startrun+endrun)

    echo(startrun+tests+testlist+endrun)
    push_results()

def get_tests(testpriority):
    tests=""
    valuetests=""
    finalTestNames=""

    #apiendpoint=f"{url}/api/external/prioritized-tests/?project_name={projectencoded}&priority={testpriority}&testsuitename_separator={testsuitesnameseparator}&testsuitename={addtestsuitename}&classname={addclassname}&classname_separator={classnameseparator}&test_suite_name={testsuiteencoded}&first_commit={commitId}"
    #headers={'token': apikey}
    headers = {
        'token': apikey,
    }

    params = {
        'name_type': importtype
        'commit': commitId,
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

    response = requests.get(url+'/api/external/prioritized-tests/', headers=headers, params=params)

    if response.status_code >= 500:
        print('[!] [{0}] Server Error'.format(response.status_code))
        return None
    elif response.status_code == 404:
        print('[!] [{0}] URL not found: [{1}]'.format(response.status_code,api_url))
        return None  
    elif response.status_code == 401:
        print('[!] [{0}] Authentication Failed'.format(response.status_code))
        return None
    elif response.status_code == 400:
        print('[!] [{0}] Bad Request'.format(response.status_code))
        return None
    elif response.status_code >= 300:
        print('[!] [{0}] Unexpected Redirect'.format(response.status_code))
        return None
    elif response.status_code == 200:
        testset = json.loads(response.content.decode('utf-8'))
        echo(testset)
        return testset
    else:
        print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content))
    for element in testset:
        echo("test = " + element["name"])
        tests=tests+element["name"]
    return None

def get_and_run_tests(type):
    testset = get_test(type)
    count=0
    
    tests = ""
    for element in testset:
        count = count + 1
        if count == 1:
            tests = prefixtest+element["name"]+postfixtest
        else:
            tests = tests+testseparator+prefixtest+element["name"]+postfixtest
        
        if count == maxtests:
            execute_tests(tests)
            count = 0
            tests = ""
            failfast_tests()
    
    if tests != "":
        execute_tests(tests)
        failfast_tests

def failfast_tests(tests):
if failfast == "true":
    rerun_tests()
    getresults()  
}

def rerun_tests_execute():
    get_and_run_tests(5)

def rerun_tests():
    if rerun == "true": 
        numruns=1
        echo "rerun " + numruns
        while numruns <= maxrerun:
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

    response = requests.get(url+'/api/external/output/', headers=headers, params=params)
    resultset = ""
    if response.status_code >= 500:
        print('[!] [{0}] Server Error'.format(response.status_code))
        return None
    elif response.status_code == 404:
        print('[!] [{0}] URL not found: [{1}]'.format(response.status_code,api_url))
        return None  
    elif response.status_code == 401:
        print('[!] [{0}] Authentication Failed'.format(response.status_code))
        return None
    elif response.status_code == 400:
        print('[!] [{0}] Bad Request'.format(response.status_code))
        return None
    elif response.status_code >= 300:
        print('[!] [{0}] Unexpected Redirect'.format(response.status_code))
        return None
    elif response.status_code == 200:
        resultset = json.loads(response.content.decode('utf-8'))
        echo(resultset)
    else:
        print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content))


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
                call_import(os.path.abspath(file))

def call_import(filepath):
    apiurl = url+"/api/external/import/"

    payload = {'type': importtype,
            'commit': commitId,
            'project_name': projectencoded,
            'test_suite_name': testsuiteencoded}
    files = {
        'file': open(filepath, 'rb'),
    }
    headers = {
        'token': apikey,
    }
    response = requests.post(apiurl, headers=headers, data=payload, files=files)
    if response.status_code >= 500:
        print('[!] [{0}] Server Error {1}'.format(response.status_code, response.content.decode('utf-8')))
    elif response.status_code == 404:
        print('[!] [{0}] URL not found: []'.format(response.status_code))
    elif response.status_code == 401:
        print('[!] [{0}] Authentication Failed'.format(response.status_code))
    elif response.status_code == 400:
        print('[!] [{0}] Bad Request'.format(response.status_code))
    elif response.status_code >= 300:
        print('[!] [{0}] Unexpected Redirect'.format(response.status_code))
    elif response.status_code == 200 or response.status_code == 201:
        resultset = json.loads(response.content.decode('utf-8'))
        echo(resultset)
        echo("report url = " + resultset["report_url"])
        run_id = resultset["test_run_id"]
    else:
        print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content))

url = ""
apikey =""
project =""
testsuite =""
report = ""
maxtests=1000000 #default 10000000
fail="newdefects, reopeneddefects" #default new defects and reopened defects  #options newdefects, reopeneddefects, flakybrokentests, newflaky, reopenedflaky, failedtests, brokentests
additionalargs="" #default ''
endrun="" #default ''
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
startrun = "" #startrun needs to end with a space sometimes
endrun = ""#endrun needs to start with a space sometimes
commitId=""
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
#--testsuitesnameseparator and classnameseparator need to be encoded i.e. # is %23
####testing
commitId="e8056a83e26be8d05fbce5c3348c35b8b538fed1"
project="Test Prioritization v16"
testsuite="test"
branch="master"
run_id=6

########
#Templates
########
c=0

if len(sys.argv) > 1 :
    c=len(sys.argv)
    for k in range(1,c):
        if sys.argv[k] == "--runtemplate":
            runtemplate = sys.argv[k+1]
        if sys.argv[k] == "--testtemplate":
            runtemplate = sys.argv[k+1]

#####Test Run Templates######

if runtemplate == "prioritized tests with unassigned":
    teststorun="high,medium,unassigned"

if runtemplate == "prioritized tests without unassigned":
    teststorun="high,medium,unassigned"

if runtemplate == "no tests":
    teststorun="none"

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
    testseparator=","
    addtestsuitename="true"
    testsuitesnameseparator="%23"
    generatefile="sahi"
    if teststorun != "all" and teststorun != "none":
        startrun="ant -f "
    else:
        startrun="ant -f "

#set endrun to being final command for test runner i.e. browser etc
if testtemplate == "sahi testrunner":
    generatesfile="true"
    testseparator=","
    addtestsuitename="true"
    testsuitesnameseparator="%23"
    generatefile="sahi"
    if teststorun != "all" and teststorun != "none":
        startrun="testrunner temp.dd.csv"
    else:
        startrun="testrunner"

if testtemplate == "mvn":
    testseparator=","
    addtestsuitename="true"
    testsuitesnameseparator="%23"
    if teststorun != "all" and teststorun != "none":
        startrun="mvn -Dtest="
        endrun="test"
    else:
        startrun="mvn test"
    report="/target/surefire-reports/"
    reporttype="directory"

if testtemplate == "rspec":
    testseparator=" -e '"
    if teststorun != "all" and teststorun != "none":
        startrun="rspec --format RspecJunitFormatter --out rspec.xml -e '"
        postfixtest="'"
    else:
        startrun="rspec --format RspecJunitFormatter --out rspec.xml"
    reporttype="file"
    report="rspec.xml"

#startrun should be how your tests are executed i.e. java -jar robotframework.jar or robot
#then -x robot.xml to create the output file
#then --test ' if you are running specific tests
#endrun should be the location of your tests
if testtemplate == "robotframework":
    testseparator=" --test '"
    postfixtest="'"
    reporttype="file"
    report="robot.xml"

#mocha
#install https://www.npmjs.com/package/mocha-junit-reporter
#https://github.com/mochajs/mocha/issues/1565
if testtemplate == "mocha":
    testseparator="|"
    reporttype="file"
    report="test-results.xml"
    if teststorun != "all" and teststorun != "none":
        startrun="mocha test --reporter mocha-junit-reporter -g "
        postfixtest="$"
        prefixtest="^"
    else:
        startrun="mocha test --reporter mocha-junit-reporter "

#pytest
#https://stackoverflow.com/questions/36456920/is-there-a-way-to-specify-which-pytest-tests-to-run-from-a-file
if testtemplate == "pytest":
    testseparator=" or "
    reporttype="file"
    report="test-results.xml"
    if teststorun != "all" and teststorun != "none":
        startrun="python -m pytest --junitxml=test-results.xml -k '"
        endrun="'"
    else:
        startrun="python -m pytest --junitxml=test-results.xml"

#testim
#https://help.testim.io/docs/the-command-line-cli
if testtemplate == "testim":
    testseparator=" --name '"
    reporttype="file"
    report="test-results.xml"
    if teststorun != "all" and teststorun != "none":
        startrun="testim --report-file test-results.xml --name '"
        postfixtest="'"
    else:
        startrun="testim --report-file test-results.xml"

#cypress
#https://github.com/bahmutov/cypress-select-tests

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
        if sys.argv[k] == "--startrun":
            startrun = sys.argv[k+1]
        if sys.argv[k] == "--prefixtest":
            prefixtest = sys.argv[k+1]
        if sys.argv[k] == "--postfixtest":
            postfixtest = sys.argv[k+1]
        if sys.argv[k] == "--testseparator":
            testseparator = sys.argv[k+1]
        if sys.argv[k] == "--testseparatorend":
            testseparatorend = sys.argv[k+1]
        if sys.argv[k] == "--endrun":
            endrun = sys.argv[k+1]
        if sys.argv[k] == "--additionalargs":
            additionalargs = sys.argv[k+1]
        if sys.argv[k] == "--fail":
            fail = sys.argv[k+1]
        if sys.argv[k] == "--commitId":
            commitId = sys.argv[k+1]
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
        if sys.argv[k] == "--help":
            echo("please see url for more details on this script and how to execute your tests with appsurify - https://github.com/Appsurify/AppsurifyCIScript")

if url[-1:] == "/":
    url = url[:-1]
    echo("url = "+ url)

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

if commitId == "":
    commitId=runcommand("git log -1 --pretty=\"%H\"")
    print("commit id = " + commitId)

#git branch | grep \* | cut -d ' ' -f2
#git rev-parse --abbrev-ref HEAD
#https://stackoverflow.com/questions/6245570/how-to-get-the-current-branch-name-in-git

if branch == "":
    branch=runcommand("git rev-parse --abbrev-ref HEAD")
    print("branch = " + branch)

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

#if [[ $teststorun == "" ]] ; then echo "no teststorun specified" ; exit 1 ; fi
#if [[ $startrun == "" ]] ; then echo "no command used to start running tests specified" ; exit 1 ; fi

####example RunTestsWithAppsurify.sh --url "http://appsurify.dev.appsurify.com" --apikey "MTpEbzhXQThOaW14bHVQTVdZZXNBTTVLT0xhZ00" --project "Test" --testsuite "Test" --report "report" --teststorun "all" --startrun "mvn -tests" 
#example RunTestsWithAppsurify.sh --url "http://appsurify.dev.appsurify.com" --apikey "MTpEbzhXQThOaW14bHVQTVdZZXNBTTVLT0xhZ00" --project "Test" --testsuite "Test" --report "report" --teststorun "all" --startrun "C:\apache\apache-maven-3.5.0\bin\mvn tests " 
#./RunTestsWithAppsurify.sh --url "https://demo.appsurify.com" --apikey "MTU6a3Q1LUlTU3ZEcktFSTFhQUNoYy1DU3pidkdz" --project "Spirent Demo" --testsuite "Unit" --report "c:\testresults\GroupedTests1.xml" --teststorun "all" --commitId "44e9b51296e41e044e45b81e0ef65e9dc4c3bc23"
#python RunTestsWithAppsurify.py --url "http://appsurify.dev.appsurify.com" --apikey "MTpEbzhXQThOaW14bHVQTVdZZXNBTTVLT0xhZ00" --project "Test" --testsuite "Test"

run_id=""

#$url $apiKey $project $testsuite $fail $additionalargs $endrun $testseparator $postfixtest $prefixtest $startrun $fullnameseparator $fullname $failfast $maxrerun $rerun $importtype $teststorun $reporttype $report $commitId $run_id
echo("Getting tests to run")

valuetests=""
finalTestNames=""

if teststorun == "all":
    execute_tests("")

if teststorun == "none":
    push_results()

testtypes=[]

if "high" in teststorun
    testtypes.append(1)
if "medium" in teststorun
    testtypes.append(2)
if "low" in teststorun
    testtypes.append(3)
if "unassigned" in teststorun
    testtypes.append(4)

####start loop
for i in testtypes:
    get_and_run_tests(i)

if failfast == "false" and rerun == "true":
    rerun_tests()

