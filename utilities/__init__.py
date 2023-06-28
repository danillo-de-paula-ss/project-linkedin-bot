from utilities.driver_settings import start_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException, WebDriverException
from selenium.webdriver.support import expected_conditions
from time import sleep
from typing import Any
import PySimpleGUI as sg
import pyperclip as pc
import threading
import sys
import random

def import_text(window: sg.Window, path: str):
    with open(path, 'rt', encoding='utf-8') as file:
        window['-TEXT-TO-WRITE-'].update(file.read())
    window.write_event_value('import_text_complete', '')

def avoid_runtime_error(window: sg.Window, key: Any, value: Any, *, write_event: bool, message: str = '', text_color: str = 'black'):
    while True:
        try:
            window['-OUT-'].update(message, text_color_for_value=text_color, append=True)
            if write_event:
                window.write_event_value(key, value)
            break
        except RuntimeError:
            sleep(5)

def start_driver2(window: sg.Window):
    thread = threading.current_thread()
    window['-OUT-'].update('Iniciando o navegador... ', append=True)
    driver, wait = start_driver()
    if getattr(thread, 'close_driver', False):
        driver.quit()
        sys.exit()
    avoid_runtime_error(window, 'driver_started', (driver, wait), write_event=True, message='OK!\n', text_color='green')
    # window['-OUT-'].update('OK!\n', text_color_for_value='green', append=True)
    # window.write_event_value('driver_started', (driver, wait))

def open_linkedin(window: sg.Window, driver: WebDriver, wait: WebDriverWait):
    # open Linkedin
    window['-OUT-'].update('Acessando o site do Linkedin... ', append=True)
    while True:
        try:
            driver.get('https://www.linkedin.com/')
            break
        except WebDriverException:
            pass
    avoid_runtime_error(window, 'linkedin_is_open', '', write_event=True, message='OK!\n', text_color='green')

def check_login_page(window: sg.Window, driver: WebDriver, wait: WebDriverWait):
    # click on signin or reload page
    while True:
        sleep(5)
        try:
            button_login: WebElement = driver.find_element(By.XPATH, '//button[@class="authwall-join-form__form-toggle--bottom form-toggle"]')
            window['-OUT-'].update('Clicando em "Entrar"... ', append=True)
            button_login.click()
            window['-OUT-'].update('OK!\n', text_color_for_value='green', append=True)
            break
        except NoSuchElementException:
            sleep(5)
            try:
                driver.find_element(By.XPATH, '//button[contains(text(),"Entrar")]')
                break
            except NoSuchElementException:
                pass
            window['-OUT-'].update('Recarregando a página... ', append=True)
            driver.execute_script("location.reload()")
            window['-OUT-'].update('OK!\n', text_color_for_value='green', append=True)
    window.write_event_value('login_page_is_open', '')

def login(window: sg.Window, driver: WebDriver, wait: WebDriverWait, username: str, password: str):
    window['-OUT-'].update('Logando no site... ', append=True)
    username_field: WebElement = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//input[@autocomplete="username"]')))
    username_field.send_keys(username)
    sleep(1)
    password_field: WebElement = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//input[@autocomplete="current-password"]')))
    password_field.send_keys(password)
    sleep(1)
    driver.find_element(By.XPATH, '//button[contains(text(),"Entrar")]').click()
    avoid_runtime_error(window, 'login_complete', '', write_event=True, message='OK!\n', text_color='green')

def get_posts(window: sg.Window, driver: WebDriver, wait: WebDriverWait):
    window['-OUT-'].update('Pegando quantidade de postagens... ', append=True)
    try:
        posts: list[WebElement] = wait.until(expected_conditions.presence_of_all_elements_located((By.XPATH, '//div[@class="scaffold-finite-scroll__content"]/div')))
        # ./div/div/div/div/div[4]/div/div/span/span
        texts: list[str] = [post.find_element(By.XPATH, './div/div/div/div/div[4]/div/div/span/span').text for post in posts]
        # ./div/div/div/div/div[2]/a/div[3]/span[3]/div/span/span
        last_releases: list[str] = [post.find_element(By.XPATH, './div/div/div/div/div[2]/a/div[3]/span[3]/div/span/span').text for post in posts]
        # ./div/div[4]/div/div/div[5]/ul/li/button/span
        comments: list[str] = []
        for post in posts:
            text = ''
            for k in range(5, 10):
                try:
                    l = 1
                    while l >= 0:
                        # /div/div[4]/div/div/div[6]/ul/li[2]/button
                        text = post.find_element(By.XPATH, f'./div/div[4]/div/div/div[{k}]/ul/li[{l}]/button/span').text
                        if 'comentário' in text:
                            break
                        l += 1
                    break
                except NoSuchElementException:
                    text = '0 comentários'
            comments.append(text)
        
        # make values for combo element
        values_combo = [t[:30] + '[...] - ' + r[:-2] + ' - ' + c for t, r, c in zip(texts, last_releases, comments)]

        window['-OUT-'].update('OK!\n', text_color_for_value='green', append=True)
        window.write_event_value('number_of_posts_found', values_combo)
    except (TimeoutException, NoSuchElementException):
        window['-OUT-'].update('ERRO! Postagens não encontradas.\n', text_color_for_value='red', append=True)
        window.write_event_value('number_of_posts_not_found', '')

