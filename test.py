# def repetir_processo(driver: WebDriver, wait: WebDriverWait):
    # thread = threading.current_thread()
    # stop = False
    # while stop == False:
    #     # navegar até a página alvo
    #     driver.get('https://www.instagram.com/devaprender/')
    #     sleep(5)
    #     # clicar na última postagem
    #     postagens: list[WebElement] = wait.until(expected_conditions.visibility_of_any_elements_located(
    #         (By.XPATH, '//div[@class="_aabd _aa8k _aanf"]')))
    #     postagens[0].click()
    #     sleep(5)
    #     # verificar se postagem foi curtida, caso não tenha sido, clicar em curtir, caso já tenha sido, aguardar 24 horas
    #     elementos_postagens: list[WebElement] = wait.until(
    #         expected_conditions.visibility_of_any_elements_located((By.XPATH, '//div[@class="_abm0 _abl_"]')))
    #     if len(elementos_postagens) == 7:
    #         elementos_postagens[1].click()
    #     else:
    #         print('postagem já foi curtida')
    #     for _ in range(86400):
    #         if getattr(thread, 'do_run', True) == False:
    #             stop = True
    #             break
    #         sleep(1)

# # clicar e digitar o meu usuário
# campo_usuario: WebElement = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//input[@name="username"]')))
# campo_usuario.send_keys('danillodepaula238@gmail.com')
# sleep(3)
# # clicar e digitar a minha senha
# campo_senha: WebElement = wait.until(expected_conditions.element_to_be_clickable(
#     (By.XPATH, '//input[@name="password"]')))
# campo_senha.send_keys('sagavazas')
# sleep(3)
# # clicar no campo entrar
# botao_entrar: WebElement = wait.until(
#     expected_conditions.element_to_be_clickable((By.XPATH, '//div[text()="Entrar"]')))
# botao_entrar.click()
# sleep(3)
# thread = threading.Thread(target=repetir_processo, args=(driver, wait), daemon=True)
# thread.start()
# while keyboard.is_pressed('1') == False:
#     pass
# thread.do_run = False
# thread.join()
# driver.quit()
