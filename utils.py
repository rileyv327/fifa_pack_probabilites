from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep


def get_free_proxies():

    # create selenium driver
    options = Options()
    options.binary_location = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
    driver = webdriver.Chrome(chrome_options=options,
                              executable_path=r'C:/Users/riley/chromedriver_win32/chromedriver.exe')

    driver.get('https://sslproxies.org')

    table = driver.find_element(By.TAG_NAME, 'table')
    thead = table.find_element(
        By.TAG_NAME, 'thead').find_elements(By.TAG_NAME, 'th')
    tbody = table.find_element(
        By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')

    headers = []
    for th in thead:
        headers.append(th.text.strip())

    proxies = []
    for tr in tbody:
        proxy_data = {}
        tds = tr.find_elements(By.TAG_NAME, 'td')
        for i in range(len(headers)):
            proxy_data[headers[i]] = tds[i].text.strip()
        proxies.append(proxy_data)

    driver.quit()

    return [x["IP Address"] for x in proxies]


# '145.239.169.47', '76.118.227.8', '85.25.117.134', '194.233.86.75', '45.80.148.189'
