from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd
import time
import pyautogui
import os
import numpy as np


# iniciar webdriver
class AutomacaoSantanderBenner:
    # Ler Exel e carregar as funções do webdriver
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option(
            "prefs",
            {
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True,
            },
        )
        load_dotenv()  # Carrega as variáveis do arquivo .env
        self.login = os.getenv("LOGIN")
        self.password = os.getenv("PASSWORD")
        # Service initialization parameters
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.df = None
        self.df = pd.read_excel("Pasta1.xlsx")
        # self.new_df = pd.read_excel('analisado.xlsx')

    # acessar benner
    def conectar_internet(self):
        self.driver.get(
            "https://www.santandernegocios.com.br/portaldenegocios/#/externo"
        )

    # fazer login no benner
    def logar_santander(self):
        login_input = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, "userLogin__input"))
        )
        login_input.send_keys(self.login)
        time.sleep(2)
        password_input = self.driver.find_element(By.ID, "userPassword__input")
        password_input.send_keys(self.password)
        time.sleep(2)
        login_button = self.driver.find_element(
            By.XPATH,
            "/html/body/app/ui-view/login/div/div/div/div/div[2]/div[3]/button[2]",
        )
        login_button.click()
        time.sleep(6)

    # Mover para Segunda tela do benner
    def ir_para_segunda_tela(self):
        botao_login = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "icon"))
        )
        botao_login.click()
        botao_entrada = self.driver.find_element(
            By.XPATH, '//*[@id="header"]/div[4]/user-menu/div/nav/div/div[2]/ul/li[2]/a'
        )
        botao_entrada.click()
        time.sleep(6)
        self.aba_nova = self.driver.window_handles[1]
        self.aba_original = self.driver.window_handles[0]
        self.driver.switch_to.window(self.aba_nova)

    # Pesquisar o processo
    def pesquisar_processo(self):
        for index, row in self.df.iterrows():
            # Clicar no elemento "processos"
            element = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="topmenu-PR_PROCESSOS_MENU"]/a')
                )
            )
            element.click()
            time.sleep(2)

            # Clicar duas vezes no elemento "processos"
            processos = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="ctl00_Main_WIDGETID_635929640475007316_FilterControl_GERAL_PROCESSO"]',
                    )
                )
            )
            self.actions.double_click(processos).perform()

            # Limpar campo de busca
            self.actions.key_down(Keys.CONTROL).send_keys("a").key_up(
                Keys.CONTROL
            ).send_keys(Keys.DELETE).perform()
            time.sleep(1)

            # Escrever o número da integração no campo de busca
            processos.send_keys(str(row["CD_DOSS_PROC"]))
            self.driver.find_element(
                By.ID,
                "ctl00_Main_WIDGETID_635929640475007316_FilterControl_FilterButton",
            ).click()
            time.sleep(3)

            try:
                elemento = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            '//*[@id="ctl00_Main_WIDGETID_635929640475007316_SimpleGrid"]/tbody/tr[1]/td[6]/a',
                        )
                    )
                )
                self.driver.execute_script("arguments[0].click();", elemento)
            except Exception as e:
                print(f"Erro ao clicar no elemento: {str(e)}")

            # Procurar pelos pedidos
            self.driver.execute_script(
                "javascript:__doPostBack('ctl00$Main$PEDIDOS_GRID','New')"
            )
            time.sleep(5)

            # mudar para iframe
            iframe = '//*[@id="ModalCommand_modal"]/div/div/div[2]/iframe'
            WebDriverWait(self.driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.XPATH, iframe))
            )

            # Caixa de texto para danos morais
            self.driver.find_element(
                By.XPATH,
                '//*[@id="ctl00_Main_PR_PROCESSOPEDIDOS_FORM_PageControl_GERAL_GERAL"]/div[1]/div[3]/div/span/div/span[1]/span[1]/span',
            ).click()

            text_key = self.driver.find_element(
                By.XPATH, '//*[@id="ctl00_Body"]/span/span/span[1]/input'
            )
            text_key.send_keys("DANOS MORAIS")

            opt = self.driver.find_element(
                By.XPATH,
                '//*[@id="select2-ctl00_Main_PR_PROCESSOPEDIDOS_FORM_PageControl_GERAL_GERAL_ctl12_ctl01_select-results"]/li[2]',
            ).click()

            # Data
            data_key = self.driver.find_element(
                By.XPATH,
                '//*[@id="ctl00_Main_PR_PROCESSOPEDIDOS_FORM_PageControl_GERAL_GERAL_DATAPEDIDO_DATE"]',
            )
            data_key.send_keys(str(row["DT_CADR_PROC"]))

            # Pedido
            pedido_key = self.driver.find_element(
                By.XPATH,
                '//*[@id="ctl00_Main_PR_PROCESSOPEDIDOS_FORM_PageControl_GERAL_GERAL_VALORPEDIDO"]',
            )
            pedido_key.send_keys(str(row["Pedidos"]))

            # Riscos
            self.driver.find_element(
                By.XPATH,
                '//*[@id="ctl00_Main_PR_PROCESSOPEDIDOS_FORM_PageControl_GERAL_GERAL"]/div[4]/div/div/div[11]/div/span/div/span[1]/span[1]/span',
            ).click()
            
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="select2-ctl00_Main_PR_PROCESSOPEDIDOS_FORM_PageControl_GERAL_GERAL_ctl146_ctl01_select-results"]/li[3]',
                    )
                )
            ).click() 
            
            time.sleep(3)
            
            # Botão Salvar
            self.driver.execute_script("javascript:__doPostBack('ctl00$Main$PR_PROCESSOPEDIDOS_FORM','Save')")
            
            # expandir decisões
            self.driver.execute_script("javascript:;")

    def executar(self):
        while True:
            try:
                self.conectar_internet()
                self.logar_santander()
                self.ir_para_segunda_tela()
                self.verificar_arquivo_e_fechar_driver()
                self.pesquisar_processo()
                break
            except NoSuchElementException as e:
                print(f"Error: {e}")
                time.sleep(10)
                i = 0
                while i < 10:
                    print(f"Reiniciando em {i}")
                self.driver.quit()
                
            
                
if __name__ == '__main__':
    bot = AutomacaoSantanderBenner()
    bot.executar()