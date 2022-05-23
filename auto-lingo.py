import sys
from time import sleep
from os.path import dirname, join
from json import load
from random import randint
from argparse import ArgumentParser

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.chrome.service import Service as ChromeService


def set_chrome_options(chrome_options):
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")

    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    if settings['incognito']:
        chrome_options.add_argument("--incognito")

    if settings['mute_audio']:
        chrome_options.add_argument("--mute-audio")

    if settings['maximize_window']:
        chrome_options.add_argument("start-maximized")

    if settings['headless']:
        chrome_options.add_argument("--headless")


def exit(message=""):
    if message == "":
        message = "Oops! Something went wrong."

    print(message)
    driver.quit()
    sys.exit()


def get_settings():
    settings = {}
    try:
        path = dirname(__file__)
        with open(join(path, 'settings.json')) as json_f:
            settings = load(json_f)
    except:
        print("Failed to import settings from settings.json.")
        sys.exit()

    if settings['deviation'] > settings['antifarm_sleep'] and settings['antifarm_sleep'] != 0:
        print("deviation cannot be larger than antifarm_sleep time")
        sys.exit()

    if settings['deviation'] < 0:
        print("deviation cannot be negative")
        sys.exit()

    return settings


def get_credentials():
    try:
        path = dirname(__file__)
        path = join(path, 'credential.json')
        with open(path) as json_file:
            creds = load(json_file)

        login = creds['login']
        password = creds['password']
    except:
        return "", ""

    return login, password


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("-s", "--stories",
                        help="stories mode", action="store_true")
    parser.add_argument("-l", "--learn", help="learn mode",
                        action="store_true")
    parser.add_argument("-i", "--incognito",
                        help="incognito browser mode", action="store_true")
    parser.add_argument(
        "-m", "--mute", help="mute browser audio", action="store_true")
    parser.add_argument(
        "-a", "--autologin", help="login to duolingo automatically", action="store_true")

    args = parser.parse_args()

    if args.incognito:
        settings['incognito'] = True

    if args.mute:
        settings['mute_audio'] = True

    if args.autologin:
        settings['auto_login'] = True

    # set default mode to stories
    if not args.learn and not args.stories:
        args.stories = True

    return args


def log_in(login, password):
    if settings['auto_login'] and login != "" and password != "":
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//input[@data-test="email-input"]'))
        )
        email_field.send_keys(login)

        password_field = driver.find_element(By.XPATH,
                                             '//input[@data-test="password-input"]')
        password_field.send_keys(password)

        login_button = driver.find_element(By.XPATH,
                                           '//button[@data-test="register-button"]')
        login_button.click()

    try:
        wait = WebDriverWait(driver, 25)
        wait.until(lambda driver: driver.current_url ==
                   "https://www.duolingo.com/learn")

        print('Loggin in')

    except WebDriverException:
        exit("Timed out. Please login to Duolingo in time.")

# this function is dedicated to all imbecils who put "Correct solution:" inside the solution itself

def anti_imbecil_check(solution):
    return len(solution) > 17 and solution[0:17] == "Correct solution:"

def task_tokens(tokens):

    # I think this is where the solving happens
    done_list = []

    for i in range(len(tokens)):
        if i in done_list:
            continue

        for j in range(len(tokens)):
            if j in done_list or i == j:
                continue

            tokens[i].click()
            tokens[j].click()

            # check if we found a pair
            classes = tokens[i].get_attribute('class')
            if '_3alTu' in classes:
                done_list.append(i)
                done_list.append(j)
                break

def task_options(options):
    for option in options:
        try:
            if(option.get_attribute('data-test')=='challenge-tap-token'):
                challenge_match()
            else:
                option.click()
        except WebDriverException:
            pass

def challenge_select():
    sentence = driver.find_element(By.XPATH,
                                   '//h1[@data-test="challenge-header"]').text
    sentence += " (s)"
    if sentence in dictionary:
        choices = driver.find_elements(By.XPATH, '//span[@class="HaQTI"]')

        for choice in choices:
            if choice.text == dictionary[sentence]:
                choice.click()

    else:
        skip = driver.find_element(By.XPATH,
                                   '//button[@data-test="player-skip"]')
        skip.click()
        solution = driver.find_element(By.XPATH,
                                       '//div[@class="_1UqAr _1sqiF"]').text
        dictionary[sentence] = solution
        # print(sentence, '-o->', dictionary[sentence])

