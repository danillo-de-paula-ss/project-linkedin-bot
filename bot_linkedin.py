from utilities import *
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
import PySimpleGUI as sg
import threading
import argparse
import os
import json
import pickle
from cryptography.fernet import Fernet

class Program:
    def __init__(self, dev_mode: bool = False) -> None:
        sg.theme('Reddit')
        self.dev_mode = dev_mode
        self.key = b'C5S5cpuAyO_XDOHX2Rr5MnHu64Ne6Bzg_pKsk1l9zag='
        my_username = 'nerdpesquisando@gmail.com'
        my_password = 'sagavazas1234'
        key_message = 'Eu quero'
        link_to_share = 'https://www.youtube.com/'
        post_selected = 0
        wait_time = 10
        captcha_time = 60
    
    def make_win1(self) -> sg.Window:
        login_frame = [
            [sg.Text('Usuário:', size=(8, 0), text_color='gray', key='-USERNAME-TEXT-'), sg.Input(expand_x=True, disabled=True, key='-USERNAME-')],
            [sg.Text('Senha:', size=(8, 0), text_color='gray', key='-PASSWORD-TEXT-'), sg.Input(expand_x=True, disabled=True, key='-PASSWORD-', password_char='*')],
            [sg.Text('', text_color='red', key='-NOTIFICATION-')],
        ]
        layout = [
            [sg.Text('Como deve ser feito o processo de login?'), sg.Radio('manual', 'login', key='-LOGIN-PROCESSa-', enable_events=True, default=True), sg.Radio('automático', 'login', key='-LOGIN-PROCESSb-', enable_events=True, default=False)],
            [sg.Frame('Login automático', login_frame, expand_x=True, key='-LOGIN-FRAME-')],
            [sg.Button('Confirmar', key='-CONFIRM-', expand_x=True)],
        ]
        return sg.Window('Configurações inicias', layout, size=(500, 180), resizable=False, finalize=True)

    def make_win2(self) -> sg.Window:
        column1 = [
            [sg.Text('Messagem chave:')],
            [sg.Text('Texto para o bot escrever:')],
            [sg.Button('Importar texto', key='-IMPORT-TEXT-', size=(18, 0))],
            [sg.Button('Limpar texto', key='-CLEAN-ALL-', size=(18, 0))],
        ]
        column2 = [
            [sg.Input(key='-KEY-MESSAGE-', expand_x=True)],
            [sg.Multiline(key='-TEXT-TO-WRITE-', size=(0, 10), expand_x=True, horizontal_scroll=True)]
        ]
        left_frame = [
            [sg.Column(column1, expand_x=True, vertical_alignment='top'), sg.Column(column2, expand_x=True)],
            [sg.Button('Obter postagens da página atual', expand_x=True, disabled=True, key='-BUTTON-GET-POST-')],
            [sg.Text('Selecionar postagem:', size=(16, 0)), sg.Combo((), expand_x=True, readonly=True, key='-COMBO-POSTS-')],
            [sg.Text('Tempo de espera em minutos para atualizar a página:', size=(40, 0)), sg.Spin(list(range(1, 60)), 1, readonly=True, size=(10, 0), key='-SPIN-WAIT-')],
            [sg.Button('Iniciar o Bot', key='-START-BOT-', expand_x=True, disabled=True), sg.Button('Parar o Bot', key='-STOP-BOT-', expand_x=True, disabled=True)]
        ]
        # left_frame = [
        #     [sg.Text('Como deve ser feito o processo de login?'), sg.Radio('manual', 'login', key='-LOGIN-PROCESSa-', enable_events=True, default=True), sg.Radio('automático', 'login', key='-LOGIN-PROCESSb-', enable_events=True, default=False, disabled=not self.dev_mode)],
        #     # [sg.Frame('Login automático', login_frame, expand_x=True, key='-LOGIN-FRAME-')],
        #     [sg.Frame('Configurações do Bot', settings_frame, expand_x=True, key='-SETTINGS-FRAME-')]
        # ]
        right_frame = [
            [sg.Multiline(expand_x=True, expand_y=True, auto_refresh=True, autoscroll=True, write_only=True, disabled=True, key='-OUT-', font=('', 14, 'bold'))]
        ]
        layout = [
            [sg.Push('black'), sg.Text('Bot Linkedin para respostas automáticas'), sg.Push('black')],
            [sg.Frame('Configurações do Bot', left_frame, size=(550, 600), expand_y=True, vertical_alignment='top', key='-FRAME1-'), sg.Frame('Log de atividades', right_frame, size=(550, 600), expand_y=True, key='-FRAME2-')]
        ]
        return sg.Window('Bot Linkedin', layout, size=(1200, 600), resizable=True, element_justification='center', finalize=True)

    def main(self, nobrowser) -> None:
        data_path = os.path.join(os.path.dirname(__file__), 'data.pkl')
        if not os.path.exists(data_path):
            initial_window, main_window = self.make_win1(), None
        else:
            with open(data_path, 'rb') as file:
                data: dict = pickle.load(file)
                username, password_encrypted = data.values()
                password = Fernet(self.key).decrypt(password_encrypted).decode()
            initial_window, main_window = None, self.make_win2()
            automatic_login = True

        # start browser
        thread_driver = threading.Thread(target=start_driver2, args=(main_window,), daemon=True)
        if not nobrowser and main_window is not None:
            thread_driver.start()
            program_closed_fast = True
        else:
            program_closed_fast = False
        
        # settings
        driver, wait = None, None
        login_frame_keys = ['-USERNAME-', '-PASSWORD-']
        login_frame_text_keys = ['-USERNAME-TEXT-', '-PASSWORD-TEXT-']
        posts_list = []

        # main program
        while True:
            window, event, values = sg.read_all_windows()
            if event == sg.WIN_CLOSED:
                    if program_closed_fast and main_window is not None:
                        main_window.close()
                        thread_driver.close_driver = True
                        thread_driver.join()
                    break
            # initial window
            elif window == initial_window:
                # execution process type system
                if event == '-LOGIN-PROCESSa-':
                    for key in login_frame_keys:
                        initial_window[key].update(disabled=True)
                    for key in login_frame_text_keys:
                        initial_window[key].update(text_color='gray')
                    initial_window['-NOTIFICATION-'].update('')
                elif event == '-LOGIN-PROCESSb-':
                    for key in login_frame_keys:
                        initial_window[key].update(disabled=False)
                    for key in login_frame_text_keys:
                        initial_window[key].update(text_color='black')
                elif event == '-CONFIRM-':
                    if values['-LOGIN-PROCESSa-']:
                        main_window = self.make_win2()
                        initial_window.close()
                        automatic_login = False
                        thread_driver = threading.Thread(target=start_driver2,
                                                         args=(main_window,),
                                                         daemon=True)
                        thread_driver.start()
                        program_closed_fast = True
                    else:
                        username: str = values['-USERNAME-']
                        password: str = values['-PASSWORD-']
                        if username != '' and password != '':
                            password_encrypted = Fernet(self.key).encrypt(password.encode())
                            with open(data_path, 'wb') as file:
                                file.write(pickle.dumps({'username': username,
                                                         'password': password_encrypted.decode()}))
                            main_window = self.make_win2()
                            initial_window.close()
                            automatic_login = True
                            thread_driver = threading.Thread(target=start_driver2,
                                                             args=(main_window,),
                                                             daemon=True)
                            thread_driver.start()
                            program_closed_fast = True
                        else:
                            initial_window['-NOTIFICATION-'].update('Os campos usuário e senha estão vazios.')

            # main window
            elif window == main_window:
                # start browser
                if event == 'driver_started':
                    thread_driver.join()
                    driver: WebDriver = values['driver_started'][0]
                    wait: WebDriverWait = values['driver_started'][1]
                    program_closed_fast = False
                    thread_open_l = threading.Thread(target=open_linkedin,
                                                     args=(main_window, driver, wait),
                                                     daemon=True)
                    thread_open_l.start()
                elif event == 'linkedin_is_open':
                    thread_open_l.join()
                    if automatic_login:
                        main_window.write_event_value('start_login', '')
                    else:
                        main_window['-BUTTON-GET-POST-'].update(disabled=False)
                        main_window['-OUT-'].update('Por favor, faça login e vá para a página de postagens. Em seguida, clique em "Obter postagens da página atual".\n', text_color_for_value='red', append=True)
                
                # automatic login system - not complete
                elif event == 'start_login':
                    thread_clp = threading.Thread(target=check_login_page,
                                                  args=(main_window, driver, wait),
                                                  daemon=True)
                    thread_clp.start()
                elif event == 'login_page_is_open':
                    thread_clp.join()
                    thread_login = threading.Thread(target=login,
                                                    args=(main_window, driver, wait, username, password))
                    thread_login.start()
                elif event == 'login_complete':
                    thread_login.join()
                    main_window['-BUTTON-GET-POST-'].update(disabled=False)
                
                # import text file
                elif event == '-IMPORT-TEXT-':
                    path = sg.popup_get_file('', no_window=True, initial_folder=f'C:\\Users\\{os.getlogin()}\\Documents')
                    if path != '':
                        with open(path, 'rt', encoding='utf-8') as file:
                            main_window['-TEXT-TO-WRITE-'].update(file.read())
                elif event == '-CLEAN-ALL-':
                    main_window['-TEXT-TO-WRITE-'].update('')

                # get posts button system
                elif event == '-BUTTON-GET-POST-':
                    thread_get_post = threading.Thread(target=get_posts,
                                                       args=(main_window, driver, wait),
                                                       daemon=True)
                    thread_get_post.start()
                    main_window['-BUTTON-GET-POST-'].update(disabled=True)
                elif event == 'number_of_posts_found':
                    thread_get_post.join()
                    posts_list = values['number_of_posts_found']
                    main_window['-COMBO-POSTS-'].update(values=values['number_of_posts_found'], set_to_index=0)
                    main_window['-BUTTON-GET-POST-'].update(disabled=False)
                    main_window['-START-BOT-'].update(disabled=False)
                elif event == 'number_of_posts_not_found':
                    thread_get_post.join()
                    main_window['-BUTTON-GET-POST-'].update(disabled=False)
                
                # bot system
                elif event == '-START-BOT-':
                    thread_bot = threading.Thread(target=start_bot,
                                                  args=(main_window,
                                                        driver,
                                                        wait,
                                                        values['-KEY-MESSAGE-'],
                                                        values['-TEXT-TO-WRITE-'],
                                                        posts_list.index(values['-COMBO-POSTS-']),
                                                        int(values['-SPIN-WAIT-'] * 60)),
                                                        daemon=True)
                    thread_bot.start()
                    main_window['-START-BOT-'].update(disabled=True)
                    main_window['-STOP-BOT-'].update(disabled=False)
                elif event == '-STOP-BOT-':
                    thread_bot.do_run = False
                elif event == 'bot_stopped':
                    thread_bot.join()
                    main_window['-START-BOT-'].update(disabled=False)
                    main_window['-STOP-BOT-'].update(disabled=True)
        
        if driver is not None:
            main_window.close()
            driver.quit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-nb', '--nobrowser', action='store_true', help='Does not open the browser')
    parser.add_argument('-d', '--dev', action='store_true', help='Enable developer mode')
    args = parser.parse_args()
    program = Program(args.dev)
    program.main(args.nobrowser)
