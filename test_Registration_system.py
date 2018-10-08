from selenium import webdriver



driver = webdriver.Chrome()
driver.implicitly_wait(30)
driver.get("localhost:5000")


driver.find_element_by_link_text('Sign Up').click()

username = driver.find_element_by_name('username').send_keys('barshan')
password = driver.find_element_by_name('password').send_keys('barshan1234')
username = driver.find_element_by_name('email').send_keys('barshan@gmail.com')

driver.find_element_by_tag_name('button').click()