def challenge_speak_listen():
    skip = driver.find_element(By.XPATH, '//button[@data-test="player-skip"]')
    skip.click()

def challenge_judge():
    sentence = driver.find_element(By.XPATH, '//div[@class="_3-JBe"]').text
    sentence += " (j)"
    if sentence in dictionary:
        choices = driver.find_elements(By.XPATH,
                                       '//div[@data-test="challenge-judge-text"]')

        for choice in choices:
            if choice.text == dictionary[sentence]:
                choice.click()
    else:
        skip = driver.find_element(By.XPATH,
                                   '//button[@data-test="player-skip"]')
        skip.click()
        solution = driver.find_element(By.XPATH,
                                       '//div[@class="_1UqAr _1sqiF"]')
        dictionary[sentence] = solution.text
        # print(sentence, '-s->', dictionary[sentence])

def challenge_form():
    sentence = driver.find_element(By.XPATH,
                                   '//div[@data-test="challenge-form-prompt"]').get_attribute('data-prompt')
    sentence += " (f)"
    if sentence in dictionary:
        choices = driver.find_elements(By.XPATH,
                                       '//div[@data-test="challenge-judge-text"]')

        for choice in choices:
            if choice.text == dictionary[sentence]:
                choice.click()
    else:
        skip = driver.find_element(By.XPATH,
                                   '//button[@data-test="player-skip"]')
        skip.click()
        solution = driver.find_element(By.XPATH,
                                       '//div[@class="_1UqAr _1sqiF"]')
        dictionary[sentence] = solution.text
        # print(sentence, '-x->', dictionary[sentence])

def challenge_name():
    sentence = driver.find_element(By.XPATH,
                                   '//h1[@data-test="challenge-header"]').text
    sentence += " (n)"
    if sentence in dictionary:
        input_field = driver.find_element(By.XPATH,
                                          '//input[@data-test="challenge-text-input"]')
        input_field.send_keys(dictionary[sentence])
        input_field.send_keys(Keys.RETURN)

    else:
        skip = driver.find_element(By.XPATH,
                                   '//button[@data-test="player-skip"]')
        skip.click()
        sleep(0.2)
        solution = driver.find_element(By.XPATH,
                                       '//div[@class="_1UqAr _1sqiF"]').text

        correct_solution_solutions = driver.find_element(By.XPATH,
                                                         '//h2[@class="_1x6Dk _1sqiF"]').text
        if "solutions" in correct_solution_solutions:
            solution = solution.split(",")[0]

        dictionary[sentence] = solution
        # print(sentence, '-+->', dictionary[sentence])

def challenge_reverse_translation():
    sentence = driver.find_element(By.XPATH,
                                   '//span[@data-test="hint-sentence"]').text
    sentence += " (r)"
    if sentence in dictionary:
        input_field = driver.find_element(By.XPATH,
                                          '//input[@data-test="challenge-text-input"]')
        input_field.send_keys(dictionary[sentence])
        input_field.send_keys(Keys.RETURN)

    else:
        skip = driver.find_element(By.XPATH,
                                   '//button[@data-test="player-skip"]')
        skip.click()
        sleep(0.2)
        solution = driver.find_element(By.XPATH,
                                       '//div[@class="_1UqAr _1sqiF"]').text

        if (anti_imbecil_check(solution)):
            solution = solution[17:]

        input_text = driver.find_element(By.XPATH,
                                         '//label[@class="_3f_Q3 _2FKqf _2ti2i sXpqy"]').text
        input_text = input_text.replace("\n", "")

        diff_length = len(solution) - len(input_text)

        changed = False

        for i in range(len(input_text)):
            if input_text[i] != solution[i]:
                solution = solution[i:i+diff_length]
                changed = True
                break

        # if the answer is at the end of sentence
        if not changed:
            solution = solution[len(input_text):]

        dictionary[sentence] = solution
        # print(sentence, '--->', dictionary[sentence])

