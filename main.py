from selenium import webdriver
from time import sleep
from secrets import pw
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InstaBot:
    def __init__(self, username, pw):
        self.driver = webdriver.Chrome()
        self.username = username
        self.driver.get("https://instagram.com")

        wait = WebDriverWait(self.driver, 10)

        el = wait.until(EC.visibility_of_element_located(
            (By.NAME, 'username')))
        el.send_keys(username)

        el = wait.until(EC.visibility_of_element_located(
            (By.NAME, 'password')))
        el.send_keys(pw)

        el = wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//button[@type="submit"]')))
        el.click()

        # waiting on the popup "Not now"
        el = wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//button[contains(text(), \'Not Now\')]')))
        el.click()

    def search_user(self, user):
        wait = WebDriverWait(self.driver, 10)
        el = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//input[@placeholder='Search']")))
        el.send_keys(user)

        el = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//a[contains(@href,'/{}/')]".format(user))))
        el.click()

    def like_posts(self):
        # first post
        wait = WebDriverWait(self.driver, 10)
        el = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "/html/body/div[1]/section/main/div/div[2]/article/div/div/div[1]/div[1]")))
        el.click()

        while True:
            print("new post liked")
            # like
            el = wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//span[@class='fr66n']")))
            el.click()

            # next
            self.driver.find_element_by_link_text('Next')\
                .click()


myBot = InstaBot("jakobudovic", pw)
# myBot.search_user("wrongcountryfool")
myBot.search_user("wrongcountryfool")
myBot.like_posts()
