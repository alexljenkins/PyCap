import time
from pathlib import Path
from dash.testing.application_runners import import_app
from selenium import webdriver

APP_PATH = str(Path(__file__).parent.parent.parent.resolve() / "app.py")

# trying to get chrome headless inside the docker
# https://stackoverflow.com/questions/45323271/how-to-run-selenium-with-chrome-in-docker
# import chromedriver_binary
# chrome_options=webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("window-size=1400,2100") 
# chrome_options.add_argument('--disable-gpu')

# driver=webdriver.Chrome(chrome_options=chrome_options)


def selenium_working_example():
    """ Just example code to see how things work
    NOT IN USE"""
    DRIVER = webdriver.Chrome()
    DRIVER.get("https://www.google.com")
    time.sleep(5)  # Let the user actually see something!
    search_box = DRIVER.find_element_by_name("q")
    search_box.send_keys("ChromeDriver")
    search_box.submit()
    time.sleep(5)  # Let the user actually see something!
    DRIVER.quit()


def test_01_dash_duo_everything(dash_duo):
    # define your app inside the test function
    app = import_app(APP_PATH)
    # host the app locally in a thread
    dash_duo.start_server(app, "0.0.0.0", port=8050, debug=True)

    # wait for elements to load
    dash_duo.wait_for_page(url='localhost:8050', timeout=10)
    dash_duo.wait_for_element_by_id("ticker-input", timeout=None)
    dash_duo.wait_for_element_by_id("ticker-button", timeout=None)

def test_02_dash_duo_server_and_selenium_actions(dash_duo):
    app = import_app(APP_PATH)
    dash_duo.start_server(app, "0.0.0.0", port=8050, debug=True)
    time.sleep(5)
    DRIVER = webdriver.Chrome()
    DRIVER.get("localhost:8050")
    time.sleep(5)  # Let the user actually see something!
    search_box = DRIVER.find_element_by_id("ticker-input")
    search_box.send_keys("ChromeDriver")
    time.sleep(5)
    search_box.submit()
    time.sleep(5)

def test_03_selenium_only_inside_docker(dash_duo):
    driver.get("0.0.0.0:8050")
    time.sleep(5)
    search_box = driver.find_element_by_id("ticker-input")
    search_box.send_keys("ChromeDriver")
    time.sleep(5)
    search_box.submit()
    assert 3 == 2