def challenge_translate():
    # static variable for choosing method of splitting tap tokens with apostrophe sign
    if "apostrophe_counter" not in challenge_translate.__dict__:
        challenge_translate.apostrophe_counter = 0
    # static variable for choosing method of splitting tap tokens with dash sign
    if "dash_counter" not in challenge_translate.__dict__:
        challenge_translate.dash_counter = 0

    sentence = driver.find_element(By.XPATH,
                                   '//span[@data-test="hint-sentence"]').text
    sentence += " (t)"
    if sentence in dictionary:
        tap_tokens = driver.find_elements(By.XPATH,
                                          '//button[@data-test="challenge-tap-token"]')
        # check if the challenge is tap tokens
        if len(tap_tokens) > 0:
            # get solution without dot at the end
            # remove commas, dots, marks and change string to lowercase
            solution = dictionary[sentence].replace(".", "").replace(
                ",", "").replace("!", "").replace("?", "").lower()

            if challenge_translate.apostrophe_counter % 2 == 0:
                solution = solution.replace("'", " '")

            if challenge_translate.dash_counter < 2:
                solution = solution.replace("-", " ")

            challenge_translate.apostrophe_counter = (
                challenge_translate.apostrophe_counter + 1) % 2
            challenge_translate.dash_counter = (
                challenge_translate.dash_counter + 1) % 4

            words = solution.split(" ")

            for word in words:
                for tap_token in tap_tokens:
                    if tap_token.get_attribute("aria-disabled") != None or tap_token.get_attribute("disabled") != None:
                        continue
                    if tap_token.text.lower() == word:
                        tap_token.click()
                        break
        else:
            input_field = driver.find_element(By.XPATH,
                                              '//textarea[@data-test="challenge-translate-input"]')
            input_field.send_keys(dictionary[sentence])
            input_field.send_keys(Keys.RETURN)

    else:
        skip = driver.find_element(By.XPATH,
                                   '//button[@data-test="player-skip"]')
        skip.click()
        solution = driver.find_element(By.XPATH,
                                       '//div[@class="_1UqAr _1sqiF"]').text
        solution = solution.replace(";", "").replace("¿", "").replace("¡", "")
        dictionary[sentence] = solution
        # print(sentence, '--->', dictionary[sentence])

def challenge_tap_complete():
    # print("---> challenge_tap_complete")
    sentence_words = driver.find_elements(By.XPATH,
                                          '//span[@data-test="hint-sentence"]')
    sentence = ""
    for word in sentence_words:
        sentence += word.text

    sentence += " (c)"
    if sentence in dictionary:
        tap_tokens = driver.find_elements(By.XPATH,
                                          '//button[@data-test="challenge-tap-token"]')

        for tap_token in tap_tokens:
            if tap_token.text == dictionary[sentence]:
                tap_token.click()
                break

    else: # this is when it can not quickly solve it.
        skip = driver.find_element(By.XPATH,
                                   '//button[@data-test="player-skip"]')
        # print(skip.text)
        skip.click()
        sleep(1)
        solution = driver.find_element(By.XPATH,
                                       '//div[@class="_1UqAr _1sqiF"]').text
        solution = solution.replace(" ", "")

        input_text = sentence[:-3]
        input_text = input_text.strip(" ")

        diff_length = len(solution) - len(input_text)

        changed = False

        for i in range(len(input_text)):
            if input_text[i] != solution[i]:
                solution = solution[i:i+diff_length]
                changed = True
                break

        # if the answer is at the end of sentence
        if not changed:
            solution = solution[len(input_text):]

        dictionary[sentence] = solution
        # print(sentence, '-q->', dictionary[sentence])

def challenge_tap():
    # print("---> challenge_tap")
    sentence = driver.find_element(By.XPATH,
                                   '//div[@class="_3NgMa _2Hg6H"]').text
    sentence += " (ta)"
    if sentence in dictionary:
        choices = driver.find_elements(By.XPATH,
                                       '//div[@class="_1yW4j _2LmyT"]')
        words = dictionary[sentence].split()
        for word in words:
            for choice in choices:
                if choice.text == word:
                    choice.click()
    else:
        skip = driver.find_element(By.XPATH,
                                   '//button[@data-test="player-skip"]')
        print(skip.text)
        skip.click()
        solution = driver.find_element(By.XPATH,
                                       '//div[@class="_1UqAr _1sqiF"]').text
        solution = solution.replace(".", "").replace("?", "").replace(
            "!", "").replace(";", "").replace(",", "").replace("¿", "")
        dictionary[sentence] = solution
        # print(sentence, '-ta->', dictionary[sentence])

