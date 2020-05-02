from selenium import webdriver
from time import sleep
from secrets import pw
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys                         # for escape and such



class InstaBot:
    def __init__(self, username, pw):
        self.driver = webdriver.Chrome()
        self.username = username
        self.driver.get("https://instagram.com")

        wait = WebDriverWait(self.driver, 20)

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

    def like_posts(self, user):
        # first post
        wait = WebDriverWait(self.driver, 10)

        # wait until the profile is actually loaded
        print("waiting on matching name", user)
        el = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//h2[@class='_7UhW9       fKFbl yUEEX   KV-D4            fDxYl     ']")))
        print(el.text)
        
        while el.text != user:
            sleep(2)
            el = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//h2[@class='_7UhW9       fKFbl yUEEX   KV-D4            fDxYl     ']")))
            print(el.text)

        # get number of posts
        el = wait.until(EC.visibility_of_element_located(
            (By.CLASS_NAME, 'g47SY ')))
        num_posts = int(el.text)
        print("\nnumber of posts:", num_posts)



        el = wait.until(EC.visibility_of_element_located(
            # (By.XPATH, "/html/body/div[1]/section/main/div/div[2]/article/div/div/div[1]/div[1]")))
            (By.CLASS_NAME, "eLAPa")))
            # try: classes eLAPa, KL4Bh, FFVAD
        el.click()

        new_likes = 0

        for i in range(num_posts):
            
            # wait for the visible heart first
            heart = wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//span[@class='fr66n']")))
            
            # get the color of the like heart
            color = self.driver.find_element_by_css_selector('section>span>button>svg').get_attribute('fill')

            if color == "#262626":
                # unlike: fill="#262626"
                # already liked: fill="#ed4956"
                heart.click()
                ++new_likes
                # print("post", i+1, "liked")

            # next
            if i+1 < num_posts:
                self.driver.find_element_by_link_text('Next')\
                    .click()
            else:
                # close (last) post
                webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
        
        print("\nNumber of new likes for the user", user, new_likes, "!\n")


myBot = InstaBot("jakobudovic", pw)
# myBot.search_user("wrongcountryfool")

users = ["aljadostal", "og_loc420_69", "wrongcountryfool"]

myBot.search_user("ogloc42069")
myBot.like_posts("ogloc42069")


"""
for user in users:
    myBot.search_user(user)
    print("\n---------------------------------)
    print(liking users post from: ", user))
    myBot.like_posts(user)
"""
print("all users covered!")
