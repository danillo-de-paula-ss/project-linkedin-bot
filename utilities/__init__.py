from .driver_settings import start_driver
from .exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException, WebDriverException, SessionNotCreatedException
from selenium.webdriver.support import expected_conditions
from time import sleep
from typing import Any, Callable
import PySimpleGUI as sg
import pyperclip as pc
import threading
import sys
import random
import traceback
import unicodedata

def import_text(window: sg.Window, path: str):
    while True:
        try:
            with open(path, 'rt', encoding='utf-8') as file:
                text = file.read()
            text = '\n'.join([t.strip() for t in text.splitlines()])
            window.write_event_value('import_text_complete', text)
            break
        except RuntimeError:
            sleep(1)

def check_text(text1:str, text2:str, percentage:int) -> bool:
    count = 0
    for char1, char2 in zip(text1, text2):
        if char1 == char2:
            count += 1
    return count >= len(text1) * (percentage / 100)

def avoid_runtime_error(window:sg.Window, message:str = '', text_color:str = 'black', *, write_event:bool = False, key:Any = None, value:Any = None):
    while True:
        try:
            if message != '':
                window['-OUT-'].update(message, text_color_for_value=text_color, append=True)
            if write_event:
                window.write_event_value(key, value)
            break
        except RuntimeError:
            sleep(random.choice([1, 2]))

def start_driver2(window: sg.Window):
    while True:
        thread = threading.current_thread()
        avoid_runtime_error(window, 'Iniciando o navegador... ')
        # window['-OUT-'].update('Iniciando o navegador... ', append=True)
        try:
            driver, wait = start_driver()
        except SessionNotCreatedException:
            avoid_runtime_error(window, 'Erro ao iniciar o navegador!\n', text_color='red')
            continue
        if getattr(thread, 'close_driver', False):
            driver.quit()
            sys.exit()
        avoid_runtime_error(window, 'OK!\n', 'green', write_event=True, key='driver_started', value=(driver, wait))
        # window['-OUT-'].update('OK!\n', text_color_for_value='green', append=True)
        # window.write_event_value('driver_started', (driver, wait))
        break

def open_linkedin(window: sg.Window, driver: WebDriver, wait: WebDriverWait):
    # open Linkedin
    avoid_runtime_error(window, 'Acessando o site do Linkedin... ')
    # window['-OUT-'].update('Acessando o site do Linkedin... ', append=True)
    while True:
        try:
            driver.get('https://www.linkedin.com/')
            break
        except WebDriverException:
            pass
    avoid_runtime_error(window, 'OK!\n', 'green', write_event=True, key='linkedin_is_open', value='')

def check_login_page(window: sg.Window, driver: WebDriver, wait: WebDriverWait):
    # click on signin or reload page
    while True:
        sleep(5)
        try:
            button_login: WebElement = driver.find_element(By.XPATH, '//button[@class="authwall-join-form__form-toggle--bottom form-toggle"]')
            avoid_runtime_error(window, 'Clicando em "Entre"... ')
            # window['-OUT-'].update('Clicando em "Entrar"... ', append=True)
            button_login.click()
            avoid_runtime_error(window, 'OK!\n', 'green')
            # window['-OUT-'].update('OK!\n', text_color_for_value='green', append=True)
            break
        except NoSuchElementException:
            sleep(5)
            try:
                driver.find_element(By.XPATH, '//button[contains(text(),"Entrar")]')
                break
            except NoSuchElementException:
                pass
            avoid_runtime_error(window, 'Recarregando a página... ')
            # window['-OUT-'].update('Recarregando a página... ', append=True)
            driver.execute_script("location.reload()")
            avoid_runtime_error(window, 'OK!\n', 'green')
            # window['-OUT-'].update('OK!\n', text_color_for_value='green', append=True)
    avoid_runtime_error(window, '', write_event=True, key='login_page_is_open', value='')
    # window.write_event_value('login_page_is_open', '')

def login(window: sg.Window, driver: WebDriver, wait: WebDriverWait, username: str, password: str):
    avoid_runtime_error(window, 'Logando no site... ')
    # window['-OUT-'].update('Logando no site... ', append=True)
    username_field: WebElement = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//input[@autocomplete="username"]')))
    username_field.send_keys(username)
    sleep(1)
    password_field: WebElement = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//input[@autocomplete="current-password"]')))
    password_field.send_keys(password)
    sleep(1)
    driver.find_element(By.XPATH, '//button[contains(text(),"Entrar")]').click()
    avoid_runtime_error(window, 'OK!\n', 'green', write_event=True, key='login_complete', value='')

