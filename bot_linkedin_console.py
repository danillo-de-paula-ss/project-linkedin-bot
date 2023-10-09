from utilities.driver_settings import start_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from time import sleep
import os
import threading
import sys

def main_program(driver: WebDriver, wait: WebDriverWait, key_message: str, link_to_share: str, post_selected: int, wait_time: int):
    thread = threading.current_thread()
    stop = False
    while not stop:
        driver.execute_script("window.scrollTo(0, -document.body.scrollHeight)") 
        # posts
        print('Selecionando postagem...')
        posts: list[WebElement] = wait.until(expected_conditions.presence_of_all_elements_located((By.XPATH, '//li[@class="profile-creator-shared-feed-update__container"]')))
        y = 0
        while True:
            try:
                post = posts[post_selected]
                post.find_element(By.XPATH, './div/div/div[2]/div/div[5]/ul/li/button/span').click()
                break
            except IndexError:
                print('Erro! Postagem não encontrada.\nPressione ENTER para fechar o programa.')
                break
            except NoSuchElementException:
                print('Postagem não tem comentários.\nPressione ENTER para fechar o programa.')
                break
            except ElementClickInterceptedException:
                y += 10
                driver.execute_script(f"window.scrollTo(0, {y})") 
                # print('Recarregando a página...')
                # driver.execute_script("location.reload()")
                # sleep(5)
                # continue
        sleep(2)

        # click on the load more messages button
        print('Carregando mais mensagens...')
        y = 0
        while True:
            try:
                post.find_element(By.XPATH, './div/div/div[2]/div/div[5]/div[4]/div[3]/div[2]/button').click()
                break
            except NoSuchElementException:
                break
            except ElementClickInterceptedException:
                y += 10
                driver.execute_script(f"window.scrollTo(0, {y})") 
        sleep(2)

        # main bot
        print(f'Identificando comentários que possuem a palavra-chave "{key_message}"...')
        comments = post.find_elements(By.XPATH, './div/div/div[2]/div/div[5]/div[4]/div[3]/div/article/div[3]/div/div/span/div/span')
        comment_texts = list(map(lambda w: w.text, comments))
        buttons_ans = post.find_elements(By.XPATH, './div/div/div[2]/div/div[5]/div[4]/div[3]/div/article/div[4]/div[2]/div/div[3]/button')
        k = 1
        for button_ans, text in zip(buttons_ans, comment_texts):
            # click on the load previous messages button
            y = 0
            while True:
                try:
                    post.find_element(By.XPATH, f'./div/div/div[2]/div/div[5]/div[4]/div[3]/div[1]/article[{k}]/div[4]/div[4]/div/button').click()
                    break
                except NoSuchElementException:
                    break
                except ElementClickInterceptedException:
                    y += 10
                    driver.execute_script(f"window.scrollTo(0, {y})") 

            # detect if link has been shared
            reply_comments = post.find_elements(By.XPATH, f'./div/div/div[2]/div/div[5]/div[4]/div[3]/div/article[{k}]/div[4]/div[4]/div[1]/article/div[3]/div/div/span/div/span')
            href_texts = []
            if reply_comments:
                for comment in reply_comments:
                    try:
                        href_text = comment.find_element(By.XPATH, './a').text
                        href_texts.append(href_text)
                    except NoSuchElementException:
                        pass
            
            # detect key message in comments
            if text.lower() == key_message.lower() and link_to_share not in href_texts:
                button_ans.click()
                sleep(2)
                field = post.find_element(By.XPATH, f'./div/div/div[2]/div/div[5]/div[4]/div[3]/div/article[{k}]/div[4]/div[4]/div[{len(reply_comments) + 1}]/div[2]/form/div/div/div[1]/div/div/div/div/div[1]/p')
                field.send_keys(link_to_share)
                sleep(2)
                button = post.find_element(By.XPATH, f'./div/div/div[2]/div/div[5]/div[4]/div[3]/div/article[{k}]/div[4]/div[4]/div[{len(reply_comments) + 1}]/div[2]/form/div[2]/button')
                button.click()
                sleep(2)
            k += 1
        print(f'Esperando {wait_time} segundo{"s" if wait_time > 1 else ""}...')
        for _ in range(wait_time):
            if not getattr(thread, 'do_run', True):
                stop = True
                break
            sleep(1)
        if not stop:
            print('Recarregando a página...')
            driver.execute_script("location.reload()")
            sleep(5)

# Find path
def find_data_file(filename):
    if getattr(sys, "frozen", False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)
    return os.path.join(datadir, filename)

if __name__ == '__main__':
    with open(find_data_file('settings.txt'), 'rt', encoding='utf-8') as file:
        lines = file.readlines()
        my_username = lines[0].split('=')[-1].strip()
        my_password = lines[1].split('=')[-1].strip()
        key_message = lines[2].split('=')[-1].strip()
        link_to_share = lines[3].split('=')[-1].strip()
        post_selected = int(lines[4].split('=')[-1].strip())
        wait_time = int(lines[5].split('=')[-1].strip())
        captcha_time = int(lines[6].split('=')[-1].strip())

    print('Iniciando navegador...')
    driver, wait = start_driver()
    # my_username = ''
    # my_password = ''
    # key_message = 'Eu quero'
    # link_to_share = 'https://www.youtube.com/'
    # post_selected = 0
    # wait_time = 10
    # captcha_time = 60

    # open Linkedin
    print('Acessando o site do Linkedin...')
    driver.get('https://www.linkedin.com/')

    # click on sign in or reload page
    while True:
        sleep(1)
        try:
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

    # login
    print('Logando no site...')
    username_field: WebElement = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//input[@autocomplete="username"]')))
    for char in my_username:
        username_field.send_keys(char)
    sleep(1)
    password_field: WebElement = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//input[@autocomplete="current-password"]')))
    for char in my_password:
        password_field.send_keys(char)
    sleep(1)
    driver.find_element(By.XPATH, '//button[contains(text(),"Entrar")]').click()

    # time to solve CAPTCHA
    if captcha_time > 0:
        print(f'Resolva o CAPTCHA! Você tem {captcha_time} segundo{"s" if wait_time > 1 else ""} para resolver.')
    sleep(captcha_time)

    # main page
    print('Acessando postagens...')
    button_profile: WebElement = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//button[@class="global-nav__primary-link global-nav__primary-link-me-menu-trigger artdeco-dropdown__trigger artdeco-dropdown__trigger--placement-bottom ember-view"]')))
    button_profile.click()
    sleep(2)
    button_activity: WebElement = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//a[contains(@href,"recent-activity")]')))
    button_activity.click()

    thread = threading.Thread(target=main_program, args=(driver, wait, key_message, link_to_share, post_selected, wait_time), daemon=True)
    thread.start()
    input('Pressione ENTER para fechar o programa.')
    print('Encerrando o programa...')
    thread.do_run = False
    thread.join()
    driver.quit()
