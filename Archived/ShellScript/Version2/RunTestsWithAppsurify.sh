f#!/bin/bash -x
urlencode() {
    # urlencode <string>

    local length="${#1}"
    for (( i = 0; i < length; i++ )); do
        local c="${1:i:1}"
        case $c in
            [a-zA-Z0-9.~_-:/]) printf "$c" ;;
            *) printf '%%%x' \'"$c" ;;
        esac
    done
}


maxtests=1000000 #default 10000000
fail="newdefects, reopeneddefects" #default new defects and reopened defects  #options newdefects, reopeneddefects, flakybrokentests, newflaky, reopenedflaky, failedtests, brokentests
additionalargs="" #default ''
endrun="" #default ''
testseparator="" #default ' '
postfixtest="" #default ''
prefixtest="" #default ''
fullnameseparator=" " #default ' '
fullname="false" #default false
failfast="false" #defult false
maxrerun=3 #default 3
rerun="true" #default false
importtype="junit" #default junit
reporttype="directory" #default directory other option file, when directory needs to end with /
teststorun="all" #options include - high, medium, low, unassigned, ready, open, none
deletereports="false" #options true or false, BE CAREFUL THIS WILL DELETE THE SPECIFIC FILE OR ALL XML FILES IN THE DIRECTORY
#startrun needs to end with a space sometimes
#endrun needs to start with a space sometimes
commitId=""
scriptlocation="./"
branch=""
#runfrequency="single" #options single for single commits, lastrun for all commits since the last run, betweeninclusive or betweenexclusive for all commits between two commits either inclusive or exclusive
runfrequency="single" #options single for single commits, multiple for when there have been multiple commits since the last test run.
fromcommit=""
repository="git"
scriptlocation="./"
generatefile="false"
template="none"
addtestsuitename="false"
addclassname="false"
#--testsuitesnameseparator and classnameseparator need to be encoded i.e. # is %23


########
#Templates
########



while [ "$1" != "" ]; do
    case $1 in
        -d | --runtemplate )       shift
                                   runtemplate=$1
                                   ;;
        -d | --testtemplate )          shift
                                   testtemplate=$1
                                   ;;
    esac
    shift
done

#####Test Run Templates######

if [[ $runtemplate == "prioritized tests with unassigned" ]] ; then
teststorun="high,medium,unassigned"
; fi

if [[ $runtemplate == "prioritized tests without unassigned" ]] ; then
teststorun="high,medium,unassigned"
; fi

if [[ $runtemplate == "no tests" ]] ; then
teststorun="none"
; fi

if [[ $testtemplate == "all tests" ]] ; then
teststorun="all"
fail="newdefects, reopeneddefects, failedtests, brokentests"
; fi


while [ "$1" != "" ]; do
    case $1 in
        -t | --teststorun )    shift
                               teststorun=$1
                               ;;
    esac
    shift
done

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

if [[ $testtemplate == "sahi ant" ]] ; then
    generatesfile="true"
    testseparator=","
    addtestsuitename=true
    testsuitesnameseparator=%23
    generatefile="sahi"
    if [[ $teststorun != "all" && $teststorun != "none"]] ; then
    startrun="ant -f "
    else
    startrun="ant -f "
    ; fi
; fi

#set endrun to being final command for test runner i.e. browser etc
if [[ $testtemplate == "sahi testrunner" ]] ; then
    generatesfile="true"
    testseparator=","
    addtestsuitename=true
    testsuitesnameseparator=%23
    generatefile="sahi"
    if [[ $teststorun != "all" && $teststorun != "none"]] ; then
    startrun="testrunner temp.dd.csv"
    else
    startrun="testrunner"
    ; fi
; fi

if [[ $testtemplate == "mvn" ]] ; then
    testseparator=","
    addtestsuitename=true
    testsuitesnameseparator=%23
    if [[ $teststorun != "all" && $teststorun != "none"]] ; then
    startrun="mvn -Dtest="
    endrun="test"
    else
    startrun="mvn test"
    ; fi
    report="/target/surefire-reports/"
    reporttype="directory"
; fi

