from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.test import LiveServerTestCase


class UserContactTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def name_key(self, name, keys):
        self.browser.find_element_by_name(name).send_keys(keys)

    def test_create_contact(self):
        # user opens web browser, navigates to home page
        self.browser.get(self.live_server_url + "/")

        # user clicks on Persons link
        add_link = self.browser.find_elements_by_link_text('Add Contact')
        add_link[0].click()

        self.name_key('first_name', "Bill")
        self.name_key('last_name', "Smith")
        self.name_key('email', "bill@example.com")
        self.name_key('address', "123 Fake St")
        self.name_key('city', "Our Town")
        self.name_key('state', "NV")
        self.name_key('country', "USA")
        self.name_key('number', "12345")

        # click save
        self.browser.find_element_by_css_selector(
            "input[value='Add']").click()

        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('bill@example.com', body.text)

    def test_create_contact_error(self):
        # open web browse, navigates to home page
        self.browser.get(self.live_server_url + "/")

        # click on the Persons link
        add_link = self.browser.find_elements_by_link_text('Add Contact')
        add_link[0].click()

        self.name_key('first_name', "Bob@")
        self.name_key('last_name', "Smit@h")
        self.name_key('email', "bill@example.com")
        self.name_key('address', "123 Fake St")
        self.name_key('city', "Our Town")
        self.name_key('state', "NV")
        self.name_key('country', "USA")
        self.name_key('number', "12345")

        # click save
        self.browser.find_element_by_css_selector(
            "input[value='Add']").click()

        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Invalid', body.text)


class AdminTest(LiveServerTestCase):

    # load fixtures
    fixtures = ['ft/fixtures/admin.json']

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)
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

        # user verifies that user_contacts is present
        body = self.browser.find_elements_by_tag_name('body')

        self.assertIn('User_Contacts', body[0].text)

        # user clicks on the Persons link
        persons_links = self.browser.find_elements_by_link_text('Persons')
        persons_links[0].click()

        # user clicks on the Add person link
        add_person_link = self.browser.find_element_by_link_text('Add person')
        add_person_link.click()

        # user fills out the form
        self.browser.find_element_by_name('first_name').send_keys('Joe')
        self.browser.find_element_by_name('last_name').send_keys('Smith')
        self.browser.find_element_by_name('email').send_keys('joe@example.com')
        self.browser.find_element_by_name('address').send_keys('123 Fake St')
        self.browser.find_element_by_name('city').send_keys('Fake Town')
        self.browser.find_element_by_name('state').send_keys('CA')
        self.browser.find_element_by_name('country').send_keys('USA')

        # user clicks the save button
        self.browser.find_element_by_css_selector(
            "input[value='Save']").click()

        # the Person is added
        body = self.browser.find_elements_by_tag_name('body')
        self.assertIn('Smith, Joe', body[0].text)

        # back to admin home
        home_link = self.browser.find_element_by_link_text('Home')
        home_link.click()

        # go to Phones link
        phone_links = self.browser.find_elements_by_link_text('Phones')
        phone_links[0].click()

        # click add phone
        add_phone_link = self.browser.find_elements_by_link_text('Add phone')
        add_phone_link[0].click()

        # find person in dropdown
        el = self.browser.find_element_by_name("person")
        for option in el.find_elements_by_tag_name('option'):
            if option.text == 'Smith, Joe':
                option.click()

        # add phone number
        self.browser.find_element_by_name('number').send_keys("12345000")

        # click save
        self.browser.find_element_by_css_selector(
            "input[value='Save']").click()

        # see that the number has been added
        body = self.browser.find_elements_by_tag_name('body')
        self.assertIn('12345000', body[0].text)

        # logout
        self.browser.find_element_by_link_text('Log out').click()
        body = self.browser.find_elements_by_tag_name('body')
        self.assertIn('quality time', body[0].text)
