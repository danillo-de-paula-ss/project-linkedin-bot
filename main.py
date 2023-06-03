from drive_settings import start_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from time import sleep
import pyautogui as pg
import keyboard
import threading
import sys


# def repetir_processo(driver: WebDriver, wait: WebDriverWait):
    # thread = threading.current_thread()
    # stop = False
    # while stop == False:
    #     # navegar até a página alvo
    #     driver.get('https://www.instagram.com/devaprender/')
    #     sleep(5)
    #     # clicar na última postagem
    #     postagens: list[WebElement] = wait.until(expected_conditions.visibility_of_any_elements_located(
    #         (By.XPATH, '//div[@class="_aabd _aa8k _aanf"]')))
    #     postagens[0].click()
    #     sleep(5)
    #     # verificar se postagem foi curtida, caso não tenha sido, clicar em curtir, caso já tenha sido, aguardar 24 horas
    #     elementos_postagens: list[WebElement] = wait.until(
    #         expected_conditions.visibility_of_any_elements_located((By.XPATH, '//div[@class="_abm0 _abl_"]')))
    #     if len(elementos_postagens) == 7:
    #         elementos_postagens[1].click()
    #     else:
    #         print('postagem já foi curtida')
    #     for _ in range(86400):
    #         if getattr(thread, 'do_run', True) == False:
    #             stop = True
    #             break
    #         sleep(1)


driver, wait = start_driver()
my_username = 'nerdpesquisando@gmail.com'
my_password = 'sagavazas1234'

# open Linkedin
driver.get('https://www.linkedin.com/')

# login
while True:
    sleep(1)
    try:
        # button_login: WebElement = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//button[@class="authwall-join-form__form-toggle--bottom form-toggle"]')))
        button_login: WebElement = driver.find_element(By.XPATH, '//button[@class="authwall-join-form__form-toggle--bottom form-toggle"]')
        button_login.click()
        break
    except NoSuchElementException:
        try:
            driver.find_element(By.XPATH, '//input[@autocomplete="username"]')
            break
        except NoSuchElementException:
            pass
        driver.execute_script("location.reload()")

username_field: WebElement = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//input[@autocomplete="username"]')))
username_field.send_keys(my_username)
sleep(1)
password_field: WebElement = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//input[@autocomplete="current-password"]')))
password_field.send_keys(my_password)
sleep(1)
driver.find_element(By.XPATH, '//button[contains(text(),"Entrar")]').click()

sleep(30 * 2)

# main page
button_profile: WebElement = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//button[@class="global-nav__primary-link global-nav__primary-link-me-menu-trigger artdeco-dropdown__trigger artdeco-dropdown__trigger--placement-bottom ember-view"]')))
button_profile.click()
sleep(2)
button_activity: WebElement = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//a[contains(@href,"recent-activity")]')))
button_activity.click()

# posts
posts: list[WebElement] = wait.until(expected_conditions.presence_of_all_elements_located((By.XPATH, '//li[@class="profile-creator-shared-feed-update__container"]')))
post_selected = 0
try:
    post = posts[post_selected]
    post.find_element(By.XPATH, './div/div/div[2]/div/div[5]/ul/li/button/span').click()
except (IndexError, NoSuchElementException):
    driver.quit()
    sys.exit()
sleep(2)
# comments: list[WebElement] = wait.until(expected_conditions.presence_of_all_elements_located((By.XPATH, '//div[@class="update-components-text relative"]/span')))
comments = post.find_elements(By.XPATH, './div/div/div[2]/div/div[5]/div[4]/div[3]/div/article/div[3]/div/div/span/div/span')
texts = list(map(lambda w: w.text, comments))
print(texts)
# /html/body/div[4]/div[3]/div/div/div[2]/div/div/main/div/section/div[2]/div/div/div[1]/ul/li[1]/div/div/div[2]/div/div[5]/div[3]/div[3]/div/article[1]/div[4]/div[2]/div/div[3]/button
buttons_answer = post.find_elements(By.XPATH, './div/div/div[2]/div/div[5]/div[4]/div[3]/div/article/div[4]/div[2]/div/div[3]/button')
for k, text in enumerate(texts):
    if text == 'Eu quero':
        buttons_answer[k].click()
        sleep(2)
        field = post.find_elements(By.XPATH, './div/div/div[2]/div/div[5]/div[4]/div[3]/div/article/div[4]/div[4]/div[2]/div[2]/form/div/div/div[1]/div/div/div/div/div[1]/p')
        field[0].send_keys('https://www.youtube.com/')
        sleep(2)
        button = post.find_elements(By.XPATH, './div/div/div[2]/div/div[5]/div[4]/div[3]/div/article/div[4]/div[4]/div[2]/div[2]/form/div[2]/button')
        button[0].click()
        sleep(2)
# //div[@class="comments-comment-item__nested-items"]/div/div[2]/form/div/div/div/div/div/div/div/div/p
# //div[@class="comments-comment-item__nested-items"]/div/div[2]/form/div[2]/button

keyboard.wait('f1')
driver.quit()
# # clicar e digitar o meu usuário
# campo_usuario: WebElement = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//input[@name="username"]')))
# campo_usuario.send_keys('danillodepaula238@gmail.com')
# sleep(3)
# # clicar e digitar a minha senha
# campo_senha: WebElement = wait.until(expected_conditions.element_to_be_clickable(
#     (By.XPATH, '//input[@name="password"]')))
# campo_senha.send_keys('sagavazas')
# sleep(3)
# # clicar no campo entrar
# botao_entrar: WebElement = wait.until(
#     expected_conditions.element_to_be_clickable((By.XPATH, '//div[text()="Entrar"]')))
# botao_entrar.click()
# sleep(3)
# thread = threading.Thread(target=repetir_processo, args=(driver, wait), daemon=True)
# thread.start()
# while keyboard.is_pressed('1') == False:
#     pass
# thread.do_run = False
# thread.join()
# driver.quit()
