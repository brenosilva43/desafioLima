from google.cloud import bigquery
import os
import configparser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

config = configparser.ConfigParser()
config.read('config.txt')
credentials_path = config['Conf']['path_key']
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
client = bigquery.Client()
table_id = config['Conf']['table_id']


chrome = webdriver.Chrome()
website = config['Bot']['site']
chrome.get(website)
resumoXpath = config['Bot']['xpath_resumo']
chamadaXpath = config['Bot']['xpath_chamada']

list = []

for z in range(1, 4):
    for x in range(1,4):
        schema = ['categoria', 'resumo', 'chamada', 'url']
        schemaCreate = dict.fromkeys(schema)
        if z == 1:
            schemaCreate['categoria'] = 'news'
        if z == 2:
            schemaCreate['categoria'] = 'esporte'
        if z == 3:
            schemaCreate['categoria'] = 'most popular'

        schemaCreate['resumo'] = str((WebDriverWait(chrome, 10)
           .until(EC.element_to_be_clickable((By.XPATH, resumoXpath
           .replace("li[1]","li["+str(x)+"]")
           .replace("section[1]","section["+str(z)+"]"))))).text)

        schemaCreate['chamada'] = str((WebDriverWait(chrome, 10)
           .until(EC.element_to_be_clickable((By.XPATH, chamadaXpath
           .replace("li[1]","li["+str(x)+"]")
           .replace("section[1]","section["+str(z)+"]"))))).text)

        schemaCreate['url'] = str((WebDriverWait(chrome, 10)
           .until(EC.element_to_be_clickable((By.XPATH, chamadaXpath
           .replace("li[1]","li["+str(x)+"]")
           .replace("section[1]","section["+str(z)+"]"))))).get_attribute('href'))
        list.append(schemaCreate)


client.insert_rows_json(table_id,list)
