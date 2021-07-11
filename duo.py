import sys, time, random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

if len(sys.argv) < 3:
	print("Pass credentials")
	sys.exit(1)

email = sys.argv[1]
password = sys.argv[2]

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://duolingo.com")

option = Options()
option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")
option.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})

urls = ["https://www.duolingo.com/stories/de-en-der-pass?mode=read", "https://www.duolingo.com/stories/de-en-eddy-der-arzt?mode=read", "https://www.duolingo.com/stories/de-en-eine-neue-jacke?mode=read", "https://www.duolingo.com/stories/de-en-der-neue-schuler?mode=read", "https://www.duolingo.com/stories/de-en-juniors-frage?mode=read", "https://www.duolingo.com/stories/de-en-zum-bahnhof?mode=read", "https://www.duolingo.com/stories/de-en-der-vegetarier?mode=read", "https://www.duolingo.com/stories/de-en-urlaubskleidung?mode=read", "https://www.duolingo.com/stories/de-en-die-reservierung?mode=read", "https://www.duolingo.com/stories/de-en-kann-ich-helfen?mode=read"]

try:
    have_account = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//a[@data-test="have-account"]'))
    )
    have_account.click()

    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "input"))
    )
    email_field.send_keys(email)

    password_field = driver.find_elements_by_css_selector("input")[1]
    password_field.send_keys(password)

    login = driver.find_elements_by_css_selector("button")[3]
    login.click()

    time.sleep(5)

    it = -1

    while True:
	    it += 1
	    if it > 99:
	    	break

	    driver.get(urls[it//10])
	    
	    time.sleep(4)

	    start_story = driver.find_elements_by_css_selector("button")[0]
	    start_story.click()
	    
	    time.sleep(2)

	    while True:
	    	try:
	    		next = driver.find_element_by_xpath('//span[text()="Continue"]')
	    		try:
	    			next.click()
	    		except WebDriverException:
	    			pass
	    	except WebDriverException:
	    		break

	    	try:
		    	options = driver.find_elements_by_xpath('//span[@data-test="stories-phrase"]')
		    	if len(options) > 0:
		    		for option in options:
		    			try:
		    				option.click()
		    				next.click()
		    			except WebDriverException:
		    				pass
	    	except WebDriverException:
	    		pass

	    	try:		
	    		options = driver.find_elements_by_xpath('//button[@data-test="stories-choice"]')
	    		if len(options) > 0:
		    		for option in options:
		    			try:
		    				option.click()
		    				next.click()
		    			except WebDriverException:
		    				pass
	    	except WebDriverException:
	    		pass

	    	try:		
	    		options = driver.find_elements_by_xpath('//div[@data-test="stories-selectable-phrase"]')
	    		if len(options) > 0:
		    		for option in options:
		    			try:
		    				option.click()
		    				next.click()
		    			except WebDriverException:
		    				pass
	    	except WebDriverException:
	    		pass

	    	finals = driver.find_elements_by_css_selector("button._1hk_1._27o_2:not(._3alTu)")
	    	if len(finals) > 0:

	    		for i in range(len(finals)):
	    			try:
	    				finals[i].click()
	    				next.click()
	    			except WebDriverException:
	    				pass

	    			for j in range(len(finals)):
	    				if i != j:
			    			try:
			    				finals[j].click()
			    				next.click()
			    			except WebDriverException:
			    				pass


finally:
    driver.quit()