from driver_settings import start_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
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

def start_main_program(window: sg.Window, driver: WebDriver, wait: WebDriverWait):
    # //div[@class="scaffold-finite-scroll__content"]/div
    # ./div/div[4]/div/div/div[5]/ul/li/button
    # ./div/div[4]/div/div/div[5]/div[3]/div[3]/div/article[1 ou 2]/div[3]/div/div/span/div/span
    # ./div/div[4]/div/div/div[5]/div[3]/div[3]/div/article[1 ou 2]/div[4]/div[2]/div/div[3]/button
    # ./div/div[4]/div/div/div[5]/div[3]/div[3]/div/article[1 ou 2]/div[4]/div[4]/div[3 ou 4]/div[2]/form/div/div/div/div/div/div/div/div/p
    # ./div/div[4]/div/div/div[5]/div[3]/div[3]/div/article[1 ou 2]/div[4]/div[4]/div[3 ou 4]/div[2]/form/div[2]/button
    # ./div/div[4]/div/div/div[5]/div[3]/div[3]/div/article[1 ou 2]/div[4]/div[4]/div[1]/article[3 ou 4]/div[3]/div/div/span/div/span
    
    pass

class Program:
    def __init__(self) -> None:
        sg.theme('Reddit')
        self.window = self.make_win()
        self.driver: WebDriver = None
        self.wait: WebDriverWait = None
        my_username = 'nerdpesquisando@gmail.com'
        my_password = 'sagavazas1234'
        key_message = 'Eu quero'
        link_to_share = 'https://www.youtube.com/'
        post_selected = 0
        wait_time = 10
        captcha_time = 60
    
    def make_win(self):
        login_frame = [
            [sg.Text('Usuário:', size=(8, 0), text_color='gray', key='-USER-TEXT-'), sg.Input(expand_x=True, disabled=True, key='-USER-')],
            [sg.Text('Senha:', size=(8, 0), text_color='gray', key='-PASSWORD-TEXT-'), sg.Input(expand_x=True, disabled=True, key='-PASSWORD-', password_char='*')],
            [sg.Text('Deseja esperar 1 minuto para resolver o CAPTCHA?', text_color='gray', key='-CAPTCHA-TEXT-'), sg.Radio('Sim', 'captcha', False, disabled=True, key='-RADIO-CAPTCHAa-'), sg.Radio('Não', 'captcha', True, disabled=True, key='-RADIO-CAPTCHAb-')],
            [sg.Button('Logar', size=(6, 0), key='-LOGIN-', disabled=True), sg.Text('', text_color='gray', key='-NOTIFICATION-TEXT-')],
        ]
        left_frame = [
            [sg.Text('Como deve ser feito o processo de login?'), sg.Radio('manual', 'login', key='-LOGIN-PROCESSa-', enable_events=True, default=True), sg.Radio('automático', 'login', key='-LOGIN-PROCESSb-', enable_events=True, default=False)],
            [sg.Frame('Login automático', login_frame, expand_x=True, key='-LOGIN-FRAME-')],
        ]
        right_frame = [
            [sg.Multiline(expand_x=True, expand_y=True, auto_refresh=True, autoscroll=True, write_only = True, disabled=True, key='-OUT-', font=('', 14, 'bold'))]
        ]
        layout = [
            [sg.Push('black'), sg.Text('Bot Linkedin para compartilhamento de links'), sg.Push('black')],
            [sg.Frame('', left_frame, size=(550, 600), expand_y=True, vertical_alignment='top', key='-FRAME1-'), sg.Frame('', right_frame, size=(550, 600), expand_y=True, key='-FRAME2-')]
        ]
        return sg.Window('Bot Linkedin', layout, size=(1200, 600), resizable=True, element_justification='center', finalize=True)

    def main(self):
        # self.window.bind('<Configure>', "resize_window")
        thread1 = threading.Thread(target=start_driver2, args=(self.window,))
        thread1.start()
        program_closed_fast = True
        login_button_disabled = True
        login_frame_keys = ['-USER-', '-PASSWORD-', '-RADIO-CAPTCHAa-', '-RADIO-CAPTCHAb-', '-LOGIN-']
        login_frame_text_keys = ['-USER-TEXT-', '-PASSWORD-TEXT-', '-CAPTCHA-TEXT-', '-NOTIFICATION-TEXT-']
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED:
                if program_closed_fast:
                    self.window.close()
                    thread1.close_driver = True
                    thread1.join()
                break
            # elif event == 'resize_window':
            #     print(self.window['-FRAME1-'].get_size())
            elif event == 'driver_started':
                thread1.join()
                self.driver, self.wait = values['driver_started']
                program_closed_fast = False
                thread2 = threading.Thread(target=open_linkedin, args=(self.window, self.driver, self.wait), daemon=True)
                thread2.start()
            elif event == 'linkedin_is_open':
                thread2.join()
                thread3 = threading.Thread(target=click_on_sign_in, args=(self.window, self.driver, self.wait), daemon=True)
                thread3.start()
            elif event == 'sign_in_is_open':
                thread3.join()
                login_button_disabled = False
                if values['-LOGIN-PROCESSb-']:
                    self.window['-LOGIN-'].update(disabled=login_button_disabled)
            elif event == '-LOGIN-PROCESSa-':
                for key in login_frame_keys:
                    self.window[key].update(disabled=True)
                for key in login_frame_text_keys:
                    self.window[key].update(text_color='gray')
            elif event == '-LOGIN-PROCESSb-':
                for key in login_frame_keys[:-1]:
                    self.window[key].update(disabled=False)
                self.window['-LOGIN-'].update(disabled=login_button_disabled)
                for key in login_frame_text_keys:
                    self.window[key].update(text_color='black')
        
        if self.driver is not None:
            self.window.close()
            self.driver.quit()

if __name__ == '__main__':
    program = Program()
    program.main()