def get_posts(window: sg.Window, driver: WebDriver, wait: WebDriverWait):
    avoid_runtime_error(window, 'Pegando quantidade de postagens... ')
    # window['-OUT-'].update('Pegando quantidade de postagens... ', append=True)
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

        avoid_runtime_error(window, 'OK!\n', 'green', write_event=True, key='number_of_posts_found', value=values_combo)
        # window['-OUT-'].update('OK!\n', text_color_for_value='green', append=True)
        # window.write_event_value('number_of_posts_found', values_combo)
    except (TimeoutException, NoSuchElementException):
        avoid_runtime_error(window, 'ERRO! Postagens não encontradas.\n', 'red', write_event=True, key='number_of_posts_not_found', value='')
        # window['-OUT-'].update('ERRO! Postagens não encontradas.\n', text_color_for_value='red', append=True)
        # window.write_event_value('number_of_posts_not_found', '')

def start_bot(window: sg.Window, driver: WebDriver, wait: WebDriverWait, key_message: str = '', text_to_write: str = '', post_selected: int = 0, wait_time: int = 0, debug:bool = False, find_data_file:Callable = None):
    thread = threading.current_thread()
    action_chains = ActionChains(driver)
    post_found = False
    stop = False
    comment_index = 1
    while not stop:
        # posts
        if comment_index > 0:
            avoid_runtime_error(window, 'Selecionando postagem... ')
            # window['-OUT-'].update('Selecionando postagem... ', append=True)
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
        
        # stop bot if attribute do_run is False
        if not getattr(thread, 'do_run', True):
            stop = True
            avoid_runtime_error(window, 'Operação cancelada!\n', 'red', write_event=True, key='bot_stopped', value='')
            # window['-OUT-'].update('Operação cancelada!\n', text_color_for_value='red', append=True)
            # window.write_event_value('bot_stopped', '')
            continue

        if comment_index <= 0:
            if comment_index == 0:
                avoid_runtime_error(window, 'Erro! Postagem não tem comentários.\n', 'red')
                # window['-OUT-'].update('Erro! Postagem não tem comentários.\n', text_color_for_value='red', append=True)
            elif post_found and comment_index < 0:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                continue
            else:
                avoid_runtime_error(window, 'Erro! Postagem não encontrada.\n', 'red')
                # window['-OUT-'].update('Erro! Postagem não encontrada.\n', text_color_for_value='red', append=True)
            stop = True
            avoid_runtime_error(window, write_event=True, key='bot_stopped', value='')
            # window.write_event_value('bot_stopped', '')
            continue
            
        avoid_runtime_error(window, f'{post_selected + 1}° postagem selecionada.\n', 'green')
        # window['-OUT-'].update(f'{post_selected + 1}° postagem selecionada.\n', text_color_for_value='green', append=True)
        sleep(1)

        # click on the load more messages button
        avoid_runtime_error(window, 'Carregando mais mensagens... ')
        # window['-OUT-'].update('Carregando mais mensagens... ', append=True)

        # stop bot if attribute do_run is False
        if not getattr(thread, 'do_run', True):
            stop = True
            avoid_runtime_error(window, 'Operação cancelada!\n', 'red', write_event=True, key='bot_stopped', value='')
            # window['-OUT-'].update('Operação cancelada!\n', text_color_for_value='red', append=True)
            # window.write_event_value('bot_stopped', '')
            continue

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
        avoid_runtime_error(window, 'OK!\n', 'green')
        # window['-OUT-'].update(f'OK!\n', text_color_for_value='green', append=True)
        sleep(1)

        # main bot
        avoid_runtime_error(window, f'Identificando comentários que possuem a palavra-chave "{key_message}"... ')
        # window['-OUT-'].update(f'Identificando comentários que possuem a palavra-chave "{key_message}"... ', append=True)

        # stop bot if attribute do_run is False
        if not getattr(thread, 'do_run', True):
            stop = True
            avoid_runtime_error(window, 'Operação cancelada!\n', 'red', write_event=True, key='bot_stopped', value='')
            # window['-OUT-'].update('Operação cancelada!\n', text_color_for_value='red', append=True)
            # window.write_event_value('bot_stopped', '')
            continue

        # ./div/div[4]/div/div/div[5 ou 6]/div[3]/div[3]/div/article[1 ou 2]/div[3]/div/div/span/div/span
        comments = post.find_elements(By.XPATH, f'./div/div[4]/div/div/div[{comment_index}]/div[3]/div[3]/div/article/div[3]/div/div/span/div/span')
        comments_text: list[str] = list(map(lambda w: w.text.strip(), comments))
        # //div[@class="scaffold-finite-scroll__content"]/div[5]/div/div[4]/div/div/div[6]/div[3]/div[3]/div/article/div[3]/div/div/span/div/span
        # print(comments_text)

        length = len(list(filter(lambda text: key_message.lower() in text.lower(), comments_text)))
        avoid_runtime_error(window, f'{length} comentário{"s" if length > 1 else ""}.\n', 'green')
        # window['-OUT-'].update(f'{length} comentário{"s" if length > 1 else ""}.\n', text_color_for_value='green', append=True)

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
                avoid_runtime_error(window, 'Respondendo comentário... ')
                # window['-OUT-'].update('Respondendo comentário... ', append=True)

                # stop bot if attribute do_run is False
                if not getattr(thread, 'do_run', True):
                    stop = True
                    break

                # ./div/div[4]/div/div/div[5 ou 6]/div[3]/div[3]/div/article[1 ou 2]/div[4]/div[4]/div[3 ou 4]/div[2]/form/div/div/div/div/div/div/div/div/p
                sleep(2)
                field = post.find_element(By.XPATH, f'./div/div[4]/div/div/div[{comment_index}]/div[3]/div[3]/div/article[{k}]/div[4]/div[4]/div[{len(replies) + 1}]/div[2]/form/div/div/div/div/div/div/div/div/p')
                # field.send_keys(text_to_write.encode('unicode-escape').decode('ASCII'))
                pc.copy(text_to_write)
                sleep(1)
                field.send_keys(Keys().CONTROL, 'v')

                # stop bot if attribute do_run is False
                if not getattr(thread, 'do_run', True):
                    stop = True
                    break

                # ./div/div[4]/div/div/div[5 ou 6]/div[3]/div[3]/div/article[1 ou 2]/div[4]/div[4]/div[3 ou 4]/div[2]/form/div[2]/button
                sleep(2)
                button = post.find_element(By.XPATH, f'./div/div[4]/div/div/div[{comment_index}]/div[3]/div[3]/div/article[{k}]/div[4]/div[4]/div[{len(replies) + 1}]/div[2]/form/div[2]/button')

                # stop bot if attribute do_run is False
                if not getattr(thread, 'do_run', True):
                    stop = True
                    break

                button.click()
                avoid_runtime_error(window, 'OK!\n', 'green')
                # window['-OUT-'].update('OK!\n', text_color_for_value='green', append=True)
                sleep(2)
            elif key_found and reply_found:
                # stop bot if attribute do_run is False
                if not getattr(thread, 'do_run', True):
                    stop = True
                    break
                avoid_runtime_error(window, 'Comentário já respondido.\n')
                # window['-OUT-'].update('Comentário já respondido.\n', append=True)

        
        # stop bot
        if stop:
            avoid_runtime_error(window, 'Operação cancelada!\n', 'red', write_event=True, key='bot_stopped', value='')
            # window['-OUT-'].update('Operação cancelada!\n', text_color_for_value='red', append=True)
            # window.write_event_value('bot_stopped', '')
            continue
        
        avoid_runtime_error(window, f'Esperando {wait_time} minuto{"s" if wait_time > 1 else ""}... ')
        # window['-OUT-'].update(f'Esperando {wait_time} minuto{"s" if wait_time > 1 else ""}... ', append=True)
        for _ in range(wait_time * 60):
            if not getattr(thread, 'do_run', True):
                stop = True
                break
            else:
                sleep(1)
        
        # stop bot
        if stop:
            avoid_runtime_error(window, 'Operação cancelada!\n', 'red', write_event=True, key='bot_stopped', value='')
            # window['-OUT-'].update('Operação cancelada!\n', text_color_for_value='red', append=True)
            # window.write_event_value('bot_stopped', '')
            continue
        else:
            avoid_runtime_error(window, 'OK!\n', 'green')
            # window['-OUT-'].update('OK!\n', text_color_for_value='green', append=True)
            avoid_runtime_error(window, 'Recarregando a página... ')
            # window['-OUT-'].update('Recarregando a página... ', append=True)
            driver.execute_script("location.reload()")
            sleep(5)
            driver.execute_script("window.scrollTo(0, -document.body.scrollHeight)")
            sleep(1)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            avoid_runtime_error(window, 'OK!\n', 'green')
            # window['-OUT-'].update('OK!\n', text_color_for_value='green', append=True)
            post_found = True

