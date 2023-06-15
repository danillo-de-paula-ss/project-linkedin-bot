from utilities import *
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import PySimpleGUI as sg
import threading

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
    
    def make_win(self) -> sg.Window:
        login_frame = [
            [sg.Text('Usuário:', size=(8, 0), text_color='gray', key='-USER-TEXT-'), sg.Input(expand_x=True, disabled=True, key='-USER-')],
            [sg.Text('Senha:', size=(8, 0), text_color='gray', key='-PASSWORD-TEXT-'), sg.Input(expand_x=True, disabled=True, key='-PASSWORD-', password_char='*')],
            [sg.Text('Deseja esperar 1 minuto para resolver o CAPTCHA?', text_color='gray', key='-CAPTCHA-TEXT-'), sg.Radio('Sim', 'captcha', False, disabled=True, key='-RADIO-CAPTCHAa-'), sg.Radio('Não', 'captcha', True, disabled=True, key='-RADIO-CAPTCHAb-')],
            [sg.Button('Logar', size=(6, 0), key='-LOGIN-', disabled=True), sg.Text('', text_color='gray', key='-NOTIFICATION-TEXT-')],
        ]
        settings_frame = [
            [sg.Text('Messagem chave:', size=(20, 0)), sg.Input(expand_x=True, key='-KEY-MESSAGE-')],
            [sg.Text('Link para compartilhamento:', size=(20, 0)), sg.Input(expand_x=True, key='-LINK-TO-SHARE-')],
            [sg.Button('Obter postagens da página atual', expand_x=True, disabled=True, key='-BUTTON-GET-POST-')],
            [sg.Text('Selecionar postagem:', size=(20, 0)), sg.Combo((), expand_x=True, readonly=True, key='-COMBO-POSTS-')],
            [sg.Text('Tempo de espera em minutos para atualizar a página:', size=(40, 0)), sg.Spin(list(range(1, 60)), 1, readonly=True, size=(10, 0), key='-SPIN-WAIT-')],
            [sg.Button('Iniciar o Bot', key='-START-BOT-', expand_x=True, disabled=True), sg.Button('Parar o Bot', key='-STOP-BOT-', expand_x=True, disabled=True)]
        ]
        left_frame = [
            [sg.Text('Como deve ser feito o processo de login?'), sg.Radio('manual', 'login', key='-LOGIN-PROCESSa-', enable_events=True, default=True), sg.Radio('automático', 'login', key='-LOGIN-PROCESSb-', enable_events=True, default=False)],
            [sg.Frame('Login automático', login_frame, expand_x=True, key='-LOGIN-FRAME-')],
            [sg.Frame('Configurações do Bot', settings_frame, expand_x=True, key='-SETTINGS-FRAME-')]
        ]
        right_frame = [
            [sg.Multiline(expand_x=True, expand_y=True, auto_refresh=True, autoscroll=True, write_only = True, disabled=True, key='-OUT-', font=('', 14, 'bold'))]
        ]
        layout = [
            [sg.Push('black'), sg.Text('Bot Linkedin para compartilhamento de links'), sg.Push('black')],
            [sg.Frame('', left_frame, size=(550, 600), expand_y=True, vertical_alignment='top', key='-FRAME1-'), sg.Frame('', right_frame, size=(550, 600), expand_y=True, key='-FRAME2-')]
        ]
        return sg.Window('Bot Linkedin', layout, size=(1200, 600), resizable=True, element_justification='center', finalize=True)

    def main(self) -> None:
        # self.window.bind('<Configure>', "resize_window")
        thread_driver = threading.Thread(target=start_driver2, args=(self.window,), daemon=True)
        thread_driver.start()
        program_closed_fast = True
        login_button_disabled = True
        login_frame_keys = ['-USER-', '-PASSWORD-', '-RADIO-CAPTCHAa-', '-RADIO-CAPTCHAb-', '-LOGIN-']
        login_frame_text_keys = ['-USER-TEXT-', '-PASSWORD-TEXT-', '-CAPTCHA-TEXT-', '-NOTIFICATION-TEXT-']
        posts_list = []
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED:
                if program_closed_fast:
                    self.window.close()
                    thread_driver.close_driver = True
                    thread_driver.join()
                break

            # start browser
            elif event == 'driver_started':
                thread_driver.join()
                self.driver, self.wait = values['driver_started']
                program_closed_fast = False
                thread_open_l = threading.Thread(target=open_linkedin, args=(self.window, self.driver, self.wait), daemon=True)
                thread_open_l.start()
            elif event == 'linkedin_is_open':
                thread_open_l.join()
                login_button_disabled = False
                self.window['-BUTTON-GET-POST-'].update(disabled=False)
                if values['-LOGIN-PROCESSb-']:
                    self.window['-LOGIN-'].update(disabled=login_button_disabled)
                    self.window['-OUT-'].update('Por favor, insira os dados no quadro "Login automático" e clique em "Logar".\n', text_color_for_value='red', append=True)
                elif values['-LOGIN-PROCESSa-']:
                    self.window['-OUT-'].update('Por favor, faça login e vá para a página de postagens. Em seguida, clique em "Obter postagens da página atual".\n', text_color_for_value='red', append=True)

            # automatic login system
            elif event == '-LOGIN-':
                thread3 = threading.Thread(target=click_on_sign_in, args=(self.window, self.driver, self.wait), daemon=True)
                thread3.start()
            elif event == 'sign_in_is_open':
                thread3.join()
            
            # execution process type system
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
            
            # get posts button system
            elif event == '-BUTTON-GET-POST-':
                thread_get_post = threading.Thread(target=get_posts, args=(self.window, self.driver, self.wait), daemon=True)
                thread_get_post.start()
                self.window['-BUTTON-GET-POST-'].update(disabled=True)
            elif event == 'number_of_posts_found':
                thread_get_post.join()
                posts_list = values['number_of_posts_found']
                self.window['-COMBO-POSTS-'].update(values=values['number_of_posts_found'], set_to_index=0)
                self.window['-BUTTON-GET-POST-'].update(disabled=False)
                self.window['-START-BOT-'].update(disabled=False)
            elif event == 'number_of_posts_not_found':
                self.window['-BUTTON-GET-POST-'].update(disabled=False)
            
            # bot system
            elif event == '-START-BOT-':
                thread_bot = threading.Thread(target=start_bot, args=(self.window, self.driver, self.wait, values['-KEY-MESSAGE-'], values['-LINK-TO-SHARE-'], posts_list.index(values['-COMBO-POSTS-']), int(values['-SPIN-WAIT-'] * 60)), daemon=True)
                thread_bot.start()
                self.window['-START-BOT-'].update(disabled=True)
                self.window['-STOP-BOT-'].update(disabled=False)
            elif event == '-STOP-BOT-':
                thread_bot.do_run = False
            elif event == 'bot_stopped':
                thread_bot.join()
                self.window['-START-BOT-'].update(disabled=False)
                self.window['-STOP-BOT-'].update(disabled=True)
        
        if self.driver is not None:
            self.window.close()
            self.driver.quit()

if __name__ == '__main__':
    program = Program()
    program.main()
