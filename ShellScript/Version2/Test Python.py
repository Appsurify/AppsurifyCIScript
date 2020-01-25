import json
import requests

def get_tests(testpriority):
    print("getting test set "+ str(testpriority))
    tests=""
    valuetests=""
    finalTestNames=""
    print("runfrequency = " + runfrequency)
    print("apikey = " + apikey)
    print("importtype = " + importtype)
    print("commitId = "+ commitId)
    print("projectencoded = "+ projectencoded)
    print("testsuiteencoded = "+ testsuiteencoded)
    print("testpriority = "+ str(testpriority))
    print("addclassname = "+ addclassname)
    print("addtestsuitename = "+ addtestsuitename)
    print("testsuitesnameseparator = "+ testsuitesnameseparator)
    print("classnameseparator = "+ classnameseparator)
    print("repository = "+ repository)
    print("url = "+ url)
    

    #apiendpoint=f"{url}/api/external/prioritized-tests/?project_name={projectencoded}&priority={testpriority}&testsuitename_separator={testsuitesnameseparator}&testsuitename={addtestsuitename}&classname={addclassname}&classname_separator={classnameseparator}&test_suite_name={testsuiteencoded}&first_commit={commitId}"
    #headers={'token': apikey}
    headers = {
        'token': apikey,
    }

    params = {
        'name_type': importtype,
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

    print(params)

    response = requests.get(url+'/api/external/prioritized-tests/', headers=headers, params=params)
    print("request sent to get tests")
    print(response.status_code)

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
        print("here")
        testset = json.loads(response.content.decode('utf-8'))
        return testset
    else:
        print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content))
    return None

runfrequency = "multiple"
apikey = "MTpEbzhXQThOaW14bHVQTVdZZXNBTTVLT0xhZ00"
importtype = "junit"
commitId = "991dd559cb02a9731c18b41fdd5b7ad2051bbf64"

projectencoded = "jsoup2"
testsuiteencoded = "Unit"
testpriority = 5
addclassname = "false"
addtestsuitename = "true"
testsuitesnameseparator = "%23"
classnameseparator = ""
repository = "git"
url = "https://appsurify.test.appsurify.com"
branch = "master"
get_tests(5)