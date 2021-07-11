import sys, time, json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains


def set_chrome_options(chrome_options):
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--disable-infobars")
    # chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--incognito")
    chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})


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


def log_in(login, password):
    if login != "" and password != "":
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

            #check if we found a pair
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


def complete_story():
    start_story = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[@data-test="story-start"]'))
    )
    start_story.click()

    task_list = ['//span[@data-test="stories-phrase"]', '//button[@data-test="stories-choice"]', '//div[@data-test="stories-selectable-phrase"]', '//button[@data-test="stories-token"]']
    story_completed = False

    while not story_completed:
        #try to locate next button
        try:
            next = driver.find_element_by_xpath('//button[@data-test="stories-player-continue"]')
        except WebDriverException:
            break

        #try to click next button
        try:
            next.click()
        except WebDriverException:
            pass
        
        #try to do any task
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
    
    #wait for completion to register
    finish_story = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[@data-test="stories-player-done"]'))
    )

    #close story tab and switch to main tab
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


def stories_bot():
    while True:
        driver.get("https://www.duolingo.com/stories?referrer=web_tab")
        stories = WebDriverWait(driver, 10).until(
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


def main():
    settings = get_settings()
    login, password = get_credentials()

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

    stories_bot()
    # learn_bot() TODO

    exit("Auto-lingo finished.")


if __name__ == "__main__":
    main()