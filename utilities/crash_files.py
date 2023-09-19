from typing import Callable
import datetime
import os

def create_crash_file(find_data_file: Callable[[str], str], message: str):
    directory = find_data_file('crashes')
    os.makedirs(directory, exist_ok=True)
    datetime_ = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
    with open(find_data_file(f'crashes\\crash_{datetime_}.txt'), 'wt', encoding='utf-8') as file:
        file.write(message)
