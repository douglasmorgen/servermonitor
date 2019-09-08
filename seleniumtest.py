import unittest
from selenium import webdriver
import pprint

class PollingTestCase(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.addCleanup(self.browser.quit)

    def testFrontend(self):
        self.browser.get('http://localhost:5000/frontend')
        self.assertIn('Polling app', self.browser.title)

    def testPoll(self):
        self.browser.get('http://localhost:5000/poll')
        import pprint
        pp = pprint.PrettyPrinter(indent=4)
        #pp.pprint(self.browser.f)
        json_response=self.browser.find_element_by_tag_name('body').text
        self.assertIn('Response Added', json_response)
    
    def testAllResponses(self):
        self.browser.get('http://localhost:5000/show_responses')
        
        json_response=self.browser.find_element_by_tag_name('body').text
        self.assertIn('List of Responses', json_response)

if __name__ == '__main__':
    unittest.main(verbosity=2)