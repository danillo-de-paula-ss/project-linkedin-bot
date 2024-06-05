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
# import pyperclip as pc
import threading
import sys
import random
import traceback
import unicodedata
from .crash_files import create_crash_file

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
    attempts = 0
    while True:
        try:
            if message != '':
                window['-OUT-'].update(message, text_color_for_value=text_color, append=True)
            if write_event:
                window.write_event_value(key, value)
            break
        except RuntimeError:
            sleep(random.choice([1, 2]))
            attempts += 1
            if attempts > 10:
                break

def start_driver2(window: sg.Window, find_data_file: Callable[[str], str]):
    attempt = 0
    while True:
        thread = threading.current_thread()
        avoid_runtime_error(window, 'Iniciando o navegador... ')
        try:
            driver, wait = start_driver()
        except SessionNotCreatedException:
            if getattr(thread, 'close_driver', False):
                sys.exit()
            attempt += 1
            avoid_runtime_error(window, f'Erro ao iniciar o navegador! (tentativa {attempt}/10)\n', text_color='red')
            if attempt >= 10:
                exc_type, exc_value, exc_tb = sys.exc_info()
                tb = traceback.TracebackException(exc_type, exc_value, exc_tb)
                tb_txt = "".join(tb.format_exception_only())
                print(tb_txt)
                create_crash_file(find_data_file, tb_txt)
                break
            else:
                continue
        except WebDriverException:
            avoid_runtime_error(window, f'Erro ao iniciar o navegador!\n', text_color='red')
            exc_type, exc_value, exc_tb = sys.exc_info()
            tb = traceback.TracebackException(exc_type, exc_value, exc_tb)
            tb_txt = "".join(tb.format_exception_only())
            print(tb_txt)
            create_crash_file(find_data_file, tb_txt)
            break
        else:
            if getattr(thread, 'close_driver', False):
                driver.quit()
                sys.exit()
            avoid_runtime_error(window, 'OK!\n', 'green', write_event=True, key='driver_started', value=(driver, wait))
            break

def open_linkedin(window: sg.Window, driver: WebDriver, wait: WebDriverWait):
    # open Linkedin
    avoid_runtime_error(window, 'Acessando o site do Linkedin... ')
    while True:
        try:
            driver.get('https://www.linkedin.com/')
            break
        except WebDriverException:
            pass
    avoid_runtime_error(window, 'OK!\n', 'green', write_event=True, key='linkedin_is_open', value='')

def check_login_page(window: sg.Window, driver: WebDriver, wait: WebDriverWait):
    # click on sign in or reload page
    while True:
        sleep(5)
        try:
            button_login: WebElement = driver.find_element(By.XPATH, '//button[@class="authwall-join-form__form-toggle--bottom form-toggle"]')
            avoid_runtime_error(window, 'Clicando em "Entrar"... ')
            button_login.click()
            avoid_runtime_error(window, 'OK!\n', 'green')
            break
        except NoSuchElementException:
            sleep(5)
            try:
                driver.find_element(By.XPATH, '//a[contains(text(),"Entrar")]').click()
                break
            except NoSuchElementException:
                pass
            avoid_runtime_error(window, 'Recarregando a página... ')
            driver.execute_script("location.reload()")
            avoid_runtime_error(window, 'OK!\n', 'green')
    avoid_runtime_error(window, '', write_event=True, key='login_page_is_open', value='')

def login(window: sg.Window, driver: WebDriver, wait: WebDriverWait, username: str, password: str):
    avoid_runtime_error(window, 'Logando no site... ')
    try:
        username_field: WebElement = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//input[@autocomplete="webauthn"]')))
    except TimeoutException:
        username_field: WebElement = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//input[@autocomplete="username"]')))
        driver.execute_script("window.scrollTo(0, -document.body.scrollHeight)")
    username_field.send_keys(username)
    sleep(1)
    password_field: WebElement = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//input[@autocomplete="current-password"]')))
    password_field.send_keys(password)
    sleep(1)
    driver.find_element(By.XPATH, '//button[contains(text(),"Entrar")]').click()
    avoid_runtime_error(window, 'OK!\n', 'green', write_event=True, key='login_complete', value='')

