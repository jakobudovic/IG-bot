from selenium import webdriver
from time import sleep
from secrets import pw
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# for escape and such
from selenium.webdriver.common.keys import Keys


class InstaBot:
    def __init__(self, username, pw):
        self.driver = webdriver.Chrome()
        self.username = username
        self.driver.get("https://instagram.com")
        self.wait = WebDriverWait(self.driver, 8)

        # self.wait = WebDriverWait(self.driver, 25)

        el = self.wait.until(EC.visibility_of_element_located(
            (By.NAME, 'username')))
        el.send_keys(username)

        el = self.wait.until(EC.visibility_of_element_located(
            (By.NAME, 'password')))
        el.send_keys(pw)

        el = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//button[@type="submit"]')))
        el.click()

        # waiting on the popup "Not now"
        el = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//button[contains(text(), \'Not Now\')]')))
        el.click()

    def search_user(self, user):
        # wait = WebDriverWait(self.driver, 25)
        searchbox = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//input[@placeholder='Search']")))
        searchbox.clear()
        searchbox.send_keys(user)

        try:
            """
            el = self.wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//span[contains(text(),'{}')]".format(user))))
            el.click()
            """
            result = self.wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//a[@href=\"/{}/\"]".format(user))))
            result.click()
            return True
            # sleep(3)
        except Exception as e:
            print("Couldn't click on the user", user, "because of\n", e)
            return False

    def wait_for_the_right_user(self, user):
        found = False
        num_tires = 3
        while not found and num_tires > 0:
            num_tires = num_tires - 1
            try:
                print("waiting on matching name", user, "...")
                sleep(1)
                el = self.wait.until(EC.visibility_of_element_located(
                    (By.XPATH, "//h2[@class='_7UhW9       fKFbl yUEEX   KV-D4            fDxYl     ']")))
                if user == el.text:
                    print("Desired name found, loaded: ", el.text)
                    found = True
            except Exception as e:
                print("Element not yet visible: ", e)

    def find_num_posts(self):
        try:
            num_str = self.wait.until(EC.visibility_of_element_located(
                (By.CLASS_NAME, 'g47SY '))).text
            num_posts = int(num_str)
            print("\nnumber of posts:", num_posts)
            return num_posts
        except Exception as e:
            print("Unable to find number of posts: ", e)

    def find_first_post(self):
        wait = WebDriverWait(self.driver, 10)

        try:
            # try classes: eLAPa, KL4Bh, _9AhH0, FFVAD
            first_post = wait.until(EC.visibility_of_element_located(
                # (By.XPATH, "/html/body/div[1]/section/main/div/div[2]/article/div/div/div[1]/div[1]")))
                (By.CLASS_NAME, "_9AhH0")))
            return first_post
        except Exception as e:
            print("Post not found! \nException:\n", e)
            return None

    def next_post(self):
        try:
            self.driver.find_element_by_link_text('Next')\
                .click()
        except Exception as e:
            print("Error at getting next post,", e)

    def like_posts(self, user):
        # self.wait_for_the_right_user(user)
        num_posts = self.find_num_posts()
        if num_posts > 0:
            first_post = self.find_first_post()
        else:
            return
        if first_post == None:
            print("No post found, private page.")
            return
        first_post.click()
        print("Clicked on the first post!")

        new_likes = 0
        for i in range(num_posts):

            # wait for the visible heart first
            heart = self.wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//span[@class='fr66n']")))

            # get the color of the like heart
            color = self.driver.find_element_by_css_selector(
                'section>span>button>svg').get_attribute('fill')

            if color == "#262626":  # red: "#ed4956"
                heart.click()
                new_likes = new_likes + 1
            if i+1 < num_posts:
                self.next_post()
            else:
                # close (last) post
                webdriver.ActionChains(self.driver).send_keys(
                    Keys.ESCAPE).perform()
        print("\nNumber of new likes for the user", user, new_likes, "!\n")


bot = InstaBot("sadclown2005", pw)

users1 = ["plugwalk2005", "jakobudovic", "rokcaserman",
          "davidtrafela", "pek1aj", "plugwalk2005", "tilen_miklavic"]

# bot.search_user("ogloc42069")
# bot.like_posts("ogloc42069")


for user in users1:
    if bot.search_user(user):
        print("\n---------------------------------")
        print("Liking ", user, "'s posts...")
        bot.like_posts(user)
    else:
        print("Skipping", user)

# print("all users covered!")
