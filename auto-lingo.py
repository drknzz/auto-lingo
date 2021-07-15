import sys, time, json, argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains


def set_chrome_options(chrome_options):
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")

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
        with open('settings.json') as json_f:
            settings = json.load(json_f)
    except:
        print("Failed to import settings from settings.json.")
        sys.exit()

    return settings


def get_credentials():
    try:
        with open('credentials.json') as json_file:
            creds = json.load(json_file)

        login = creds['login']
        password = creds['password']
    except:
        return "", ""

    return login, password


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--stories", help="stories mode", action="store_true")
    parser.add_argument("-l", "--learn", help="learn mode", action="store_true")
    parser.add_argument("-i", "--incognito", help="incognito browser mode", action="store_true")
    parser.add_argument("-m", "--mute", help="mute browser audio", action="store_true")

    args = parser.parse_args()

    if args.incognito:
        settings['incognito'] = True

    if args.mute:
        settings['mute_audio'] = True

    # set default mode to stories
    if not args.learn and not args.stories:
        args.stories = True

    return args


def log_in(login, password):
    if settings['auto_login'] and login != "" and password != "":
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@data-test="email-input"]'))
        )
        email_field.send_keys(login)

        password_field = driver.find_element_by_xpath('//input[@data-test="password-input"]')
        password_field.send_keys(password)

        login_button = driver.find_element_by_xpath('//button[@data-test="register-button"]')
        login_button.click()

    try:
        wait = WebDriverWait(driver, 25)
        wait.until(lambda driver: driver.current_url == "https://www.duolingo.com/learn")
    except WebDriverException:
        exit("Timed out. Please login to Duolingo in time.")


def task_tokens(tokens):
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
            option.click()
        except WebDriverException:
            pass


def challenge_select():
    sentence = driver.find_element_by_xpath('//h1[@data-test="challenge-header"]').text
    sentence += " (s)"
    if sentence in dictionary:
        choices = driver.find_elements_by_xpath('//span[@class="HaQTI"]')

        for choice in choices:
            if choice.text == dictionary[sentence]:
                choice.click()

    else:
        skip = driver.find_element_by_xpath('//button[@data-test="player-skip"]')
        skip.click()
        solution = driver.find_element_by_xpath('//div[@class="_1UqAr _1sqiF"]').text
        dictionary[sentence] = solution
        print(sentence, '-o->', dictionary[sentence])


def challenge_speak_listen():
    skip = driver.find_element_by_xpath('//button[@data-test="player-skip"]')
    skip.click()


def challenge_judge():
    sentence = driver.find_element_by_xpath('//div[@class="_3-JBe"]').text
    sentence += " (j)"
    if sentence in dictionary:
        choices = driver.find_elements_by_xpath('//div[@data-test="challenge-judge-text"]')

        for choice in choices:
            if choice.text == dictionary[sentence]:
                choice.click()
    else:
        skip = driver.find_element_by_xpath('//button[@data-test="player-skip"]')
        skip.click()
        solution = driver.find_element_by_xpath('//div[@class="_1UqAr _1sqiF"]')
        dictionary[sentence] = solution.text
        print(sentence, '-s->', dictionary[sentence])


def challenge_form():
    sentence = driver.find_element_by_xpath('//div[@data-test="challenge-form-prompt"]').get_attribute('data-prompt')
    sentence += " (f)"
    if sentence in dictionary:
        choices = driver.find_elements_by_xpath('//div[@data-test="challenge-judge-text"]')

        for choice in choices:
            if choice.text == dictionary[sentence]:
                choice.click()
    else:
        skip = driver.find_element_by_xpath('//button[@data-test="player-skip"]')
        skip.click()
        solution = driver.find_element_by_xpath('//div[@class="_1UqAr _1sqiF"]')
        dictionary[sentence] = solution.text
        print(sentence, '-x->', dictionary[sentence])


def challenge_name():
    sentence = driver.find_element_by_xpath('//h1[@data-test="challenge-header"]').text
    sentence += " (n)"
    if sentence in dictionary:
        input_field = driver.find_element_by_xpath('//input[@data-test="challenge-text-input"]')
        input_field.send_keys(dictionary[sentence])
        input_field.send_keys(Keys.RETURN)

    else:
        skip = driver.find_element_by_xpath('//button[@data-test="player-skip"]')
        skip.click()
        time.sleep(0.2)
        solution = driver.find_element_by_xpath('//div[@class="_1UqAr _1sqiF"]').text
        dictionary[sentence] = solution
        print(sentence, '-+->', dictionary[sentence])