def challenge_dialogue_readcomp(isDial):
    if isDial:
        sentence = driver.find_element(By.XPATH,
                                       '//div[@class="_1eXoV _3ZoSe"]').text
        sentence += " (d)"
    else:
        sentence = driver.find_element(By.XPATH,
                                       '//div[@class="_1iPXH _2Hg6H"]').text
        sentence += " (rc)"
    if sentence in dictionary:
        choices = driver.find_elements(By.XPATH,
                                       '//div[@data-test="challenge-judge-text"]')
        for choice in choices:
            if choice.text == dictionary[sentence]:
                choice.click()
    else:
        skip = driver.find_element(By.XPATH,
                                   '//button[@data-test="player-skip"]')
        skip.click()
        solution = driver.find_element(By.XPATH,
                                       '//div[@class="_1UqAr _1sqiF"]')
        dictionary[sentence] = solution.text
        print(sentence, '-d->', dictionary[sentence])

def challenge_gap():
    sentence = driver.find_element(By.XPATH,
                                   '//div[@class="_3Fi4A _2Hg6H"]').text
    sentence += " (fg)"
    if sentence in dictionary:
        choices = driver.find_elements(By.XPATH,
                                       '//div[@data-test="challenge-judge-text"]')
        for choice in choices:
            if choice.text == dictionary[sentence]:
                choice.click()
    else:
        skip = driver.find_element(By.XPATH,
                                   '//button[@data-test="player-skip"]')
        skip.click()
        solution = driver.find_element(By.XPATH,
                                       '//div[@class="_1UqAr _1sqiF"]')
        dictionary[sentence] = solution.text
        print(sentence, '-fg->', dictionary[sentence])

def challenge_match():

    tap_tokens = driver.find_elements(By.XPATH,
                                      '//button[@data-test="challenge-tap-token"]')

    for token in tap_tokens:
        if token.get_attribute("aria-disabled") != None or token.get_attribute("disabled") != None:
            continue

        invalid_tokens = []

        for token2 in tap_tokens:
            token.click()
            sleep(.5) # Click slower
            if token2 in invalid_tokens or token2.get_attribute("aria-disabled") != None or token.get_attribute("disabled") != None:
                # This one has been tried, move on to the next instance of the loop
                continue
            else:
                invalid_tokens.append(token2)
                # print(f"Two: {token2.text}")
                sleep(.5) # Click slower
                token2.click()

def complete_story():
    start_story = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.XPATH, '//button[@data-test="story-start"]'))
    )
    start_story.click()

    task_list = ['//span[@data-test="stories-phrase"]',
                 '//button[@data-test="stories-choice"]',
                 '//div[@data-test="stories-selectable-phrase"]',
                 '//button[@data-test="challenge-tap-token"]',
                 '//button[@data-test="stories-token"]',
                 ]
    done_tokens = False

    while True:
        # try to click next button
        try:
            next = driver.find_element(By.XPATH,
                                       '//button[@data-test="stories-player-continue"]')
            next.click()
        except WebDriverException:
            pass

        try:
            story_done = driver.find_element(By.XPATH,
                                             '//button[@data-test="stories-player-done"]')
            break
        except WebDriverException:
            pass

        try:
            blank_item = driver.find_element(
                By.XPATH, '//div[@class="_2fX2D"]')
            break
        except WebDriverException:
            pass

        if not done_tokens:
            # try to do any task
            for task in task_list:
                options = driver.find_elements(By.XPATH, task)
                # if did not find that task
                if len(options) == 0:
                    continue
                
                if task == task_list[-1]:
                    task_tokens(options)
                    done_tokens = True
                else:
                    task_options(options)

                break

    # close story tab and switch to main tab
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

