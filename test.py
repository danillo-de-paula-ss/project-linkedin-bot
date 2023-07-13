# import os
# # # from cryptography.fernet import Fernet

# # # login_frame_keys = ['-USER-', '-PASSWORD-', '-RADIO-CAPTCHAa-', '-RADIO-CAPTCHAb-', '-LOGIN-']
# # # print(login_frame_keys[:-1])

# # # print('alall'[:-2])

# # # print(f'C:\\Users\\{os.getlogin()}\\Documents')

# # text1 = '''👉 Para saber todas as informações sobre a vaga de emprego, acesse nosso blog aqui:  www.vagaseolica.com

# # ✅  Participe do nosso grupo de whatsapp e não perca mais nenhuma vaga quando for postada: 👉www.vagaseolica.com/p/whatsapp.html 

# # 😱 O "segredo" nunca revelado antes! Descubra agora o passo a passo para ser contratado no setor de energia eólica! 
# # Clique aqui agora: 👉https://bit.ly/seuprimeiroempregonaeolica_live'''

# # text2 = ['👉 Para saber todas as informações sobre a vaga de emprego, acesse nosso blog aqui: www.vagaseolica.com\n\n✅ Participe do nosso grupo de whatsapp e não perca mais nenhuma vaga quando for postada: 👉\n\n😱 O "segredo" nunca revelado antes! Descubra agora o passo a passo para ser contratado no setor de energia eólica!\nClique aqui agora: 👉']

# # # text2 = 'msadmash,jfda,shfd'

# # # print(text2.split('\n')[0].split('www.')[0] in text1)
# # # print(text2.split('\n')[0].split('www.')[0])

# # print(any(map(lambda reply: reply.split('\n')[0].split('www.')[0] in text1, text2)))

# # # x = 1
# # # while x >= 0:
# # #     status = text2.split('\n')[0][:-x] in text1.split('\n')[0]
# # #     print(status)
# # #     if status: break
# # #     x += 1

# # # print(s.encode('unicode-escape'))
# # # print(s.encode('unicode-escape').decode('ASCII'))
# # # key = Fernet.generate_key()
# # # print('Key: ', key.decode())

# # # key = b'C5S5cpuAyO_XDOHX2Rr5MnHu64Ne6Bzg_pKsk1l9zag='
# # # message = 'Olá'
# # # token = Fernet(key).encrypt(message.encode())
# # # print(token)
# # # print(Fernet(key).decrypt(token).decode())
# # # print(key.decode())

# # t1 = '''👉 Para saber todas as informações sobre a vaga de emprego, acesse nosso blog aqui: www.vagaseolica.com

# # ✅ Participe do nosso grupo de whatsapp e não perca mais nenhuma vaga quando for postada: 👉www.vagaseolica.com/p/whatsapp.html 

# # ☑ Transforme sua vida com as vagas de emprego mais promissoras no setor de energia eólica. Saiba mais: https://www.vagaseolica.com/2023/06/seu-primeiro-emprego-na-industria.html'''

# # t2 = '''👉 Para saber todas as informações sobre a vaga de emprego, acesse nosso blog aqui: www.vagaseolica.com

# # ✅ Participe do nosso grupo de whatsapp e não perca mais nenhuma vaga quando for postada: 👉www.vagaseolica.com/p/whatsapp.html 

# # ☑ Transforme sua vida com as vagas de emprego mais promissoras no setor de energia eólica. Saiba mais: https://www.vagaseolica.com/2023/06/seu-primeiro-emprego-na-industria.html'''

# # print(t1 == t2)

# with open(f'C:\\Users\\{os.getlogin()}\\Documents\\mensagem_para_envio.txt', 'rt', encoding='utf-8') as file:
#     print(file.read())

# from utilities.exceptions import *

# try:
#     raise BotStopped
# except Exception as err:
#     print(err.args)
#     if isinstance(err, BotStopped):
#         print('sim')
#     else:
#         print('não')

# import emoji

# s = '😀'
# print(s.encode('unicode-escape').decode('ASCII'))

# print(emoji.is_emoji('❤'))

# text1 = '''👉 Para saber todas as informações sobre a vaga de emprego, acesse nosso blog aqui: www.vagaseolica.com

# ✅ Participe do nosso grupo de whatsapp e não perca mais nenhuma vaga quando for postada: 👉www.vagaseolica.com/p/whatsapp.html 

# ☑ Transforme sua vida com as vagas de emprego mais promissoras no setor de energia eólica. Saiba mais: https://www.vagaseolica.com/2023/06/seu-primeiro-emprego-na-industria.html'''

# text2 = '''👉 Para saber todas as informações sobre a vaga de emprego, acesse nosso blog aqui: www.vagaseolica.com

# ✅\xa0Participe do nosso grupo de whatsapp e não perca mais nenhuma vaga quando for postada: 👉www.vagaseolica.com/p/whatsapp.html 

# ☑ Transforme sua vida com as vagas de emprego mais promissoras no setor de energia eólica. Saiba mais: https://www.vagaseolica.com/2023/06/seu-primeiro-emprego-na-industria.html'''

text1 = ['👉 Para saber todas as informações sobre a vaga de emprego, acesse nosso blog aqui: www.vagaseolica.com\n\n✅ Participe do nosso grupo de whatsapp e não perca mais nenhuma vaga quando for postada: 👉www.vagaseolica.com/p/whatsapp.html \n\n☑ Transforme sua vida com as vagas de emprego mais promissoras no setor de energia eólica. Saiba mais: https://www.vagaseolica.com/2023/06/seu-primeiro-emprego-na-industria.html'][0]

text2 = ['👉 Para saber todas as informações sobre a vaga de emprego, acesse nosso blog aqui: www.vagaseolica.com\n\n✅ Participe do nosso grupo de whatsapp e não perca mais nenhuma vaga quando for postada: 👉www.vagaseolica.com/p/whatsapp.html\n\n☑ Transforme sua vida com as vagas de emprego mais promissoras no setor de energia eólica. Saiba mais: https://www.vagaseolica.com/2023/06/seu-primeiro-emprego-na-industria.html'][0]

text1 = '\n'.join([t.strip() for t in text1.splitlines()])
text2 = '\n'.join([t.strip() for t in text2.splitlines()])

print(text1 == text2)

def check_text(text1:str, text2:str, percentage:int) -> bool:
    count = 0
    for char1, char2 in zip(text1, text2):
        if char1 == char2:
            count += 1
    # print(count, '>=', len(text1) * (percentage / 100))
    return count >= len(text1) * (percentage / 100)

print(check_text(text1, text2, 50))

with open('t.txt', 'a', encoding='utf-8') as file:
    file.write(f'{text1}\n')
    file.write(f'{text2}\n')
with open('t.txt', 'a', encoding='utf-8') as file:
    file.write(f'{text1}\n')
    file.write(f'{text2}\n')