if [[ $testtemplate == "rspec" ]] ; then
    testseparator=" -e '"
    #addtestsuitename=true
    #testsuitesnameseparator=%23
    if [[ $teststorun != "all" && $teststorun != "none"]] ; then
    startrun="rspec --format RspecJunitFormatter --out rspec.xml -e '"
    postfixtest="'"
    else
    startrun="rspec --format RspecJunitFormatter --out rspec.xml"
    ; fi
    reporttype="file"
    report="rspec.xml"
; fi

#startrun should be how your tests are executed i.e. java -jar robotframework.jar or robot
#then -x robot.xml to create the output file
#then --test ' if you are running specific tests
#endrun should be the location of your tests
if [[ $testtemplate == "robotframework" ]] ; then
    testseparator=" --test '"
    postfixtest="'"
    reporttype="file"
    report="robot.xml"
; fi

#mocha
#install https://www.npmjs.com/package/mocha-junit-reporter
#https://github.com/mochajs/mocha/issues/1565
if [[ $testtemplate == "mocha" ]] ; then
    testseparator="|"
    reporttype="file"
    report="test-results.xml"
    if [[ $teststorun != "all" && $teststorun != "none"]] ; then
    startrun="mocha test --reporter mocha-junit-reporter -g "
    postfixtest="$"
    prefixtest="^"
    else
    startrun="mocha test --reporter mocha-junit-reporter "
    ; fi
; fi

#pytest
#https://stackoverflow.com/questions/36456920/is-there-a-way-to-specify-which-pytest-tests-to-run-from-a-file
if [[ $testtemplate == "pytest" ]] ; then
    testseparator=" or "
    reporttype="file"
    report="test-results.xml"
    if [[ $teststorun != "all" && $teststorun != "none"]] ; then
    startrun="python -m pytest --junitxml=test-results.xml -k '"
    endrun="'"
    else
    startrun="python -m pytest --junitxml=test-results.xml"
    ; fi
; fi

#testim
#https://help.testim.io/docs/the-command-line-cli
if [[ $testtemplate == "testim" ]] ; then
    testseparator=" --name '"
    reporttype="file"
    report="test-results.xml"
    if [[ $teststorun != "all" && $teststorun != "none"]] ; then
    startrun="testim --report-file test-results.xml --name '"
    postfixtest="'"
    else
    startrun="testim --report-file test-results.xml"
    ; fi
; fi

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

while [ "$1" != "" ]; do
    case $1 in
        -u | --url )           shift
                               url=$1
                               ;;
        -a | --apikey )        shift
                               apiKey=$1
                               ;;
        -p | --project )       shift
                               project=$1
                               ;;
        -ts | --testsuite )    shift
                               testsuite=$1
                               ;;
        -r | --report )        shift
                               report=$1
                               ;;
        -rt | --reporttype )   shift
                               reporttype=$1
                               ;;
        -t | --teststorun )    shift
                               teststorun=$1
                               ;;
        -i | --importtype )    shift
                               importtype=$1
                               ;;
        -r | --addtestsuitename )       shift
                                        addtestsuitename=$1
                                        ;;
        -rt | --testsuitesnameseparator )   shift
                                            testsuitesnameseparator=$1
                                            ;;
        -t | --addclassname )   shift
                                addclassname=$1
                                ;;
        -i | --classnameseparator )     shift
                                        classnameseparator=$1
                                        ;;
        -re | --rerun )        shift
                               rerun=$1
                               ;;
        -mr | --maxrerun )     shift
                               maxrerun=$1
                               ;;
        -ff | --failfast )     shift
                               failfast=$1
                               ;;
        -fn | --fullname )     shift
                               fullname=$1
                               ;;
        -fs | --fullnameseparator )         shift
                                            fullnameseparator=$1
                                            ;;
        -sr | --startrun )     shift
                               startrun=$1
                               ;;
        -pr | --prefixtest )   shift
                               prefixtest=$1
                               ;;
        -po | --postfixtest )  shift
                               postfixtest=$1
                               ;;
        -se | --testseparator )         shift
                                        testseparator=$1
                                        ;;
        -se | --testseparatorend )      shift
                                        testseparatorend=$1
                                        ;;
        -er | --endrun )       shift
                               endrun=$1
                               ;;
        -aa | --additionalargs )    shift
                                    additionalargs=$1
                                    ;;
        -f | --fail )          shift
                               fail=$1
                               ;;
        -d | --deletereports ) shift
                               deletereports=$1
                               ;;
        -d | --commitId )      shift
                               commitId=$1
                               ;;
        -d | --branch )        shift
                               branch=$1
                               ;;
        -d | --maxtests )      shift
                               maxtests=$1
                               ;;
        -d | --scriptlocation )     shift
                                    scriptlocation=$1
                                    ;;
        -d | --runfrequency )       shift
                                    runfrequency=$1
                                    ;;
        -d | --fromcommit )         shift
                                    fromcommit=$1
                                    ;;
        -d | --repository )         shift
                                    repository=$1
                                    ;;
        -g | --generatefile )       shift
                                    generatefile=$1
                                    ;;
        -h | --help )          echo "please see url for more details on this script and how to execute your tests with appsurify - https://github.com/Appsurify/AppsurifyCIScript"
                               exit 1
                               ;;
    esac
    shift