def start_bot(window: sg.Window, driver: WebDriver, wait: WebDriverWait, key_message: str = '', text_to_write: str = '', post_selected: int = 0, wait_time: int = 0):
    thread = threading.current_thread()
    action_chains = ActionChains(driver)
    post_found = False
    stop = False
    comment_index = 1
    while not stop:
        # posts
        if comment_index > 0:
            window['-OUT-'].update('Selecionando postagem... ', append=True)
        # //div[@class="scaffold-finite-scroll__content"]/div
        posts: list[WebElement] = wait.until(expected_conditions.presence_of_all_elements_located((By.XPATH, '//div[@class="scaffold-finite-scroll__content"]/div')))
        try:
            post = posts[post_selected]
            action_chains.move_to_element(post)
            for k in range(4, 10):
                try:
                    index = 1
                    while index >= 0:
                        # ./div/div[4]/div/div/div[5 ou 6]/ul/li[7 ou 8]/button
                        button = post.find_element(By.XPATH, f'./div/div[4]/div/div/div[{k}]/ul/li[{index}]/button')
                        if 'comentário' in button.find_element(By.XPATH, './span').text:
                            break
                        index += 1
                except NoSuchElementException:
                    pass
                else:
                    action_chains.move_to_element_with_offset(button, 0, -200)
                    button_y = button.location['y']
                    while True:
                        try:
                            button.click()
                            break
                        except ElementClickInterceptedException:
                            driver.execute_script(f"window.scrollTo(0, {button_y - 300})")
                            sleep(1)
                    comment_index = k
                    break
        except IndexError:
            comment_index = -1
        
        # print(comment_index)

        if comment_index <= 0:
            if comment_index == 0:
                window['-OUT-'].update('Erro! Postagem não tem comentários.\n', text_color_for_value='red', append=True)
            elif post_found and comment_index < 0:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                continue
            else:
                window['-OUT-'].update('Erro! Postagem não encontrada.\n', text_color_for_value='red', append=True)
            stop = True
            window.write_event_value('bot_stopped', '')
            continue
            
        window['-OUT-'].update(f'{post_selected + 1}° postagem selecionada.\n', text_color_for_value='green', append=True)
        sleep(2)

        # click on the load more messages button
        window['-OUT-'].update('Carregando mais mensagens... ', append=True)
        while True:
            try:
                # ./div/div[4]/div/div/div[5 ou 6]/div[3]/div[3]/div[2]/button
                button = post.find_element(By.XPATH, f'./div/div[4]/div/div/div[{comment_index}]/div[3]/div[3]/div[2]/button')
                action_chains.move_to_element_with_offset(button, 0, -200)
                button.click()
                sleep(3)
            except NoSuchElementException:
                break
            except ElementClickInterceptedException:
                action_chains.move_to_element_with_offset(button, 0, -300)
        window['-OUT-'].update(f'OK!\n', text_color_for_value='green', append=True)
        sleep(2)

        # main bot
        window['-OUT-'].update(f'Identificando comentários que possuem a palavra-chave "{key_message}"... ', append=True)

        # stop bot if attribute do_run is False
        if not getattr(thread, 'do_run', True):
            stop = True
            window['-OUT-'].update('Operação cancelada!\n', text_color_for_value='red', append=True)
            window.write_event_value('bot_stopped', '')
            continue

        # ./div/div[4]/div/div/div[5 ou 6]/div[3]/div[3]/div/article[1 ou 2]/div[3]/div/div/span/div/span
        comments = post.find_elements(By.XPATH, f'./div/div[4]/div/div/div[{comment_index}]/div[3]/div[3]/div/article/div[3]/div/div/span/div/span')
        comments_text: list[str] = list(map(lambda w: w.text.strip(), comments))
        # //div[@class="scaffold-finite-scroll__content"]/div[5]/div/div[4]/div/div/div[6]/div[3]/div[3]/div/article/div[3]/div/div/span/div/span
        # print(comments_text)

        length = len(list(filter(lambda text: key_message.lower() in text.lower(), comments_text)))
        window['-OUT-'].update(f'{length} comentário{"s" if length > 1 else ""}.\n', text_color_for_value='green', append=True)

        # ./div/div[4]/div/div/div[5 ou 6]/div[3]/div[3]/div/article[1 ou 2]/div[4]/div[2]/div/div[3]/button
        response_buttons = post.find_elements(By.XPATH, f'./div/div[4]/div/div/div[{comment_index}]/div[3]/div[3]/div/article/div[4]/div[2]/div/div[3]/button')
        for k, response_button, text in zip(range(1, len(comments_text) + 1), response_buttons, comments_text):
            action_chains.move_to_element_with_offset(response_button, 0, -200)
            # click on the load previous messages button
            while True:
                try:
                    # ./div/div[4]/div/div/div[5 ou 6]/div[3]/div[3]/div/article/div[4]/div[4]/div/button
                    button = post.find_element(By.XPATH, f'./div/div[4]/div/div/div[{comment_index}]/div[3]/div[3]/div/article[{k}]/div[4]/div[4]/div/button')
                    action_chains.move_to_element_with_offset(button, 0, -200)
                    button.click()
                    break
                except NoSuchElementException:
                    break
                except ElementClickInterceptedException:
                    action_chains.move_to_element_with_offset(button, 0, -300)

            # detect if link has been shared
            # ./div/div[4]/div/div/div[5 ou 6]/div[3]/div[3]/div/article[1 ou 2]/div[4]/div[4]/div[1]/article[3 ou 4]/div[3]/div/div/span/div/span
            replies = post.find_elements(By.XPATH, f'./div/div[4]/div/div/div[{comment_index}]/div[3]/div[3]/div/article[{k}]/div[4]/div[4]/div[1]/article/div[3]/div/div/span/div/span')
            replies_text = [reply.get_attribute('innerText').replace('\xa0', ' ') for reply in replies]
            
            # stop bot if attribute do_run is False
            if not getattr(thread, 'do_run', True):
                stop = True
                break

            # detect key message in comments
            key_found = key_message.lower() in text.lower()
            reply_found = any(map(lambda reply: reply == text_to_write, replies_text))
            if key_found and not reply_found:
                button_y = response_button.location['y']
                while True:
                    try:
                        action_chains.move_to_element_with_offset(response_button, 0, 0)
                        sleep(1)
                        response_button.click()
                        break
                    except ElementClickInterceptedException:
                        y = random.choice([400, -400])
                        driver.execute_script(f"window.scrollTo(0, {button_y - y})")
                window['-OUT-'].update('Respondendo comentário... ', append=True)
                # ./div/div[4]/div/div/div[5 ou 6]/div[3]/div[3]/div/article[1 ou 2]/div[4]/div[4]/div[3 ou 4]/div[2]/form/div/div/div/div/div/div/div/div/p
                sleep(2)
                field = post.find_element(By.XPATH, f'./div/div[4]/div/div/div[{comment_index}]/div[3]/div[3]/div/article[{k}]/div[4]/div[4]/div[{len(replies) + 1}]/div[2]/form/div/div/div/div/div/div/div/div/p')
                # field.send_keys(text_to_write.encode('unicode-escape').decode('ASCII'))
                pc.copy(text_to_write)
                sleep(1)
                field.send_keys(Keys().CONTROL, 'v')
                # ./div/div[4]/div/div/div[5 ou 6]/div[3]/div[3]/div/article[1 ou 2]/div[4]/div[4]/div[3 ou 4]/div[2]/form/div[2]/button
                sleep(2)
                button = post.find_element(By.XPATH, f'./div/div[4]/div/div/div[{comment_index}]/div[3]/div[3]/div/article[{k}]/div[4]/div[4]/div[{len(replies) + 1}]/div[2]/form/div[2]/button')
                button.click()
                window['-OUT-'].update('OK!\n', text_color_for_value='green', append=True)
                sleep(2)
            elif key_found and reply_found:
                window['-OUT-'].update('Comentário já respondido.\n', append=True)
        
        # stop bot
        if stop:
            window['-OUT-'].update('Operação cancelada!\n', text_color_for_value='red', append=True)
            window.write_event_value('bot_stopped', '')
            continue
        
        window['-OUT-'].update(f'Esperando {wait_time} minuto{"s" if wait_time > 1 else ""}... ', append=True)
        for _ in range(wait_time * 60):
            if not getattr(thread, 'do_run', True):
                stop = True
                break
            else:
                sleep(1)
        
        # stop bot
        if stop:
            window['-OUT-'].update('Operação cancelada!\n', text_color_for_value='red', append=True)
            window.write_event_value('bot_stopped', '')
            continue
        else:
            window['-OUT-'].update('OK!\n', text_color_for_value='green', append=True)
            window['-OUT-'].update('Recarregando a página... ', append=True)
            driver.execute_script("location.reload()")
            sleep(5)
            driver.execute_script("window.scrollTo(0, -document.body.scrollHeight)")
            sleep(1)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            window['-OUT-'].update('OK!\n', text_color_for_value='green', append=True)
            post_found = True
