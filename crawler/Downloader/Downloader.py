from selenium import webdriver
from time import sleep
import os

# The directory for storing our result
target_path = "J:\\DownloadTarget"
# chromedriver directory
working_directory = 'D:/Python3.9/Scripts/chromedriver.exe'
# Crawler range
start = 10000
end = 12000
# Max time spent on one target
max_sleep_time = 5

sleeptime = 0
# detect whether the file is downloaded by checking partial objects
def downloads_done():
    global sleeptime
    global max_sleep_time
    for filename in os.listdir(target_path):
        if ".crdownload" in filename:
            sleep(0.5)
            sleeptime += 0.5
            print("Pending...")
            if sleeptime < max_sleep_time:
                downloads_done()
            else:
                sleeptime = 0
                os.remove(target_path + "\\" +filename)

# download.default_directory: target directory
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': target_path}
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', prefs)

# chromedriver directory
driver = webdriver.Chrome(executable_path=working_directory, chrome_options=options)

for i in range(start,end,1):
    # Target url (some ids are missing, which will cause an error and the script will break down)
    file_url = 'https://freemidi.org/getter-'+ str(i)
    driver.get(file_url)
    # Maybe we should check the button before click?
    dl_button = driver.find_element_by_id('downloadmidi').click()
    # Check whether download is finished
    downloads_done()
    print("Finished " + file_url)

driver.quit()