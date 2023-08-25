from utilities import *
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
import PySimpleGUI as sg
import threading
import argparse
import os
import pickle
from cryptography.fernet import Fernet

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

class Program:
    def __init__(self, dev_mode:bool = False) -> None:
        sg.theme('Reddit')
        self.dev_mode = dev_mode
        self.key = b'C5S5cpuAyO_XDOHX2Rr5MnHu64Ne6Bzg_pKsk1l9zag='
    
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
        return sg.Window('Configurações inicias', layout, size=(500, 210), resizable=False, finalize=True)

    def make_win2(self) -> sg.Window:
        column1 = [
            [sg.Text('Messagem chave:')],
            [sg.Text('Texto para o bot escrever:')],
            [sg.Button('Importar texto', key='-IMPORT-TEXT-', disabled=False, size=(18, 0))],
            [sg.Button('Limpar texto', key='-CLEAR-ALL-', disabled=False, size=(18, 0))],
        ]
        column2 = [
            [sg.Input(key='-KEY-MESSAGE-', expand_x=True)],
            [sg.Multiline(key='-TEXT-TO-WRITE-', size=(0, 10), expand_x=True, horizontal_scroll=True)]
        ]
        left_frame = [
            [sg.Column(column1, expand_x=True, vertical_alignment='top'), sg.Column(column2, expand_x=True)],
            [sg.HorizontalSeparator('blue')],
            [sg.Text('Quantidade de rolagens da página:', size=(40, 0)), sg.Spin(list(range(0, 10)), 0, readonly=True, size=(10, 0), key='-SPIN-SCROLL-')],
            [sg.Text('Tempo de espera em minutos para atualizar a página:', size=(40, 0)), sg.Spin(list(range(1, 60)), 1, readonly=True, size=(10, 0), key='-SPIN-WAIT-')],
            [sg.Button('Iniciar o Bot', key='-START-BOT-', button_color='gray', expand_x=True, auto_size_button=False, disabled=True), sg.Button('Parar o Bot', key='-STOP-BOT-', button_color=('white', 'gray'), expand_x=True, auto_size_button=False, disabled=True)]
        ]
        right_frame = [
            [sg.Multiline(expand_x=True, expand_y=True, auto_refresh=True, autoscroll=True, write_only=True, disabled=True, key='-OUT-', font=('', 14, 'bold'))]
        ]
        layout = [
            [sg.Push('black'), sg.Text('Bot Linkedin para respostas automáticas'), sg.Push('black')],
            [sg.Frame('Configurações do Bot', left_frame, size=(550, 600), expand_y=True, vertical_alignment='top', key='-FRAME1-'), sg.Frame('Log de atividades', right_frame, size=(550, 600), expand_y=True, key='-FRAME2-')]
        ]
        return sg.Window('Bot Linkedin', layout, size=(1200, 600), resizable=True, element_justification='center', finalize=True)

    def main(self, nobrowser, debug) -> None:
        data_path = find_data_file('data.pkl')
        if not os.path.exists(data_path) or self.dev_mode:
            initial_window, main_window = self.make_win1(), None
        else:
            with open(data_path, 'rb') as file:
                data: dict = pickle.load(file)
                username = data['username']
                password_encrypted = data['password']
                password = Fernet(self.key).decrypt(password_encrypted).decode()
            initial_window, main_window = None, self.make_win2()
            main_window.Maximize()
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
                        main_window.Maximize()
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
                            main_window.Maximize()
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
                        main_window['-OUT-'].update('Por favor, faça login e vá para a página de postagens.\n', text_color_for_value='red', append=True)
                        main_window['-START-BOT-'].update(disabled=False, button_color='green')
                
                # automatic login system
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
                    main_window['-OUT-'].update('Por favor, vá para a página de postagens.\n', text_color_for_value='red', append=True)
                    main_window['-START-BOT-'].update(disabled=False, button_color='green')
                
                # import text file
                elif event == '-IMPORT-TEXT-':
                    path = sg.popup_get_file('', no_window=True, initial_folder=f'C:\\Users\\{os.getlogin()}\\Documents')
                    if path != '':
                        thread_import = threading.Thread(target=import_text, args=(main_window, path), daemon=True)
                        thread_import.run()
                elif event == 'import_text_complete':
                    main_window['-TEXT-TO-WRITE-'].update(values['import_text_complete'])
                    # thread_import.join()
                elif event == '-CLEAR-ALL-':
                    main_window['-TEXT-TO-WRITE-'].update('')
                
                # bot system
                elif event == '-START-BOT-':
                    bot_func = start_bot2
                    thread_bot = threading.Thread(target=bot_func,
                                                  args=(main_window,
                                                        driver,
                                                        wait,
                                                        values['-KEY-MESSAGE-'],
                                                        values['-TEXT-TO-WRITE-'],
                                                        int(values['-SPIN-SCROLL-']),
                                                        int(values['-SPIN-WAIT-']),
                                                        debug,
                                                        find_data_file),
                                                        daemon=True)
                    thread_bot.start()
                    main_window['-START-BOT-'].update(disabled=True, button_color='gray')
                    main_window['-STOP-BOT-'].update(disabled=False, button_color=('white', 'red'))
                elif event == '-STOP-BOT-':
                    thread_bot.do_run = False
                    main_window['-STOP-BOT-'].update('Encerrando...', button_color=('black', 'yellow'))
                elif event == 'bot_stopped':
                    thread_bot.join()
                    main_window['-START-BOT-'].update(disabled=False, button_color='green')
                    main_window['-STOP-BOT-'].update('Parar o Bot', disabled=True,
                                                     button_color=('white', 'gray'))
        
        if driver is not None:
            main_window.close()
            driver.quit()
            sys.exit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-nb', '--nobrowser', action='store_true', help='Does not open the browser')
    parser.add_argument('-dv', '--dev', action='store_true', help='Enable developer mode')
    parser.add_argument('-db', '--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()
    program = Program(args.dev)
    program.main(args.nobrowser, args.debug)