def complete_skill(possible_skip_to_lesson=False):
    if possible_skip_to_lesson:
        sleep(2)
        try:
            skip_to_lesson = driver.find_element(By.XPATH,
                                                 '//button[@class="_3o5OF _2q8ZQ t5wFJ yTpGk _2RTMn _3yAjN"]')
            skip_to_lesson.click()
        except WebDriverException:
            pass

    # wait for site to initialize
    try:
        skip = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, '//button[@data-test="player-skip"]'))
        )
    except WebDriverException:
        pass

    skill_completed = False

    while not skill_completed:
        while True:
            try:
                no_thanks = driver.find_element(By.XPATH,
                                                '//button[@data-test="no-thanks-to-plus"]')
                skill_completed = True
                break
            except WebDriverException:
                pass

            try:
                challenge = driver.find_element(By.XPATH,
                                                '//div[@data-test="challenge challenge-speak"]')
                challenge_speak_listen()
            except WebDriverException:
                pass

            try:
                challenge = driver.find_element(By.XPATH,
                                                '//div[@data-test="challenge challenge-listen"]')
                challenge_speak_listen()
            except WebDriverException:
                pass

            try:
                challenge = driver.find_element(By.XPATH,
                                                '//div[@data-test="challenge challenge-listenTap"]')
                challenge_speak_listen()
            except WebDriverException:
                pass

            try:
                challenge = driver.find_element(By.XPATH,
                                                '//div[@data-test="challenge challenge-selectTranscription"]')
                challenge_speak_listen()
            except WebDriverException:
                pass

            try:
                challenge = driver.find_element(By.XPATH,
                                                '//div[@data-test="challenge challenge-form"]')
                challenge_form()
            except WebDriverException:
                pass

            try:
                challenge = driver.find_element(By.XPATH,
                                                '//div[@data-test="challenge challenge-judge"]')
                challenge_judge()
            except WebDriverException:
                pass

            try:
                challenge = driver.find_element(By.XPATH,
                                                '//div[@data-test="challenge challenge-translate"]')
                challenge_translate()
            except WebDriverException:
                pass

            try:
                challenge = driver.find_element(By.XPATH,
                                                '//div[@data-test="challenge challenge-completeReverseTranslation"]')
                challenge_reverse_translation()
            except WebDriverException:
                pass

            try:
                challenge = driver.find_element(By.XPATH,
                                                '//div[@data-test="challenge challenge-name"]')
                challenge_name()
            except WebDriverException:
                pass

            try:
                challenge = driver.find_element(By.XPATH,
                                                '//div[@data-test="challenge challenge-select"]')
                challenge_select()
            except WebDriverException:
                pass

            try:
                challenge = driver.find_element(By.XPATH,
                                                '//div[@data-test="challenge challenge-tapComplete"]')
                challenge_tap()
            except WebDriverException:
                pass

            try:
                challenge = driver.find_element(By.XPATH,
                                                '//div[@data-test="challenge challenge-dialogue"]')
                challenge_dialogue_readcomp(True)
                # break
            except WebDriverException:
                pass

            try:
                challenge = driver.find_element(By.XPATH,
                                                '//div[@data-test="challenge challenge-listenComprehension"]')
                challenge_speak_listen()
                # break
            except WebDriverException:
                pass

            try:
                challenge = driver.find_element(By.XPATH,
                                                '//div[@data-test="challenge challenge-readComprehension"]')
                challenge_dialogue_readcomp(False)
                # break
            except WebDriverException:
                pass

            try:
                challenge = driver.find_element(By.XPATH,
                                                '//div[@data-test="challenge challenge-gapFill"]')
                challenge_gap()
                # break
            except WebDriverException:
                pass

            try:
                challenge = driver.find_element(By.XPATH,
                                                '//div[@data-test="challenge challenge-match"]')
                challenge_match()
                # break
            except WebDriverException:
                pass

            try:
                next = driver.find_element(By.XPATH,
                                           '//button[@data-test="player-next"]')
                next.click()
                break
            except WebDriverException:
                pass

            # check if we already quit the skill
            try:
                blank_item = driver.find_element(By.XPATH,
                                                 '//div[@class="_2fX2D"]')
                skill_completed = True
                break
            except WebDriverException:
                pass

        sleep(1)

