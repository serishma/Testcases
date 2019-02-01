*** Settings  ***
Library    ../PHC_Automation/Library/Provisioning/password_policy.py
Library    ../PHC_Automation/Library/Provisioning/base.py
Library    ../PHC_Automation/Library/Provisioning/xml_conv.py
Library    ../PHC_Automation/Library/Provisioning/utils.py
Library     ../PHC_Automation/TestCases/TestCases.py        WITH NAME    class

Default Tags    Prov_Broker_Testing

*** Keywords ***
print1 class
        class.xpath_test009

*** Test Cases ***

TESTCASE1: xpath_test009
	print1 class
        [Tags]    Prov_Broker_Testing


