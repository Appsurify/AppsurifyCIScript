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
rerun="false" #default false
importtype="junit" #default junit
reporttype="directory" #default directory
teststorun="all" #options include - high, medium, low, unassigned, ready, open, none
deletereports="false" #options true or false, BE CAREFUL THIS WILL DELETE THE SPECIFIC FILE OR ALL XML FILES IN THE DIRECTORY
#startrun needs to end with a space sometimes
#endrun needs to start with a space sometimes
commitId=""
scriptlocation="./"



###############
#atm rerunning tests and fast fail don't work together very well
##########


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
        -d | --maxtests )      shift
                               maxtests=$1
                               ;;
        -d | --scriptlocation )     shift
                                    scriptlocation=$1
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

if [[ $report == *.xml* ]] ; then reporttype="file" ; fi
if [[ $report == *.Xml* ]] ; then reporttype="file" ; fi
if [[ $report == *.XML* ]] ; then reporttype="file" ; fi

if [[ $url == "" ]] ; then echo "no url specified" ; exit 1 ; fi
if [[ $apiKey == "" ]] ; then echo "no apikey specified" ; exit 1 ; fi
if [[ $project == "" ]] ; then echo "no project specified" ; exit 1 ; fi
if [[ $testsuite == "" ]] ; then echo "no testsuite specified" ; exit 1 ; fi
if [[ $report == "" ]] ; then echo "no report specified" ; exit 1 ; fi
#if [[ $teststorun == "" ]] ; then echo "no teststorun specified" ; exit 1 ; fi
#if [[ $startrun == "" ]] ; then echo "no command used to start running tests specified" ; exit 1 ; fi

####example RunTestsWithAppsurify.sh --url "http://appsurify.dev.appsurify.com" --apikey "MTpEbzhXQThOaW14bHVQTVdZZXNBTTVLT0xhZ00" --project "Test" --testsuite "Test" --report "report" --teststorun "all" --startrun "mvn -tests" 
#example RunTestsWithAppsurify.sh --url "http://appsurify.dev.appsurify.com" --apikey "MTpEbzhXQThOaW14bHVQTVdZZXNBTTVLT0xhZ00" --project "Test" --testsuite "Test" --report "report" --teststorun "all" --startrun "C:\apache\apache-maven-3.5.0\bin\mvn tests " 


run_id=""


echo $commitId

#$url $apiKey $project $testsuite $fail $additionalargs $endrun $testseparator $postfixtest $prefixtest $startrun $fullnameseparator $fullname $failfast $maxrerun $rerun $importtype $teststorun $reporttype $report $commitId $run_id
echo "Getting tests to run"
. "$scriptlocation"GetAndRunTests.sh