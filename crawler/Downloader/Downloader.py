from selenium import webdriver
from time import sleep

# download.default_directory: target directory
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'J:\\DownloadTarget'}
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', prefs)

# chromedriver directory
driver = webdriver.Chrome(executable_path='D:/Python3.9/Scripts/chromedriver.exe', chrome_options=options)

for i in range(10000,10050,1):
    # Target url (some ids are missing, which will cause an error and the script will break down)
    file_url = 'https://freemidi.org/getter-'+ str(i)
    driver.get(file_url)
    # Maybe we should check the button before click?
    dl_button = driver.find_element_by_id('downloadmidi').click()
    # Pause for download
    sleep(10)
    print("Finished" + file_url)

driver.quit()