def start_bot2(window:sg.Window, driver:WebDriver, wait:WebDriverWait, key_message:str = '', text_to_write:str = '', page_scrolls:int = 0, wait_time:int = 0, debug:bool = False, find_data_file:Callable = None):
    first = True
    is_other_tab = False
    if debug:
        with open(find_data_file('replies.txt'), 'wt', encoding='utf-8') as file:
            pass
    while True:
        try:
            if first:
                thread = threading.current_thread()
                action_chains = ActionChains(driver)
                try:
                    avoid_runtime_error(window, 'Clicando em "Atividades"... ')
                    activity_button: WebElement = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//span[text()="Atividades"]')))
                    button_y = activity_button.location['y']
                    i = 1
                    while True:
                        try:
                            activity_button.click()
                            break
                        except ElementClickInterceptedException:
                            driver.execute_script(f"window.scrollTo(0, {button_y - i * 100})")
                            sleep(1)
                            i += 1
                    
                    # stop bot
                    if not getattr(thread, 'do_run', True):
                        raise BotStopped
                    
                    avoid_runtime_error(window, 'OK!\n', 'green')
                    avoid_runtime_error(window, 'Filtrando comentários... ')
                    filter_button: WebElement = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//button[@role="checkbox" and contains(@aria-label, "Coment")]')))
                    
                    # stop bot
                    if not getattr(thread, 'do_run', True):
                        raise BotStopped
                    
                    if filter_button.get_attribute('aria-checked') == 'false':
                        button_y = filter_button.location['y']
                        i = 1
                        while True:
                            try:
                                filter_button.click()
                                break
                            except ElementClickInterceptedException:
                                driver.execute_script(f"window.scrollTo(0, {button_y - i * 100})")
                                sleep(1)
                                i += 1
                except TimeoutException:
                    pass
                
                # stop bot
                if not getattr(thread, 'do_run', True):
                    raise BotStopped
                
                avoid_runtime_error(window, 'OK!\n', 'green')
            else:
                driver.execute_script("window.scrollTo(0, -document.body.scrollHeight)")
                avoid_runtime_error(window, 'Recarregando a página... ')
                sleep(1)
                driver.execute_script("location.reload()")
                
                # stop bot
                if not getattr(thread, 'do_run', True):
                    raise BotStopped
                
                sleep(3)
                avoid_runtime_error(window, 'OK!\n', 'green')

            sleep(5)
            for _ in range(page_scrolls):
                avoid_runtime_error(window, 'Rolando a página para baixo... ')
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

                # stop bot
                if not getattr(thread, 'do_run', True):
                    raise BotStopped
                
                sleep(3)
                avoid_runtime_error(window, 'OK!\n', 'green')

            avoid_runtime_error(window, 'Encontrando comentários... ')
            comments: list[WebElement] = wait.until(expected_conditions.presence_of_all_elements_located((By.XPATH, '//div[@class="scaffold-finite-scroll__content"]/div/div/article/div[2]')))

            # stop bot
            if not getattr(thread, 'do_run', True):
                raise BotStopped
            
            comments_text = [comment.find_element(By.XPATH, './button/div/span').text for comment in comments]
            length_comments = len(comments)
            avoid_runtime_error(window, f'{length_comments} encontrado{"s" if len(comments) != 1 else ""}.\n', 'green')
            initial_tab = driver.current_window_handle
            for k, comment, comment_text in zip(range(1, len(comments) + 1), comments, comments_text):
                is_other_tab = False
                sleep(2)
                avoid_runtime_error(window, f'{k}º comentário.\n')
                avoid_runtime_error(window, 'Identificando se o comentário contém a palavra chave... ')

                # stop bot
                if not getattr(thread, 'do_run', True):
                    raise BotStopped

                if key_message.lower() in comment_text.lower():
                    avoid_runtime_error(window, 'OK!\n', 'green')
                    avoid_runtime_error(window, 'Clicando em "Responder"... ')
                    
                    # stop bot
                    if not getattr(thread, 'do_run', True):
                        raise BotStopped
                    
                    button = comment.find_element(By.XPATH, './div/div/button')
                    button_y = button.location['y']
                    i = 1
                    while True:
                        try:
                            button.click()
                            break
                        except ElementClickInterceptedException:
                            driver.execute_script(f"window.scrollTo(0, {button_y - i * 100})")
                            sleep(1)
                            i += 1
                    avoid_runtime_error(window, 'OK!\n', 'green')
                    avoid_runtime_error(window, 'Trocando de aba... ')
                    tabs = driver.window_handles

                    # stop bot
                    if not getattr(thread, 'do_run', True):
                        raise BotStopped

                    for tab in tabs:
                        sleep(1)

                        # stop bot
                        if not getattr(thread, 'do_run', True):
                            raise BotStopped

                        if tab not in initial_tab:
                            is_other_tab = True
                            driver.switch_to.window(tab)
                            sleep(10)

                            # stop bot
                            if not getattr(thread, 'do_run', True):
                                raise BotStopped

                            avoid_runtime_error(window, 'OK!\n', 'green')
                            data_id = driver.current_url.split('%')[-2].removeprefix('2C')
                            avoid_runtime_error(window, 'Identificando se o comentário já foi respondido... ')
                            # try:
                            replies: list[WebElement] = driver.find_elements(By.XPATH, f'//article[contains(@data-id, "{data_id}")]/div[6]/div[4]/div/article/div[3]/div/div/span/div/span/span')
                            # except NoSuchElementException:
                            #     replies = []
                            replies_text = [reply.get_attribute('innerText') for reply in replies]
                            # reply_found = any(map(lambda reply: reply == text_to_write, replies_text))
                            # reply_found = any(map(lambda reply: check_text(text_to_write, reply, 80), replies_text))
                            reply_found = any(map(lambda reply: check_text(
                                ''.join([t for t in text_to_write if t not in ' \n']),
                                ''.join([t for t in unicodedata.normalize("NFKC", reply) if t not in ' \n']),
                                80), replies_text))

                            if debug:
                                with open(find_data_file('replies.txt'), 'at', encoding='utf-8') as file:
                                    file.write(f'url: {driver.current_url}\n')
                                    file.write(f'id: {data_id}\n')
                                    file.write(f'reply_found: {reply_found}\n')
                                    file.write(f'text to write: {text_to_write}\n')
                                    for k, text in enumerate(replies_text, 1):
                                        file.write(f'{k}° reply: {text}\n')
                                    file.write('\n')

                            # stop bot
                            if not getattr(thread, 'do_run', True):
                                raise BotStopped

                            if not reply_found:
                                avoid_runtime_error(window, 'Comentário não foi respondido ainda!\n', 'red')
                                avoid_runtime_error(window, 'Respondendo comentário... ')
                                # pc.copy(text_to_write)

                                # stop bot
                                if not getattr(thread, 'do_run', True):
                                    raise BotStopped

                                sleep(1)
                                # driver.find_element(By.XPATH, '//div[contains(@data-placeholder, "Responder em nome de")]/p').send_keys(Keys().CONTROL, 'v')
                                texts = text_to_write.splitlines()
                                for k in range(len(texts)):
                                    fields = driver.find_elements(By.XPATH, '//div[contains(@data-placeholder, "Responder em nome de")]/p')
                                    driver.execute_script(f"arguments[0].innerHTML = '{texts[k]}'",
                                                          fields[k])
                                    fields[k].send_keys(Keys.END + Keys.ARROW_DOWN * 10 + \
                                                        ('\n.' if k + 1 < len(texts) else ''))
                                
                                # stop bot
                                if not getattr(thread, 'do_run', True):
                                    raise BotStopped
                                
                                sleep(2)
                                driver.find_element(By.XPATH, '//form[@class="comments-comment-box__form"]/div/button[contains(@aria-label, "Responder ao comentário de")]').click()
                                avoid_runtime_error(window, 'OK!\n', 'green')
                            else:
                                avoid_runtime_error(window, 'Comentário já foi respondido!\n', 'green')
                            sleep(2)
                            driver.close()
                            driver.switch_to.window(initial_tab)
                else:
                    avoid_runtime_error(window, 'Não contém!\n', 'red')
            avoid_runtime_error(window, f'Esperando {wait_time} minuto{"s" if wait_time > 1 else ""}... ')
            for _ in range(wait_time * 60):
                if not getattr(thread, 'do_run', True):
                    raise BotStopped
                else:
                    sleep(1)
            avoid_runtime_error(window, 'OK!\n', 'green')
        except Exception as err:
            if isinstance(err, BotStopped):
                avoid_runtime_error(window, 'Bot encerrado!\n', 'red', write_event=True, key='bot_stopped', value='')
                if is_other_tab:
                    driver.close()
                    driver.switch_to.window(initial_tab)
            else:
                exc_type, exc_value, exc_tb = sys.exc_info()
                tb = traceback.TracebackException(exc_type, exc_value, exc_tb)
                tb_txt = "".join(tb.format_exception_only())
                print(tb_txt)
                if is_other_tab:
                    driver.close()
                    driver.switch_to.window(initial_tab)
                avoid_runtime_error(window, 'Erro encontrado! Bot encerrado!\n', 'red', write_event=True, key='bot_stopped', value='')
            break
        else:
            first = False
