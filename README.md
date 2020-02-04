# Appsurify CI Script

## Index
- [Available Arguments](#available_arguments)
  - [Required Arguments](#required_arguments)
  - [Recommended Arguments](#recommended_arguments)
- [Test Template](#testtemplate)
- [Example Usage](#example_usage)
- [Additional Arguments](#additional_arguments)
  - [Test Selection Arguments](#test_selection_arguments)
  - [Build Failure Arguments](#build_failure_arguments)
  - [Test Command Arguments](#test_command_arguments)
  - [Test Format Arguments](#test_format_arguments)
  - [Report Arguments](#report_arguments)
  - [Commit Arguments](#commit_arguments)
  - [Test Execution Details](#test_execution_arguments)
- [Tests To Run](#teststorun)

## <a id="available_arguments"></a>Available Arguments
 
### <a id="required_arguments"></a>Required Arguments 

| argument | options |
| --- | --- |
| apikey | Apikey from appsurify |
| url | Url of the appsurify instance i.e. "https://dummy.appsurify.com" do not end with a / |
| project | Name of the project |
| testsuite | Name of the testsuite |

### <a id="recommended_arguments"></a>Recommended Arguments
| argument | options |
| --- | --- |
| runtemplate  | Options - all tests (defaults to fail on all failures, unless overwritten), no tests (will fail on any failures, unless overwritten), prioritized tests with unassigned (will only fail on new or reopened defects, unless overwritten), prioritized tests without unassigned (will only fail on new or reopened defects, unless overwritten) |
| testtemplate | Options - mvn, sahi testrunner, sahi ant, testim, mocha, pytest, rspec, robotframework, cyprus, mstest, katalon, opentest.  See [below](#testtemplate) for usage details |
| testtemplatearg1 | Additional argument for the specified test template |
| testtemplatearg2 | Additional argument for the specified test template |
| testtemplatearg3 | Additional argument for the specified test template |

## <a id="testtemplate"></a>Parameter Details - testtemplate

<details>
  <summary>Click to expand for test template parameter details/options</summary>

### Maven
#### Parameter value - "mvn"
The following values are set when this testtemplate is selected
- testseparator=","
- addtestsuitename="true"
- testsuitesnameseparator="%23"
- startrunspecific="mvn -Dtest="
- endrunspecific="test"
- startrunall="mvn test"
- report="./target/surefire-reports/"
- reporttype="directory"

### Testim
#### Parameter value - "testim"
The following values are set when this testtemplate is selected
- testseparator=" --name '"
- reporttype="file"
- report="test-results.xml"
- startrunspecific="testim --report-file test-results.xml --name '"
- postfixtest="'"
- startrunall="testim --report-file test-results.xml"

### Rspec
#### Parameter value - "rspec"
#### Required Config
The following must be installedhttps://github.com/sj26/rspec_junit_formatter
The following values are set when this testtemplate is selected
- testseparator=" "
- startrunspecific="rspec --format RspecJunitFormatter --out rspec.xml "
- prefixtest = "-e '"
- postfixtest="'"
- startrunall="rspec --format RspecJunitFormatter --out rspec.xml"
- reporttype="file"
- report="rspec.xml"

### Sahi Ant
#### Parameter value - "sahi ant"
#### Required Config
Ensure junit report is set in the ant file - https://sahipro.com/docs/using-sahi/playback-desktop.html#Playback%20via%20ANT
- testtemplatearg1 - The report location set as per above
- testtemplatearg2 - The ant file to run all tests
- testtemplatearg3 - The ant file to the specific set of tests

The following values are set when this testtemplate is selected
- testseparator=","
- addtestsuitename="true"
- testsuitesnameseparator="%23"
- generatefile="sahi"
- startrunall="ant -f "+testtemplatearg2
- startrunspecific="ant -f "testtemplatearg3
- report = testtemplatearg1

### Sahi Testrunner
#### Parameter value - "sahi testrunner"
#### Required Config
Set the Sahi runner to create a junit report - https://sahipro.com/docs/using-sahi/sahi-reports.html
The following values must be supplied
- testtemplatearg1 - The report location set as per above
- testtemplatearg2 - The command to run all tests

The following values are set when this testtemplate is selected
- testseparator=","
- addtestsuitename="true"
- testsuitesnameseparator="%23"
- generatefile="sahi"
- startrunspecific="testrunner temp.dd.csv"
- startrunall="testrunner " + testtemplatearg2
- report=testtemplatearg1

### Robot Framework
#### Parameter value - "robotframework"
#### Required Config
- testtemplatearg1 - The execution command used to start robotframework tests i.e. java -jar robotframework.jar 
- testtemplatearg2 - The location of your tests
- testtemplatearg3 - Report location

The following values are set when this testtemplate is selected
- testseparator=" --test '"
- postfixtest="'"
- reporttype="file"
- report=testtemplatearg3
- startrunall=testtemplatearg1+" -x "+testtemplatearg3+" "
- endrunall=testtemplatearg2
- startrunspecific=testtemplatearg1+" -x "+testtemplatearg3+" "
- endrunall=testtemplatearg2

### Mocha
#### Parameter value - "mocha"
#### Required Config
Note the following plugin must be installed to generate the junit report file - https://www.npmjs.com/package/mocha-junit-reporter

The following values are set when this testtemplate is selected
- testseparator="|"
- reporttype="file"
- report="test-results.xml"
- startrunspecific="mocha test --reporter mocha-junit-reporter -g "
- postfixtest="$"
- prefixtest="^"
- startrunall="mocha test --reporter mocha-junit-reporter "

### Pytest
#### Parameter value - "pytest"
The following values are set when this testtemplate is selected
- testseparator=" or "
- reporttype="file"
- report="test-results.xml"
- startrunspecific="python -m pytest --junitxml=test-results.xml -k '"
- endrunspecific="'"
- startrunall="python -m pytest --junitxml=test-results.xml"


### Cyprus
#### Parameter value - "cyprus"
#### Required Config
The following cyprus addon must be installed in order to specify the tests - https://github.com/bahmutov/cypress-select-tests

The following values are set when this testtemplate is selected
- testseparator="|"
- reporttype="file"
- report="results.xml"
- startrunspecific="cypress run --reporter junit --reporter-options mochaFile=result.xml grep="
- postfixtest="'"
- prefixtest="'"
- startrunall="cypress run --reporter junit --reporter-options mochaFile=result.xml"

### Mstest
#### Parameter value - "mstest"
The following values are set when this testtemplate is selected
- testseparator=","
- reporttype="file"
- startrunspecific="mstest /resultsfile:'" + testtemplatearg1 + "' /testcontainer:'" + testtemplatearg2 + "'" + "/tests:"
- postfixtest="'"
- prefixtest="'"
- startrunall="mstest /resultsfile:'" + testtemplatearg1 + "' /testcontainer:'" + testtemplatearg2 + "'"
- report=testtemplatearg1
- importtype="trx"

### Katalon
#### Parameter value - "katalon"
#### Required Config
- testtemplatearg1 - Report location
- testtemplatearg2 - Absolute path to project file
- testtemplatearg3 - Relative path from project to a created test suite with all tests added to it
- testtemplatearg4 - API Key

The following values are set when this testtemplate is selected
- testseparator=","
- reporttype="file"
- report = testtemplatearg1
- head_tail = os.path.split(testtemplatearg1) 
- report_folder = head_tail[0]
- report_file = head_tail[1]
- head_tail = os.path.split(testtemplatearg3) 
- startrunspecific="katalonc -noSplash -runMode=console -projectPath='" + testtemplatearg2 + "' -testSuitePath='" + "'" + os.path.join(head_tail[0], "temp.ts") + "' -apiKey='" + testtemplatearg4 +"' -reportFolder='" + report_folder + " -reportFileName='" + report_file + "'"
- startrunall="katalonc -noSplash -runMode=console -projectPath='" + testtemplatearg2 + "' -testSuitePath='" + "'" + testtemplatearg3 + "' -apiKey='" + testtemplatearg4 +"' -reportFolder='" + report_folder + " -reportFileName='" + report_file + "'"
- generatefile="katalon"

### Opentest
#### Parameter value - "opentest"
#### Required Config
- testtemplatearg1 - Report location
- testtemplatearg2 - Template of template with no tests - this template will be copied as temp.yaml and tests to be executed will be appended to this template
- testtemplatearg3 - Template to run with all tests

The following values are set when this testtemplate is selected
- testseparator=",,"
- reporttype="file"
- report = testtemplatearg1
- full_path = os.path.realpath(source)
- destination = os.path.join(os.path.dirname(full_path),"temp.yaml")
- startrunspecific="opentest session create --out '"+testtemplatearg1+ "' --template '" + destination + "' "
- startrunall="opentest session create --out '"+testtemplatearg1+ "' --template '" + testtemplatearg3 + "' "
- generatefile="opentest"

</details>

<details>
  <summary>Click to expand for additional test template configuration options</summary>

  ### Test Template Customization

In order to customize the way tests are run you can use the following parameters

| argument | options |
| --- | --- |
| startrunpostfix | appended to the startrun command |
| endrunprefix | prepended to the endrun command |
| endrunpostfix | appended to the endrun command |

Editing these will change the way tests are executed to the following: startrun + startrunpostfix + testlist + endrunprefix + endrun + endrunpostfix

</details>

## <a id="example_usage"></a>Example Usage

python RunTestsWithAppsurify.py --url "https://dummy.appsurify.com" --apikey "apikeyvalue" --project "Test" --testsuite "Test" --report "report --runtemplate "specific tests with unassigned" --testtemplate "mvn"

## <a id="additional_arguments"></a>Additional Arguments - For Customization

<details>
  <summary>Click to expand for details on additional arguments</summary>

### <a id="test_selection_arguments"></a>Test Selection Arguments

| argument | default | options/details |
| --- | --- | --- |
| teststorun | "all" | Defaults to "all" if runtemplate is not set.  Options include - high, medium, low, unassigned, ready, open, none.  Details below |
| maxtests | 10000000 | the maximum number of tests to run in each test execution set | 
| runfrequency | "multiple" | #options 'single' or 'multiple' determines if the prioritized tests should be for a single commit or mulltiple i.e. since the last test run |

### <a id="build_failure_arguments"></a>Build Failure Arguments 

| argument | default | options/details |
| --- | --- | --- |
| fail | newdefects, reopeneddefects | options newdefects, reopeneddefects, flakybrokentests, newflaky, reopenedflaky, failedtests, brokentests |
| rerun | "false" | whether failed tests should be rerun |
| maxrerun | 3 | the number of times failed tests should be rerun |
| failfast | "false" | whether after each set of test runs to determine if the build has failed (tests will still be rerun if this has been selected) |
| runtemplate | None | Options - all tests (defaults to fail on all failures, unless overwritten), no tests (will fail on any failures, unless overwritten), prioritized tests with unassigned (will only fail on new or reopened defects, unless overwritten), prioritized tests without unassigned (will only fail on new or reopened defects, unless overwritten) |

### <a id="test_command_arguments"></a>Test Command Arguments 

| argument | default | options/details |
| --- | --- | --- |
| testtemplate | None | Options - mvn, sahi testrunner, sahi ant, testim, mocha, pytest, rspec, robotframework.  See below for usage details |
| testtemplatearg1 | None | Additional argument for the specified test template |
| testtemplatearg2 | None | Additional argument for the specified test template |
| testtemplatearg3 | None | Additional argument for the specified test template |
| startrunall | None | Required if testtemplate is not set and runtemplate is all tests or teststorun is set to all.  Command to start the test run to execute all tests.  Details below |
| endrunall | None | Command to end the test run to execute all tests.  Details below |
| startrunspecific | None | Required if testtemplate is not set and teststorun is not all or none or testtemplate is not all tests or no tests.  Command to start the test run to execute specific tests.  Details below  |
| endrunspecific | None | Command to end the test run to execute specific tests |

### <a id="test_format_arguments"></a>Test Format Arguments 

| argument | default | options/details |
| --- | --- | --- |
| testseparator | "" | #string or character used to separate tests when creating the command to run a specific set of tests |  
| postfixtest | "" | #string to postpend to each test  when creating the command to run a specific set of tests |
| prefixtest | "" | string to prepend to each test  when creating the command to run a specific set of tests |
| addclassname | "false" | whether to include the classname when creating the command to run a specific set of tests |
| classnameseparator | " " | string or character to separate classname and testname when creating the command to run a specific set of tests |
| addtestsuitename | "false" | whether to include the testsuitename when creating the command to run a specific set of tests |
| testsuitenameseparator | " " | string or character to separate testsuitename and classname/testname when creating the command to run a specific set of tests |

### <a id="report_arguments"></a>Report Arguments 

| argument | default | options/details |
| --- | --- | --- |
| report | Required if testtemplate is not passed through as an argument.  Location of the reports generated by the test run. |
| deletereports | "false" | options true or false, BE CAREFUL THIS WILL DELETE THE SPECIFIC FILE OR ALL XML FILES IN THE DIRECTORY |
| importtype | "junit" | #options 'junit', 'nunit' or 'trx' |
| reporttype | "directory" | default directory must end with a /, will look for all importtype files in that directory |

### <a id="commit_arguments"></a>Commit Arguments 

| argument | default | options/details |
| --- | --- | --- |
| branch | 'git branch \| grep \\\* \| cut -d ' ' -f2' | The branch from which you would like to select the commits to get priorized tests for.  Will default to the value of 'git branch \| grep \\\* \| cut -d ' ' -f2' if not specified |
| commit | git log -1 --pretty="%H | commitId that this test run is for, if not supplied the script will use git log -1 --pretty="%H |

</details>

## <a id="test_execution_details"></a>Test Execution Details

<details>
  <summary>Click to expand for test execution details</summary>

### Execution Command

Note the execution arguments will automatically be set when using the testtemplate.

When executing all tests the following command is created: startrunall+startrunpostfix+endrunprefix+endrunall+endrunpostfix.  To execute all tests via maven the command 'mvn test' needs to be run.  To do this startrunall could be set to 'mvn test' or startrunall could be set to 'mvn ' and endrunall set to 'test'.  Please note spaces are required otherwise the command will not be properly formatted.

When executing specific tests the following command is created startrunspecific+startrunpostfix+specifictestlist+endrunprefix+endrunspecific+endrunpostfix  To execute specific tests via maven the command 'mvn -Dtests=<specifictestlist> test'.  To do this startrunspecific needs to be set to 'mvn -Dtests=' and endrunspecific set to ' test'.  For details on how specifictestlist is created see below.

### Specific Tests

To create the list of specific tests the ci script queries Appsurify for a list of tests.  For each test they may have an associated testsuite name and classname as often found in the xml junit report.  See below for an example.  The list of tests returned by the api may include the testsuitename and/or classname dependant on whether addtestsuitename, addclassname, testssuitenameseparator and classnameseparator are set.  If for example addtestsuitename="true", testsuitenameseparator="%23, addclassname="true", classnameseparator=%40 (note values need to be encoded via percent encoding https://en.wikipedia.org/wiki/Percent-encoding) the tests would be formatted as follows: testsuitename#classname@testname.

To create the list the arguments will be conbined in the following way: prefixtest+test+postfixtest
If there are multiple tests the arguments would be combined as follows: prefixtest+test+postfixtest+testseparator+prefixtest+test+postfixtest

Combining the above to run a specific set of tests using mvn the following arguments would need to be set: addtestsuitname="true", testsuiteseparator="%23", testseparator=",", startrunspecific='mvn -Dtests=' and endrunspecific =' test' which would cause the following command to be created "mvn -Dtest=testsuite#testname,testsuite#testname test

If however the tests needed to be in the format of 'run tests -test=test1 -test=test2 -test=test3' then the following arguments would be required: startrunspecific="run tests " and prefixtest="-test="

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<testsuites>
  <testsuite errors="0" failures="1" hostname="DESKTOP-16O0SVF" id="0" name="TestRun" package="junit" skipped="0" tests="1" time="0.16" timestamp="2018-06-07T06:22:50">
      <testcase classname="junit.TestRun" name="PassToFail" time="0.008">
        <failure message="failreason1" type="junit.framework.AssertionFailedError"> fails
        </failure>
      </testcase>
  </testsuite>
</testsuites>
```

</details>

## <a id="teststorun"></a>Parameter Details - teststorun  

| Option | Details |
| --- | --- |
| all tests | Will run all tests.  Will fail on any failure.  Recommended for nightly or weekly test executions |
| no tests | Will run no tests.  Will fail on any failure.  Recommended when starting with Appsurify to just upload data |
| prioritized tests with unassigned | Will run just high, medium and unassigned tests.  Will only fail the build on new/reopened defects.  Recommended for your most frequent run type i.e. per commit, nightly |
| prioritized tests without unassigned | Will run just high and medium tests.  Will only fail the build on new/reopened defects.  Recommended for long term use |

<details>
  <summary>Click to expand for further details</summary>

We recommend using the runtemplate parameter instead of using teststorun.  But for additional control on which tests to run you may change the teststorun field.  When doing so we recommend initially running all your tests and just pushing the results to Appsurify. To do this choose either "all" and use this script to run the tests, or choose none and use this script to just upload the results.

Once you have either selected the coverage of the tests or uploaded a number of test reults for Appsurify to learn from select Appsurify recommended and choose from the options where - high = most likely to fail, covers the exact change, medium = less likely to fail, covers the functional area or dependencies, low = very unlikely to fail, does not cover the change, unassigned = tests where Appsurify is unsure whether the coverage of these tests, ready defects = tests which have a defect associated with them which is ready for testing, open defects = tests which have a defect associated with them which is open.

</details>

## Examples

### Maven 
python RunTestsWithAppsurify.py --url "https://dummy.appsurify.com" --apikey "apikeyvalue" --project "Test" --testsuite "Test" --report "report --runtemplate "prioritized tests with unassigned" --testtemplate "mvn"


### Deprecated examples

<details>
  <summary>Click to expand for deprecated examples</summary>

#### Java All Tests
RunTestsWithAppsurify.sh --url "https://dummy.appsurify.com" --apikey "apikeyvalue" --project "Test" --testsuite "Test" --report "report" --teststorun "all" --startrun "mvn test" 

#### Java High Tests
RunTestsWithAppsurify.sh --url "https://dummy.appsurify.com" --apikey "apikeyvalue" --project "Test" --testsuite "Test" --report "report" --teststorun "high,medium" --startrun "mvn -Dtest=" --fullname "true" --fullnameseparator "#" --endrun " test" --testseparator ","


#### Rspec all tests
https://github.com/sj26/rspec_junit_formatter must be installed
Startrun="rspec --format RspecJunitFormatter --out rspec.xml"


#### Rspec specific tests
RunTestsWithAppsurify.sh --url "https://dummy.appsurify.com" --apikey "apikeyvalue" --project "Test" --testsuite "Test" --report "rspec.xml" --teststorun "high,medium" --startrun "rspec --format RspecJunitFormatter --out rspec.xml -e '" --endrun = "'" --testseparator "' -e '"
https://relishapp.com/rspec/rspec-core/docs/command-line/example-option

</details>