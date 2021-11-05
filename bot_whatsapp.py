# https://dojopy.com/blog/python-automatizando-whatsapp-con-selenium
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

import time

class BotWhatsapp:
    def __init__(self):
        self.path_driver = 'chromedriver.exe'
        self.base_url = 'https://web.whatsapp.com'
        self.timeout = 8
        self.set_paths()

    def set_paths(self):
        # self.base_input = "//input[@title='Busca un chat o inicia uno nuevo']"
        # self.first_contact = '//*[@id="pane-side"]/div[1]/div/div/div[1]'
        # self.base_sent = '/html/body/div/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]'

        self.base_input = '//div[@role="textbox"][@class="_13NKt copyable-text selectable-text"]'
        self.first_contact = '//div[@class="_2nY6U"]'
        self.base_sent = '//div[@class="_2lMWa"]//div[@role="textbox"][@class="_13NKt copyable-text selectable-text"]'

    def start_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-extensions')
        options.add_argument('--profile-directory=Default')
        options.add_argument('--disable-plugins-discovery')

        # options.add_argument('--user-data-dir=chrome-data')
        options.add_argument('--user-data-dir=C:\\Users\\rmaki\\AppData\\Local\\Google\\Chrome\\User Data')

        self.browser = webdriver.Chrome(executable_path=self.path_driver,
                                        # chrome_options=options,
                                        options=options)

        self.browser.implicitly_wait(self.timeout) # seconds
        self.browser.get(self.base_url)
        try:
            WebDriverWait(self.browser, self.timeout).until(
                EC.presence_of_element_located(
                    (By.XPATH, self.base_input)
                )
            )
            return True
        except Exception as e:
            print(e)
            return False
    
    def send_message_to_contact(self, contact, message):
        start = self.start_browser()
        if not start:
            return False

        user_search = self.search_user_or_group(contact)
        if not (user_search or contact or message):
            return False
        
        time.sleep(1)
        message = message.strip()
        try:
            send_msg = WebDriverWait(self.browser, self.timeout).until(
                EC.presence_of_element_located(
                    (By.XPATH, self.base_sent)
                )
            )
        except Exception as e:
            print(e)
            return
        
        messages = message.split("\n")
        for msg in messages:
            send_msg.send_keys(msg)
            send_msg.send_keys(Keys.SHIFT + Keys.ENTER)
            sleep(1)

        send_msg.send_keys(Keys.ENTER)
        print('mensaje enviado')
        return True

    def search_user_or_group(self, contact):
        search = self.browser.find_element_by_xpath(self.base_input)
        # search = self.browser.find_element_by_css_selector(self.base_input)
        search.clear()
        search.send_keys(contact)
        try:
            time.sleep(1)
            vali_ = WebDriverWait(self.browser, self.timeout).until(
                EC.presence_of_element_located(
                    (By.XPATH, self.first_contact)
                )
            )
            if vali_.is_displayed():
                search.send_keys(Keys.ENTER)
                return True
        except Exception as e:
            print(e)
            print('No se encontró contacto.')
        return False

obj = BotWhatsapp()
obj.send_message_to_contact('59163580462', 'Hola Mundo!')