def stories_bot():

    print("📙 STORIES BOT")

    while True:
        driver.get("https://www.duolingo.com/stories?referrer=web_tab")
        stories = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//div[@class="_2nLk_" and not(@class="_3N2Ph")]//div[@class="X4jDx"]'))
        )

        if len(stories) == 0:
            break
        # for start from highest score
        stories = list(reversed(stories))
        for story in stories:
            story_display = story.text.splitlines()
            if "+0 XP" in story.text:
                print(f"📖 Skipping {story_display[0]}")
                continue

            
            print(f"📙 Starting {story_display[0]}")
            driver.execute_script("arguments[0].scrollIntoView();", story)
            story.click()

            read_story = story.find_element(By.XPATH,
                                            './/a[@data-test="story-start-button"]')
            story_url = read_story.get_attribute('href')

            driver.execute_script("window.open('" + story_url + "', '_blank')")
            driver.switch_to.window(driver.window_handles[1])

            complete_story()
            if settings['antifarm_sleep'] > 0:
                deviation = randint(-settings['deviation'],
                                           settings['deviation'])
                sleep(settings['antifarm_sleep'] + deviation)

            print(f"📙 Finishing {story_display[0]}")

def learn_bot():

    while True:
        driver.get("https://www.duolingo.com/learn")
        skills = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//div[@data-test="skill"]'))
        )

        completed_skill = False

        for skill in skills:
            try:
                start_skill = skill.find_element(By.XPATH,
                                                 '//a[@data-test="start-button"]')
                start_skill.click()
                complete_skill()
                completed_skill = True

                if settings['antifarm_sleep'] > 0:
                    sleep(settings['antifarm_sleep'])

                break

            except WebDriverException:
                pass

            # search for g tag with grey circle fill
            # cannot search for skills with level < 5 because some skills cap at level 1
            try:
                g_tag = skill.find_element(by=By.TAG_NAME, value='g')
            except WebDriverException:
                continue

            if 'fill="#e5e5e5"' not in g_tag.get_attribute('innerHTML'):
                continue

            # first check if there is a chance for "Welcome to x!" screen with skip to lesson button
            possible_skip_to_lesson = False

            # if the chosen skill has no crowns, there is a chance an additional screen will pop up
            try:
                zero_level = skill.find_element(By.XPATH,
                                                './/div[@data-test="level-crown"]')
            except WebDriverException:
                possible_skip_to_lesson = True

            # before doing anything with skills, perform a blank click for possible notifications to disappear
            blank_item = driver.find_element(
                By.XPATH, '//div[@class="_2fX2D"]')
            action = ActionChains(driver)
            action.move_to_element(blank_item).click().perform()

            sleep(0.5)

            # navigate to chosen skill
            action = ActionChains(driver)
            action.move_to_element(skill).perform()

            sleep(0.5)

            skill.click()

            sleep(0.5)

            found = True
            try:
                start_skill = skill.find_element(By.XPATH,
                                                 '//a[@data-test="start-button"]')
            except WebDriverException:
                found = False
            if not found:
                start_skill = skill.find_element(By.XPATH,
                                                 '//button[@data-test="start-button"]')

            action = ActionChains(driver)
            action.move_to_element(start_skill).click().perform()

            complete_skill(possible_skip_to_lesson)

            completed_skill = True

            if settings['antifarm_sleep'] > 0:
                deviation = randint(-settings['deviation'],
                                           settings['deviation'])
                sleep(settings['antifarm_sleep'] + deviation)

            break

        if not completed_skill:
            break

def main():

    print("🏁 Starting out")

    global dictionary
    dictionary = {}

    global settings
    settings = get_settings()

    login, password = get_credentials()

    args = parse_arguments()
    print(args.path)

    chrome_options = Options()
    set_chrome_options(chrome_options)

    global driver

    service = ChromeService(executable_path=settings['chromedriver_path'])

    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get("https://duolingo.com")

    try:
        have_account = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//button[@data-test="have-account"]'))
        )
        have_account.click()
    except WebDriverException as e:
        exit(e)

    log_in(login, password)

    if args.learn:
        learn_bot()

    if args.stories:
        stories_bot()

    exit("Auto-lingo finished.")

if __name__ == "__main__":
    main()
