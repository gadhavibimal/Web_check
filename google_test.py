from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest

class SearchPage:
    def __init__(self, driver):
        self.driver = driver

    def search(self, term):
        search_box = self.driver.find_element(By.NAME, 'q')
        search_box.send_keys(term)
        search_box.submit()

    def get_first_result_text(self):
        first_result = self.driver.find_element(By.CSS_SELECTOR, 'h3')
        return first_result.text

class SearchTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(executable_path='C:/FILEPATH')  # Replace FILEPATH with the path to the Chromedriver file.
        self.driver.get('https://www.google.com')
        self.search_page = SearchPage(self.driver)

    def test_search(self):
        self.search_page.search('your search term')
        first_result = self.search_page.get_first_result_text()
        self.assertTrue(first_result.strip())  # Assert that the first result is not empty

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
