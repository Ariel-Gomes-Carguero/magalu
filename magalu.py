from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders



import time
def parsing(tag):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path="chromedriver.exe", options=chrome_options)
    try:
        driver.get("https://www.magazineluiza.com.br/")
        testando = str(tag)
        time.sleep(5)
        buscar = driver.find_element_by_id("inpHeaderSearch").send_keys(testando)


        driver.find_element_by_id("inpHeaderSearch").send_keys(Keys.ENTER)
        time.sleep(10)
        paginacao = driver.current_url
        varios = (paginacao + "&results_per_page=200")
        driver.get(varios)
        all_products = driver.find_elements_by_class_name("product-li")
        produtos = []


        if all_products:
            print("Aguarde enquanto a busca é feita !")
            for i in all_products:

                produtos.append(i.get_attribute('href'))

            for acesso in produtos:
                driver.get(acesso)
                titulo = driver.find_elements_by_xpath("//h1[@class='header-product__title']")
                for i in titulo:
                    titu_product = (i.text)

                for price in driver.find_elements_by_xpath("//span[@class='price-template__text']"):
                    uniq = (price.text)

                    with open('links.csv', 'a') as arquivo:
                        time.sleep(5)
                        arquivo.writelines("Produto: {} Valor:{} Link:{} \n".format(titu_product, uniq, acesso))

        else:
            print("Nada foi encontrado :(")
    except SystemError:
        print("OPS, houve algum erro na busca !")



def enviar():
    try:
        fromaddr = "EMAIL ORIGEM"
        toaddr = 'EMAIL DESTINO'
        msg = MIMEMultipart()

        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Suas Buscas estão prontas"

        body = "\nOlá, seu robô de busca enviou o arquivo com todos os links encontrados !"

        msg.attach(MIMEText(body, 'plain'))

        filename = 'links.csv'

        attachment = open('links.csv', 'rb')

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        msg.attach(part)

        attachment.close()

        server = smtplib.SMTP('smtp.PROVEDOR.com', 587)
        server.starttls()
        server.login(fromaddr, "DIGITE AQUI SUA SENHA")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        print('\nEmail enviado com sucesso!')
    except:
        print("\nErro ao enviar email")

def menu():
    print('''
    
 |  \/  |   __ _    __ _    __ _  | |  _   _ 
 | |\/| |  / _` |  / _` |  / _` | | | | | | |
 | |  | | | (_| | | (_| | | (_| | | | | |_| |
 |_|  |_|  \__,_|  \__, | t \__,_| |_|  \__,_|
                   |___/             1.0 beta
                   
    ''')




menu()
item = input("Qual produto deseja buscar?: ")
parsing(item)
enviar()