def start_bot2(window: sg.Window, driver: WebDriver, wait: WebDriverWait, key_message: str = '', text_to_write: str = '', page_scrolls: int = 0, wait_time: int = 0, debug: bool = False, find_data_file: Callable = None):
    first = True
    is_other_tab = False
    if debug:
        # with open(find_data_file('replies.txt'), 'wt', encoding='utf-8') as file:
        #     pass
        with open(find_data_file('errors.txt'), 'wt', encoding='utf-8') as file:
            pass
    while True:
        try:
            if first:
                thread = threading.current_thread()
                # action_chains = ActionChains(driver)
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
                    filter_button: WebElement = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//li[@class="org-menu__item" and @data-test-org-menu__item="horizontal"][2]/a')))
                    
                    # stop bot
                    if not getattr(thread, 'do_run', True):
                        raise BotStopped
                    
                    # if filter_button.get_attribute('aria-checked') == 'false':
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
                
                sleep(5)
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
            comments: list[WebElement] = wait.until(expected_conditions.presence_of_all_elements_located((By.XPATH, '//div[@class="scaffold-finite-scroll__content"]/div/div/article/div/div[2]')))

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
                            sleep(12)

                            # stop bot
                            if not getattr(thread, 'do_run', True):
                                raise BotStopped

                            avoid_runtime_error(window, 'OK!\n', 'green')
                            data_id = driver.current_url.split('%')[-2].removeprefix('2C')
                            avoid_runtime_error(window, 'Identificando se o comentário já foi respondido... ')
                            replies: list[WebElement] = driver.find_elements(By.XPATH, f'//article[contains(@data-id, "{data_id}")]/div[6]/div[4]/div/article/div[3]/div/div/span/div/span')
                            replies_text = [reply.get_attribute('innerText') for reply in replies]
                            reply_found = any(map(lambda reply: check_text(
                                ''.join([t for t in text_to_write if t not in ' \n']),
                                ''.join([t for t in unicodedata.normalize("NFKC", reply) \
                                         if t not in ' \n']), 80), replies_text))

                            # if debug:
                            #     with open(find_data_file('replies.txt'), 'at', encoding='utf-8') as file:
                            #         file.write(f'url: {driver.current_url}\n')
                            #         file.write(f'id: {data_id}\n')
                            #         file.write(f'reply_found: {reply_found}\n')
                            #         file.write(f'text to write: {text_to_write}\n')
                            #         for k, text in enumerate(replies_text, 1):
                            #             file.write(f'{k}° reply: {text}\n')
                            #         file.write('\n')

                            # stop bot
                            if not getattr(thread, 'do_run', True):
                                raise BotStopped

                            if not reply_found:
                                avoid_runtime_error(window, 'Comentário não foi respondido ainda!\n', 'red')
                                avoid_runtime_error(window, 'Respondendo comentário... ')

                                # stop bot
                                if not getattr(thread, 'do_run', True):
                                    raise BotStopped

                                sleep(1)
                                texts = text_to_write.splitlines()
                                for k in range(len(texts)):
                                    fields = driver.find_elements(By.XPATH, '//div[contains(@data-placeholder, "Responder em nome de")]/p')
                                    sleep(0.1)
                                    driver.execute_script(f"arguments[0].innerHTML = '{texts[k]}'", fields[k])
                                    sleep(0.1)
                                    fields[k].send_keys(Keys.END)
                                    sleep(0.1)
                                    fields[k].send_keys(Keys.ARROW_DOWN * 10)
                                    sleep(0.1)
                                    fields[k].send_keys('\n.' if k + 1 < len(texts) else '')
                                
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
                            is_other_tab = False
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
                if is_other_tab:
                    driver.close()
                    driver.switch_to.window(initial_tab)
                avoid_runtime_error(window, 'Bot encerrado!\n', 'red', write_event=True, key='bot_stopped', value='')
            else:
                exc_type, exc_value, exc_tb = sys.exc_info()
                tb = traceback.TracebackException(exc_type, exc_value, exc_tb)
                tb_txt = "".join(tb.format_exception_only())
                print(tb_txt)
                if debug:
                    with open(find_data_file('errors.txt'), 'at', encoding='utf-8') as file:
                        file.write(tb_txt + '\n')
                if is_other_tab:
                    driver.close()
                    driver.switch_to.window(initial_tab)
                avoid_runtime_error(window, 'Erro encontrado! Bot encerrado!\n', 'red', write_event=True, key='bot_stopped', value='')
            break
        else:
            first = False
