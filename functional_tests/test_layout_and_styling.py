from .base import FunctionTest


class LayoutAndStylingTest(FunctionTest):
    def test_layout_and_styling(self):
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width']/2,
            512,
            delta=10        # 오차가 +- 10픽셀 내로.
        )

        inputbox.send_keys('testing\n')

        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
