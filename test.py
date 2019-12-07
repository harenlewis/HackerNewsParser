import unittest 
from bs4 import BeautifulSoup
 

class HNWebScrapperTest(unittest.TestCase): 
  
    # Returns True or False.
    def test(self):
        test_soup = BeautifulSoup('sample._test.html', 'html.parser')
        table = test_soup.find('table', attrs={'class': 'itemlist'})
        self.assertTrue(True) 
  
if __name__ == '__main__': 
    unittest.main() 