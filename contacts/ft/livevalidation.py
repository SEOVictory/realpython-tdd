from os.path import dirname, realpath

from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from django.test import LiveServerTestCase


class LiveValidationTestCase(LiveServerTestCase):
    """
    run tests on ajaxy live validation
    """

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def key(self, name, keys):
        self.by('name', name).send_keys(keys)

    def by(self, what, key):
        get = getattr(self.browser, 'find_element_by_' + what)
        return get(key)

    def test_validation_avatar_appears(self):
        self.browser.get(self.live_server_url + "/add")
        self.key('first_name', 'a')

        self.assertIsInstance(
            self.by('id', 'validate_avatar_id_first_name'),
            WebElement)

        self.assertEqual(
            self.by('id', 'validate_avatar_id_first_name').tag_name,
            'span')
