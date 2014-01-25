from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.test import LiveServerTestCase


class AdminTest(LiveServerTestCase):

    # load fixtures
    fixtures = ['ft/fixtures/admin.json']

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.set_page_load_timeout(5)

    def tearDown(self):
        self.browser.quit()

    def test_admin_site(self):

        self.browser.get(self.live_server_url + '/admin/')

        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)

        # users type in username and password and presses enter
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('admin')
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('password')
        password_field.send_keys(Keys.RETURN)

        #login creds correct, and user is redirect to admin home
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Site administration', body.text)

        # user clicks on the Users link
        user_link = self.browser.find_elements_by_link_text('Users')
        user_link[0].click()

        # user verifies that user live@forever.com is present

        table = self.browser.find_element_by_tag_name('table')

        self.assertIn('live@forever.com', table.text)

    def test_create_contact_admin(self):
        self.browser.get(self.live_server_url + '/admin/')
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('admin')
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('password')
        password_field.send_keys(Keys.RETURN)

        sleep(15)
        # user verifies that user_contacts is present
        body = self.browser.find_element_by_tag_name('body')

        self.assertIn('User_Contacts', body.text)
