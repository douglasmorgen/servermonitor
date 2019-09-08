import unittest
import requests
#from my_sum import sum
import pprint
import json

class TestSum(unittest.TestCase):
    def test_frontend(self):
        frontend = requests.get("http://localhost:5000/frontend",timeout=2)
        content=str(frontend.content)
        self.assertIn('<title>Polling app</title>',content )

    def test_api(self):
        
        responses = requests.get("http://localhost:5000/show_responses",timeout=2)
        d = json.loads(responses.content)
        print(d['message'])
        self.assertEqual(d['message'], 'List of Responses')
        
    def test_list_poll(self):
        
        pp = pprint.PrettyPrinter(indent=4)
        #pp.pprint(frontend.content)
        poll = requests.get("http://localhost:5000/poll",timeout=2)
        d = json.loads(poll.content)
        self.assertEqual(d['message'], 'Response Added')
    
    def test_sanity(self):
        data = [1, 2, 3]
        result = sum(data)
        self.assertEqual(result, 6)

if __name__ == '__main__':
    unittest.main()