done

testsuiteencoded=$(urlencode "$testsuite")
projectencoded=$(urlencode "$project")

if [[ $commitId == "" ]] ; then commitId=`git log -1 --pretty="%H"` ; fi
#git branch | grep \* | cut -d ' ' -f2
#git rev-parse --abbrev-ref HEAD
#https://stackoverflow.com/questions/6245570/how-to-get-the-current-branch-name-in-git
if [[ $branch == "" ]] ; then branch=`git rev-parse --abbrev-ref HEAD` ; fi



if [[ $report == *.xml* ]] ; then reporttype="file" ; fi
if [[ $report == *.Xml* ]] ; then reporttype="file" ; fi
if [[ $report == *.XML* ]] ; then reporttype="file" ; fi
if [[ $report != *.* ]] ; then reporttype="directory" ; fi
echo $reporttype

if [[ $url == "" ]] ; then echo "no url specified" ; exit 1 ; fi
if [[ $apiKey == "" ]] ; then echo "no apikey specified" ; exit 1 ; fi
if [[ $project == "" ]] ; then echo "no project specified" ; exit 1 ; fi
if [[ $testsuite == "" ]] ; then echo "no testsuite specified" ; exit 1 ; fi
if [[ $report == "" ]] ; then echo "no report specified" ; exit 1 ; fi
if [[ $runfrequency == "betweeninclusive" && $fromcommit == "" ]] ; then echo "no from commit specified and runfrequency set to betweeninclusive" ; exit 1 ; fi
if [[ $runfrequency == "betweenexclusive" && $fromcommit == "" ]] ; then echo "no from commit specified and runfrequency set to betweenexclusive" ; exit 1 ; fi
#if [[ $teststorun == "" ]] ; then echo "no teststorun specified" ; exit 1 ; fi
#if [[ $startrun == "" ]] ; then echo "no command used to start running tests specified" ; exit 1 ; fi

####example RunTestsWithAppsurify.sh --url "http://appsurify.dev.appsurify.com" --apikey "MTpEbzhXQThOaW14bHVQTVdZZXNBTTVLT0xhZ00" --project "Test" --testsuite "Test" --report "report" --teststorun "all" --startrun "mvn -tests" 
#example RunTestsWithAppsurify.sh --url "http://appsurify.dev.appsurify.com" --apikey "MTpEbzhXQThOaW14bHVQTVdZZXNBTTVLT0xhZ00" --project "Test" --testsuite "Test" --report "report" --teststorun "all" --startrun "C:\apache\apache-maven-3.5.0\bin\mvn tests " 
#./RunTestsWithAppsurify.sh --url "https://demo.appsurify.com" --apikey "MTU6a3Q1LUlTU3ZEcktFSTFhQUNoYy1DU3pidkdz" --project "Spirent Demo" --testsuite "Unit" --report "c:\testresults\GroupedTests1.xml" --teststorun "all" --commitId "44e9b51296e41e044e45b81e0ef65e9dc4c3bc23"

run_id=""


echo $commitId



#$url $apiKey $project $testsuite $fail $additionalargs $endrun $testseparator $postfixtest $prefixtest $startrun $fullnameseparator $fullname $failfast $maxrerun $rerun $importtype $teststorun $reporttype $report $commitId $run_id
echo "Getting tests to run"
. "$scriptlocation"GetAndRunTests.sh