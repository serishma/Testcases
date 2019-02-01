import time
from selenium import webdriver
import paramiko
import mysql.connector


class Commonfunctions(object):

    def __init__(self, selenium_=False):
        if selenium_:
            self.driver_chrome = webdriver.Chrome(executable_path="C:\driver_selenium\chromedriver.exe")
            self.driver_firefox = webdriver.firefox

    def setup_chrome(self, url):
        '''
        chrome browser setup
        :param url: <str>
        :return:
        '''

        self.driver_chrome.maximize_window()
        self.driver_chrome.get(url)
        print(self.driver_chrome.title)
        print("webdriver execution")
        return self.driver_chrome

    def login_to_cjp_portal(self, user_name, cjp_password, driver):
        '''
        Login for CJP Portal
        :param user_name: <str>
        :param cjp_password: <str>
        :param driver: <object>
        :return:
        '''

        username = driver.find_element_by_id("username")
        username.clear()
        username.send_keys(user_name)
        password = driver.find_element_by_id("password")
        password.clear()
        password.send_keys(cjp_password)
        driver.find_element_by_name("submit").click()
        time.sleep(6)
        assert "My Dashboard" in driver.title, "Login Unsuccessfull"
        print("Login Successful")

    def logout_cjp_portal(self):
        '''
        Logout for CJP Portal
        :return: None
        '''

        driver = self.driver
        driver.switch_to_default_content()
        driver.find_element_by_xpath("//span[@class='caret']").click()
        driver.find_element_by_xpath("//a[@id='logoutLink']").click()
        time.sleep(5)

    def ssh_to_cjp_server_and_validate(self, cmd, dict_params):
        '''
        making SSH connection, executing commands and getting result
        :param cmd: <str>
        :param dict_params: <dictionary>
        :return: <str>
        '''

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(dict_params['hostname'], dict_params['port'], dict_params['username'],
                           dict_params['password'])
        stdin, stdout, stderr = ssh_client.exec_command(cmd)
        outlines = stdout.readlines()
        resp = ''.join(outlines)
        return resp

    def cjp_db_connection_fetching_data(self, query, query_params, connection_params):
        '''
        Making MYSQL Database connection, querying and getting result
        :param query: <str>
        :param query_params: <str>
        :param connection_params: <str>
        :return: <list>
        '''

        connection = mysql.connector.connect(
            host=connection_params['hostname'],
            user=connection_params['username'],
            passwd=connection_params['password'],
            database=connection_params['database'],
        )
        try:
            cursor = connection.cursor()
            cursor.execute(query, query_params)
            result = cursor.fetchall()
        except Exception as e:
            print( str(e) )
        return result

    def get_columnnames_for_tablename(self, columnsresult):
        '''
        getting column names list for the requested tablename in sql
        :param columnsresult: <list>
        :return: <str>
        '''

        keys = []
        for columns in columnsresult:
            keys.append(columns[0])
        return keys

    def optimizing_query_result(self, queryresult):
        '''
        optimizing the query result in to list
        :param queryresult: <list>
        :return: <str>
        '''

        values = []
        for columndata in queryresult:
            columndata = columndata
        i = 0
        while i < (len(columndata)):
            values.append(columndata[i])
            i += 1
        return values

    def xpath_query_to_cjp(self, xpath, attribute="*"):
        '''Check data DB by using the Xpath Query'''

        driver = self.driver
        driver.find_element_by_xpath('//textarea[@name="xpath"]').clear()
        driver.find_element_by_xpath('//textarea[@name="xpath"]').send_keys(xpath)
        driver.find_element_by_xpath('//input[@name="attributes"]').clear()
        driver.find_element_by_xpath('//input[@name="attributes"]').send_keys(attribute)
        driver.find_element_by_xpath('//input[@name="Query"]').click()

        xml_html_data = driver.page_source
        return xml_html_data

    def tearDown(self):
        ''' close the browser '''
        self.driver.quit()


