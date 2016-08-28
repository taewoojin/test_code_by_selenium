from .base import FunctionTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionTest):
    def test_can_start_a_list_and_retrieve_it_later(self):
        # 로컬 주소를 하드코딩하는 대신에 live_server_url 메소드가 제공됨.
        self.browser.get(self.server_url)

        # self.assertIn('To-Do', self.browser.title)
        # header_text = self.browser.find_element_by_tag_name('h1').text
        # self.assertIn('To-Do', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            '작업 아이템 입력'
        )
        inputbox.send_keys('공작깃털 사기')
        inputbox.send_keys(Keys.ENTER)

        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('공작깃털을 이용해서 그물 만들기')
        inputbox.send_keys(Keys.ENTER)

        self.check_for_row_in_list_table('1. 공작깃털 사기')
        self.check_for_row_in_list_table('2. 공작깃털을 이용해서 그물 만들기')

        ## 새로운 브라우저 세션을 이용해서 에디스의 정보가
        ## 쿠키를 통해 유입되는 것을 방지한다.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('공작깃털 사기', page_text)
        self.assertNotIn('공작깃털을 이용해서 그물 만들기', page_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('우유 사기')
        inputbox.send_keys(Keys.ENTER)

        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('공작깃털 사기', page_text)
        self.assertIn('우유 사기', page_text)
