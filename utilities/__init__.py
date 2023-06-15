from utilities.driver_settings import start_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support import expected_conditions
from time import sleep
import PySimpleGUI as sg
import threading
import sys

def start_driver2(window: sg.Window):
    thread = threading.current_thread()
    window['-OUT-'].update('Iniciando o navegador... ', append=True)
    driver, wait = start_driver()
    if getattr(thread, 'close_driver', False):
        driver.quit()
        sys.exit()
    window['-OUT-'].update('OK!\n', text_color_for_value='green', append=True)
    window.write_event_value('driver_started', (driver, wait))

def open_linkedin(window: sg.Window, driver: WebDriver, wait: WebDriverWait):
    # open Linkedin
    window['-OUT-'].update('Acessando o site do Linkedin... ', append=True)
    driver.get('https://www.linkedin.com/')
    window['-OUT-'].update('OK!\n', text_color_for_value='green', append=True)
    window.write_event_value('linkedin_is_open', '')

def click_on_sign_in(window: sg.Window, driver: WebDriver, wait: WebDriverWait):
    # click on sign in or reload page
    while True:
        sleep(1)
        try:
            button_login: WebElement = driver.find_element(By.XPATH, '//button[@class="authwall-join-form__form-toggle--bottom form-toggle"]')
            window['-OUT-'].update('Clicando em "Entrar".\n', append=True)
            button_login.click()
            break
        except NoSuchElementException:
            try:
                driver.find_element(By.XPATH, '//input[@autocomplete="username"]')
                break
            except NoSuchElementException:
                pass
            window['-OUT-'].update('Recarregando a página.\n', append=True)
            driver.execute_script("location.reload()")
    window.write_event_value('sign_in_is_open', '')

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
            try:
                text = post.find_element(By.XPATH, './div/div[4]/div/div/div[5]/ul/li/button/span').text
            except NoSuchElementException:
                text = '0 comentários'
            comments.append(text)
        
        # make values for combo element
        values_combo = [t[:30] + ' - ' + r[:-2] + ' - ' + c for t, r, c in zip(texts, last_releases, comments)]

        window['-OUT-'].update('OK!\n', text_color_for_value='green', append=True)
        window.write_event_value('number_of_posts_found', values_combo)
    except TimeoutException:
        window['-OUT-'].update('ERRO! Postagens não encontradas.\n', text_color_for_value='red', append=True)
        window.write_event_value('number_of_posts_not_found', '')

