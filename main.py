from selenium import webdriver
from time import sleep
from secrets import pw
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# for escape and such
from selenium.webdriver.common.keys import Keys
import time


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
        try:
            el = self.wait.until(EC.visibility_of_element_located(
                (By.XPATH, '//button[contains(text(), \'Not Now\')]')))
            el.click()
        except Exception as e:
            print("No 'Not Now' button found!")

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
        try:
            # try classes: eLAPa, KL4Bh, _9AhH0, FFVAD
            first_post = self.wait.until(EC.visibility_of_element_located(
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
        if num_posts is not None and num_posts > 0:
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

    def my_profile(self):
        sleep(1)
        my_icon = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//a[@href=\"/{}/\"]".format(self.username))))
        my_icon.click()

    def unfollow(self, me, cool_users):
        self.my_profile()

        following_btn = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//a[@href=\"/{}/following/\"]".format(self.username))))
        following_btn.click()
        # TODO

    def get_unfollowers(self):
        self.my_profile()
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(@href,'/following')]")\
            .click()
        following = self._get_names()
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
            .click()
        followers = self._get_names()
        not_following_back = [
            user for user in following if user not in followers]
        print(not_following_back)
        return not_following_back

    def _get_names(self):
        sleep(2)
        names = []

        # try:
        """sugs = self.wait.until(EC.visibility_of_element_located(self.driver.find_element_by_xpath(
                '//h4[contains(text(), Suggestions)]')))
            self.driver.execute_script('arguments[0].scrollIntoView()', sugs)"""
        # except Exception as e:
        sleep(2)

        scroll_box = self.wait.until(EC.visibility_of_element_located(
                                     (By.CLASS_NAME, "isgrP")))
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)

        # "jSC57  _6xe7A"

        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        # print(names)
        # close button
        close_btn = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, "/html/body/div[4]/div/div[1]/div/div[2]")))

        close_btn.click()
        return names


start_time = time.time()

me = "plugwalk2005"
# me = "jakobudovic"
bot = InstaBot(me, pw)

# users1 = ["plugwalk2005", "jakobudovic", "rokcaserman",
#           "davidtrafela", "pek1aj", "plugwalk2005", "tilen_miklavic"]

users = ["theinsignianow"]
cool_people = ["jakobudovic", "wrongcountryfool"]

# bot.unfollow(me, cool_people)
unfollowers = bot.get_unfollowers()
"""
unfollowers = ['annaklinski', 'beetlepimp', 'cloutmass', 'ogreen99', 'librarymacabre', 'bruhper', 'bangerbuddy', 'kuwambo', 'edp445daily', 'ogloc42069', 'killingdig', 'vozzey', 'realquornhub', 'shpitpost', 'cocaineape', 'avarosehi', '_colebennett_', 'radboudinternationalstudents', 'future', 'kevinflynnnnnnnnnnnnnn', 'deddstar', 'thuggerthugger1', 'klowt', 'bbnomula', 'nut.mov', 'thereallilmar', 'programmer.me', 'painful_memes.v2', 'thegrilledchez', 'dankmemesgang', 'adam22', 'yungcaterpillar.vhs', 'memezar', 'ted',
               'dybearpooh', 'whitepeoplehumor', 'nut', 'lilpump', 'h3h3product'
               'ions', 'i_have_no_memes96_v2', 'mkbhd']
"""

f = open('unfollowers_meme_page.txt', 'w')
for unfollower in unfollowers:
    f.write(unfollower + '\n')
f.write('\nlen:' + str(len(unfollowers)) + '\n')

f.close()

"""
for user in users:
    if bot.search_user(user):
        print("\n---------------------------------")
        print("Liking ", user, "'s posts...")
        bot.like_posts(user)
    else:
        print("Skipping.", user, "was not found.")
"""

# print("all users covered!")
print("--- %s seconds ---" % (time.time() - start_time))