def challenge_reverse_translation():
    sentence = driver.find_element_by_xpath('//span[@data-test="hint-sentence"]').text
    sentence += " (r)"
    if sentence in dictionary:
        input_field = driver.find_element_by_xpath('//input[@data-test="challenge-text-input"]')
        input_field.send_keys(dictionary[sentence])
        input_field.send_keys(Keys.RETURN)

    else:
        skip = driver.find_element_by_xpath('//button[@data-test="player-skip"]')
        skip.click()
        time.sleep(0.2)
        solution = driver.find_element_by_xpath('//div[@class="_1UqAr _1sqiF"]').text

        input_text = driver.find_element_by_xpath('//label[@class="_3f_Q3 _2FKqf _2ti2i sXpqy"]').text
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
        print(sentence, '--->', dictionary[sentence])


def challenge_translate():
    sentence = driver.find_element_by_xpath('//span[@data-test="hint-sentence"]').text
    sentence += " (t)"
    if sentence in dictionary:
        tap_tokens = driver.find_elements_by_xpath('//button[@data-test="challenge-tap-token"]')
        if len(tap_tokens) > 0:
            # get solution without dot at the end
            # remove commas, dots, marks and change string to lowercase
            solution = dictionary[sentence].replace(".", "").replace(",", "").replace("!", "").replace("?", "").replace("'", " '").lower()
            words = solution.split(" ")

            for word in words:
                for tap_token in tap_tokens:
                    if tap_token.get_attribute("disabled") != None:
                        continue
                    if tap_token.text.lower() == word:
                        tap_token.click()
                        break
        else:
            input_field = driver.find_element_by_xpath('//textarea[@data-test="challenge-translate-input"]')
            input_field.send_keys(dictionary[sentence])
            input_field.send_keys(Keys.RETURN)

    else:
        skip = driver.find_element_by_xpath('//button[@data-test="player-skip"]')
        skip.click()
        solution = driver.find_element_by_xpath('//div[@class="_1UqAr _1sqiF"]').text
        dictionary[sentence] = solution
        print(sentence, '--->', dictionary[sentence])


def complete_story():
    start_story = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, '//button[@data-test="story-start"]'))
    )
    start_story.click()

    task_list = ['//span[@data-test="stories-phrase"]', '//button[@data-test="stories-choice"]', '//div[@data-test="stories-selectable-phrase"]', '//button[@data-test="stories-token"]']
    story_completed = False

    while not story_completed:
        # try to locate next button
        try:
            next = driver.find_element_by_xpath('//button[@data-test="stories-player-continue"]')
        except WebDriverException:
            break

        # try to click next button
        try:
            next.click()
        except WebDriverException:
            pass
        
        # try to do any task
        for task in task_list:
            options = driver.find_elements_by_xpath(task)
            if len(options) == 0:
                continue

            if task == task_list[-1]:
                task_tokens(options)
                story_completed = True
            else:
                task_options(options)

            next.click()
            break
    
    # wait for completion to register
    finish_story = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, '//button[@data-test="stories-player-done"]'))
    )

    # close story tab and switch to main tab
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


def complete_skill(possible_skip_to_lesson=False):
    if possible_skip_to_lesson:
        time.sleep(2)
        try:
            skip_to_lesson = driver.find_element_by_xpath('//button[@class="_3o5OF _2q8ZQ t5wFJ yTpGk _2RTMn _3yAjN"]')
            skip_to_lesson.click()
        except WebDriverException:
            pass

    # wait for site to initialize
    skip = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, '//button[@data-test="player-skip"]'))
    )

    skill_completed = False

    while not skill_completed:
        while True:
            try:
                carousel = driver.find_element_by_xpath('//div[@data-test="player-end-carousel"]')
                skill_completed = True
                break
            except WebDriverException:
                pass
            
            try:
                no_thanks = driver.find_element_by_xpath('//button[@data-test="no-thanks-to-plus"]')
                skill_completed = True
                break
            except WebDriverException:
                pass

            try:
                challenge = driver.find_element_by_xpath('//div[@data-test="challenge challenge-speak"]')
                challenge_speak_listen()
                # break
            except WebDriverException:
                pass

            try:
                challenge = driver.find_element_by_xpath('//div[@data-test="challenge challenge-listen"]')
                challenge_speak_listen()
                # break
            except WebDriverException:
                pass

            try:
                challenge = driver.find_element_by_xpath('//div[@data-test="challenge challenge-listenTap"]')
                challenge_speak_listen()
                # break
            except WebDriverException:
                pass

            try:
                challenge = driver.find_element_by_xpath('//div[@data-test="challenge challenge-selectTranscription"]')
                challenge_speak_listen()
                # break
            except WebDriverException:
                pass

            try:
                challenge = driver.find_element_by_xpath('//div[@data-test="challenge challenge-form"]')
                challenge_form()
                # break
            except WebDriverException:
                pass

            try:
                challenge = driver.find_element_by_xpath('//div[@data-test="challenge challenge-judge"]')
                challenge_judge()
                # break
            except WebDriverException:
                pass

            try:
                challenge = driver.find_element_by_xpath('//div[@data-test="challenge challenge-translate"]')
                challenge_translate()
                # break
            except WebDriverException:
                pass
                
            try:
                challenge = driver.find_element_by_xpath('//div[@data-test="challenge challenge-completeReverseTranslation"]')
                challenge_reverse_translation()
                # break
            except WebDriverException:
                pass

            try:
                challenge = driver.find_element_by_xpath('//div[@data-test="challenge challenge-name"]')
                challenge_name()
                # break
            except WebDriverException:
                pass

            try:
                challenge = driver.find_element_by_xpath('//div[@data-test="challenge challenge-select"]')
                challenge_select()
                # break
            except WebDriverException:
                pass

            try:
                next = driver.find_element_by_xpath('//button[@data-test="player-next"]')
                next.click()
                break
            except WebDriverException:
                pass

        time.sleep(1)


