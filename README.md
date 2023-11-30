# Automação Santander Benner

Este script Python realiza automação no portal Santander Benner, acessando informações e preenchendo formulários usando Selenium.

## Funcionalidades

- **Conectar à Internet**: Abre o navegador Chrome e acessa o portal Santander Negócios.
- **Login no Portal**: Realiza o login usando credenciais fornecidas por meio de variáveis de ambiente.
- **Navegação no Portal**: Navega para a segunda tela do portal, onde a busca e preenchimento de processos é feita.
- **Preenchimento de Formulários**: Preenche formulários com informações de um arquivo Excel.

## Requisitos

- Python 3.x
- Bibliotecas Python: pandas, selenium, webdriver_manager, dotenv, pyautogui
- Navegador Chrome instalado

## Uso

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Configure as variáveis de ambiente no arquivo .env com suas credenciais:
```bash
LOGIN=seu_login
PASSWORD=sua_senha
```

3. Coloque seu arquivo Excel como entrada no código:
```bash
self.df = pd.read_excel("nome_do_arquivo.xlsx")
```

4. Execute o script:
```bash
python main.py
```