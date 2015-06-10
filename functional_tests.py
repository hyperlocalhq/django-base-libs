from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.base_url = 'http://localhost:8000'

    def tearDown(self):
        self.browser.quit()

    def test_can_open_homepage(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get(self.base_url)

        # She notices the page title and header mention to-do lists
        self.assertIn('Creative City Berlin', self.browser.title)

if __name__ == '__main__':
    unittest.main()