def stories_bot():
    while True:
        driver.get("https://www.duolingo.com/stories?referrer=web_tab")
        stories = WebDriverWait(driver, 100).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@class="_2nLk_" and not(@class="_3N2Ph")]//div[@class="X4jDx" and not(text()="+0 XP")]'))
        )

        if len(stories) == 0:
            break

        for story in stories:
            if "+0 XP" in story.text:
                continue

            action = ActionChains(driver)
            action.move_to_element(story).click().perform()

            read_story = story.find_element_by_xpath('//a[@data-test="story-start-button"]')
            story_url = read_story.get_attribute('href')

            driver.execute_script("window.open('" + story_url + "', '_blank')")
            driver.switch_to.window(driver.window_handles[1])

            complete_story()

            if settings['antifarm_sleep'] > 0:
                time.sleep(settings['antifarm_sleep'])


def learn_bot():
    global dictionary
    dictionary = {}

    while True:
        driver.get("https://www.duolingo.com/learn")
        skills = WebDriverWait(driver, 100).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@data-test="skill"]'))
        )

        time.sleep(2)

        completed_skill = False

        for skill in skills:
            try:
                start_skill = skill.find_element_by_xpath('//button[@data-test="start-button"]')
                start_skill.click()
                complete_skill()
                completed_skill = True

                if settings['antifarm_sleep'] > 0:
                    time.sleep(settings['antifarm_sleep'])

                break

            except WebDriverException:
                pass

            # search for g tag with grey circle fill
            # cannot search for skills with level < 5 because some skills cap at level 1
            g_tag = skill.find_element_by_tag_name('g')

            if 'fill="#e5e5e5"' not in g_tag.get_attribute('innerHTML'):
                continue

            # first check if there is a chance for "Welcome to x!" screen with skip to lesson button
            possible_skip_to_lesson = False

            try:
                zero_level = skill.find_element_by_xpath('.//div[@data-test="level-crown"]')
            except WebDriverException:
                possible_skip_to_lesson = True

            time.sleep(0.5)
            # before doing anything with skills, perform a blank click for possible notifications to disappear
            blank_item = driver.find_element_by_xpath('//div[@class="_2fX2D"]')
            action = ActionChains(driver)
            action.move_to_element(blank_item).click().perform()

            time.sleep(0.5)

            # navigate to chosen skill
            action = ActionChains(driver)
            action.move_to_element(skill).perform()
            time.sleep(0.5)

            skill.click()

            time.sleep(0.5)

            start_skill = skill.find_element_by_xpath('//button[@data-test="start-button"]')

            time.sleep(0.5)
            action = ActionChains(driver)
            action.move_to_element(start_skill).click().perform()

            complete_skill(possible_skip_to_lesson)

            completed_skill = True

            if settings['antifarm_sleep'] > 0:
                time.sleep(settings['antifarm_sleep'])

            break

        if not completed_skill:
            break


def main():
    global settings
    settings = get_settings()

    login, password = get_credentials()

    args = parse_arguments()

    chrome_options = Options()
    set_chrome_options(chrome_options)

    global driver
    driver = webdriver.Chrome(settings['chromedriver_path'], options=chrome_options)
    driver.get("https://duolingo.com")

    try:
        have_account = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[@data-test="have-account"]'))
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