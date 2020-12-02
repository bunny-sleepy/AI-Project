from selenium import webdriver
from time import sleep
import os

# TODO: you should change the directory path here
# The directory for storing our result
# **IMPORTANT** NOTE: YOU SHOULD USE \ INSTEAD OF / IN THE DIRECTORY STRING
target_path = "J:\\DownloadTarget"

# chromedriver directory
working_directory = 'D:/Python3.9/Scripts/chromedriver.exe'

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

# start: start position
# end: end position
def download_batch(start, end):

    # download.default_directory: target directory
    prefs = {'profile.default_content_settings.popups': 0,
            'download.default_directory': target_path,
            "profile.managed_default_content_settings.images": 2}
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', prefs)

    # Open error log file
    err_log_file = open(target_path + "\\DownloadErrorLog.txt", "a+")
    err_retry_list = []


    # chromedriver directory
    driver = webdriver.Chrome(executable_path=working_directory, chrome_options=options)

    for iter in range(start,end,1):
        # Target url
        file_url = 'https://freemidi.org/getter-'+ str(iter)
        try:
            driver.get(file_url)
            # Maybe we should check the button before click?
            dl_button = driver.find_element_by_id('downloadmidi').click()
            # Check whether download is finished
            downloads_done()
            print("Finished " + file_url)
        except:
            err_retry_list.append(iter)
            err_log = "Download failed: " + file_url
            print(err_log)

    for iter in err_retry_list:
        # Target url
        file_url = 'https://freemidi.org/getter-'+ str(iter)
        try:
            driver.get(file_url)
            # Maybe we should check the button before click?
            dl_button = driver.find_element_by_id('downloadmidi').click()
            # Check whether download is finished
            downloads_done()
            print("Finished " + file_url)
        except:
            err_log = "Retry failed: " + file_url
            err_log_file.write(err_log + "\n")
            print(err_log)    

    driver.quit()