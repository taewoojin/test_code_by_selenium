import sys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver


class FunctionTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        cls.live_server_url = cls.server_url
        super().tearDownClass()

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)     # 암묵적 대기

    # 에러가 발생해도 실행되는 메소드지만 setUp()에서 에러가 발생하면 실행되지 않음.
    def tearDown(self):
        self.browser.quit()

    # 헬퍼 메소드('test_'로 시작되지 않으면 테스트되지 않기 때문에 리팩토링할 때 사용된다)
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')  # element에 s가 붙어서 복수의 요소가 반환된다.
        self.assertIn(row_text, [row.text for row in rows])

    # Input box 검색
    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')