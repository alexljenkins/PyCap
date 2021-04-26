from selenium import webdriver
from pathlib import Path
import time
from dash.testing.application_runners import import_app

APP_PATH = str(Path(__file__).parent.parent.parent.resolve() / "app.py")

def selenium_working_example():
    """ Just example code to see how things work
    NOT IN USE"""
    DRIVER = webdriver.Chrome()
    DRIVER.get('https://www.google.com')
    time.sleep(5) # Let the user actually see something!
    search_box = DRIVER.find_element_by_name('q')
    search_box.send_keys('ChromeDriver')
    search_box.submit()
    time.sleep(5) # Let the user actually see something!
    DRIVER.quit()

# def test_01_input_ticker_field(dash_duo):
#     # define your app inside the test function
#     app = import_app(APP_PATH)
#     # host the app locally in a thread
#     dash_duo.start_server(app, "0.0.0.0", port=8050, debug=True)
#     # use selenium to get onto the page
#     DRIVER = webdriver.Chrome()
#     DRIVER.get('localhost:8050')

#     # wait for elements to load
#     dash_duo.wait_for_page(url='localhost:8050', timeout=10)
#     dash_duo.wait_for_element_by_id("ticker-input", timeout=None)
#     dash_duo.wait_for_element_by_id("ticker-button", timeout=None)
#     # time.sleep(10)

#     # fill in search field and click button with selenium
#     search_box = DRIVER.find_element_by_name('ticker-input')
#     search_box.send_keys('GOOGL')
#     button = DRIVER.find_element_by_id('ticker-button')
#     button.click()

#     assert 1 == 1

    # assert dash_duo.get_logs() == [], "browser console should contain no error"
    # 8. visual testing with percy snapshot
    # dash_duo.percy_snapshot("bsly001-layout")