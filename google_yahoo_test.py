from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BaseSearchPage:
    def __init__(self, driver, url):
        self.driver = driver
        self.url = url
        print(self.__dict__)

    def search(self, term):
        raise NotImplementedError("Subclasses must implement the search method")

class GoogleSearchPage(BaseSearchPage):
    def search(self, term):
        search_box = self.driver.find_element(By.NAME, 'q')
        search_box.send_keys(term)
        search_box.submit()

    def get_first_result_text(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'h3'))
            )
            first_result = self.driver.find_element(By.CSS_SELECTOR, 'h3')
            print(first_result.text)
            return first_result.text.strip()
        except Exception as e:
            print(f"Error retrieving search result: {e}")
            return ''

class YahooSearchPage(BaseSearchPage):
    def search(self, term):
        search_box = self.driver.find_element(By.NAME, 'p')
        search_box.send_keys(term)
        search_box.submit()

    def get_first_result_text(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'main'))
            )
            element = self.driver.find_element(By.PARTIAL_LINK_TEXT, 'Yahoo')
            return element.text
        except Exception as e:
            print(f"Error retrieving search result: {e}")
            return ''

class SearchTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(
            executable_path='C:/Users/gadha/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe')

    def test_google_search(self):
        expected_result = 'Google'
        self._perform_search(GoogleSearchPage(self.driver, 'https://www.google.com'), 'Google',
                             expected_result)  #

    def test_yahoo_search(self):
        expected_result = 'Yahoo'
        self._perform_search(YahooSearchPage(self.driver, 'https://search.yahoo.com'), 'Yahoo', expected_result)

    def _perform_search(self, search_page, term, expectedResult):
        self.driver.get(search_page.url)
        search_page.search(term)
        first_result = search_page.get_first_result_text()
        print(f"First result text: '{first_result}'")
        self.assertTrue(first_result.strip() == expectedResult,
                        f"Assertion failed for {search_page.__class__.__name__} with term '{term}'")

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()