def start_bot(window: sg.Window, driver: WebDriver, wait: WebDriverWait, key_message: str = '', link_to_share: str = '', post_selected: int = 0, wait_time: int = 0):
    thread = threading.current_thread()
    stop = False
    while not stop:
        driver.execute_script("window.scrollTo(0, -document.body.scrollHeight)")
        sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        # posts
        window['-OUT-'].update('Selecionando postagem... ', append=True)
        # //div[@class="scaffold-finite-scroll__content"]/div
        posts: list[WebElement] = wait.until(expected_conditions.presence_of_all_elements_located((By.XPATH, '//div[@class="scaffold-finite-scroll__content"]/div')))
        # y = 0
        while (x := 0) >= 0:
            try:
                post = posts[post_selected]
                # ./div/div[4]/div/div/div[5]/ul/li/button
                post.find_element(By.XPATH, './div/div[4]/div/div/div[5]/ul/li/button').click()
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                break
            except IndexError:
                window['-OUT-'].update('Erro! Postagem não encontrada.\n', text_color_for_value='red', append=True)
                stop = True
                break
            except NoSuchElementException:
                window['-OUT-'].update('Erro! Postagem não tem comentários.\n', text_color_for_value='red', append=True)
                stop = True
                break
            except ElementClickInterceptedException:
                x += 10
                driver.execute_script(f"window.scrollTo(0, {x})")
                # print('Recarregando a página...')
                # driver.execute_script("location.reload()")
                # sleep(5)
                # continue
        if stop:
            window.write_event_value('bot_stopped', '')
            continue
        window['-OUT-'].update(f'{post_selected + 1}° postagem selecionada.\n', text_color_for_value='green', append=True)
        sleep(2)

        # click on the load more messages button
        window['-OUT-'].update('Carregando mais mensagens... ', append=True)
        # y = 0
        while (y := 0) >= 0:
            try:
                # ./div/div[4]/div/div/div[5]/div[3]/div[3]/div[2]/button
                post.find_element(By.XPATH, './div/div[4]/div/div/div[5]/div[3]/div[3]/div[2]/button').click()
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                break
            except NoSuchElementException:
                break
            except ElementClickInterceptedException:
                y += 50
                driver.execute_script(f"window.scrollTo(0, {y})")
        window['-OUT-'].update(f'OK!\n', text_color_for_value='green', append=True)
        sleep(2)

        # main bot
        window['-OUT-'].update(f'Identificando comentários que possuem a palavra-chave "{key_message}"... ', append=True)

        # ./div/div[4]/div/div/div[5]/div[3]/div[3]/div/article[1 ou 2]/div[3]/div/div/span/div/span
        comments = post.find_elements(By.XPATH, './div/div[4]/div/div/div[5]/div[3]/div[3]/div/article/div[3]/div/div/span/div/span')
        comments_text: list[str] = list(map(lambda w: w.text, comments))

        length = len(list(filter(lambda t: t.lower() == key_message.lower(), comments_text)))
        window['-OUT-'].update(f'{length} comentário{"s" if length > 1 else ""}.\n', text_color_for_value='green', append=True)

        # ./div/div[4]/div/div/div[5]/div[3]/div[3]/div/article[1 ou 2]/div[4]/div[2]/div/div[3]/button
        response_buttons = post.find_elements(By.XPATH, './div/div[4]/div/div/div[5]/div[3]/div[3]/div/article/div[4]/div[2]/div/div[3]/button')
        for k, response_button, text in zip(range(1, len(comments_text) + 1), response_buttons, comments_text):
            # click on the load previous messages button
            # y = 0
            while (z := 0) >= 0:
                try:
                    # ./div/div[4]/div/div/div[5]/div[3]/div[3]/div/article/div[4]/div[4]/div/button
                    post.find_element(By.XPATH, f'./div/div[4]/div/div/div[5]/div[3]/div[3]/div/article[{k}]/div[4]/div[4]/div/button').click()
                    break
                except NoSuchElementException:
                    break
                except ElementClickInterceptedException:
                    z += 10
                    driver.execute_script(f"window.scrollTo(0, {z})") 

            # detect if link has been shared
            # ./div/div[4]/div/div/div[5]/div[3]/div[3]/div/article[1 ou 2]/div[4]/div[4]/div[1]/article[3 ou 4]/div[3]/div/div/span/div/span
            replies = post.find_elements(By.XPATH, f'./div/div[4]/div/div/div[5]/div[3]/div[3]/div/article[{k}]/div[4]/div[4]/div[1]/article/div[3]/div/div/span/div/span')
            href_texts = []
            if replies:
                for reply in replies:
                    try:
                        href_text = reply.find_element(By.XPATH, './a').text
                        href_texts.append(href_text)
                    except NoSuchElementException:
                        pass
            
            # detect key message in comments
            if text.lower() == key_message.lower() and link_to_share not in href_texts:
                response_button.click()
                window['-OUT-'].update('Compartilhando link... ', append=True)
                sleep(2)
                # ./div/div[4]/div/div/div[5]/div[3]/div[3]/div/article[1 ou 2]/div[4]/div[4]/div[3 ou 4]/div[2]/form/div/div/div/div/div/div/div/div/p
                field = post.find_element(By.XPATH, f'./div/div[4]/div/div/div[5]/div[3]/div[3]/div/article[{k}]/div[4]/div[4]/div[{len(replies) + 1}]/div[2]/form/div/div/div/div/div/div/div/div/p')
                field.send_keys(link_to_share)
                sleep(2)
                # ./div/div[4]/div/div/div[5]/div[3]/div[3]/div/article[1 ou 2]/div[4]/div[4]/div[3 ou 4]/div[2]/form/div[2]/button
                button = post.find_element(By.XPATH, f'./div/div[4]/div/div/div[5]/div[3]/div[3]/div/article[{k}]/div[4]/div[4]/div[{len(replies) + 1}]/div[2]/form/div[2]/button')
                button.click()
                window['-OUT-'].update('OK!\n', text_color_for_value='green', append=True)
                sleep(2)
            k += 1
        window['-OUT-'].update(f'Esperando {wait_time / 60} minuto{"s" if wait_time / 60 > 1 else ""}... ', append=True)
        for _ in range(wait_time):
            if not getattr(thread, 'do_run', True):
                stop = True
                break
            else:
                sleep(1)
        if stop:
            window['-OUT-'].update('Operação cancelada!\n', text_color_for_value='red', append=True)
            window.write_event_value('bot_stopped', '')
            continue
        else:
            window['-OUT-'].update('OK!\n', text_color_for_value='green', append=True)
            window['-OUT-'].update('Recarregando a página... ', append=True)
            driver.execute_script("location.reload()")
            sleep(5)
            window['-OUT-'].update('OK!\n', text_color_for_value='green', append=True)
