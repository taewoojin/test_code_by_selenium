from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)     # 암묵적 대기

    # 에러가 발생해도 실행되는 메소드지만 setUp()에서 에러가 발생하면 실행되지 않음.
    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')

        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!!')


if __name__ == '__main__':
    # warnings='ignore'는 테스트 작성시에 발생하는 불필요한 리소스 경고를 제거하기 위함.
    # unittest.main() 함수 호출로 test 실행자 가동.
    unittest.main(warnings='ignore')