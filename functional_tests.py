from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)     # 암묵적 대

    # 에러가 발생해도 실행되는 메소드지만 setUp()에서 에러가 발생하면 실행되지 않음.
    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')

        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            '작업 아이템 입력'
        )

        inputbox.send_keys('공작깃털 사기')

        inputbox.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')    # element에 s가 붙어서 복수의 요소가 반환된다.
        self.assertTrue(
            any(row.text == '1: 공작깃털 사기' for row in rows),
            '신규 작업이 테이블에 표시되지 않는다.',
        )

        self.fail('Finish the test!!')


if __name__ == '__main__':
    # warnings='ignore'는 테스트 작성시에 발생하는 불필요한 리소스 경고를 제거하기 위함.
    # unittest.main() 함수 호출로 test 실행자 가동.
    unittest.main(warnings='ignore')