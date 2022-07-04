from bs4 import BeautifulSoup
import requests
import zipfile as zipcompact

URL = 'http://www.4tons.com.br/03discos.htm'
allowed_domains = 'http://www.4tons.com.br'
headers = {'User_agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}

site = requests.get(URL, headers=headers)
soup = BeautifulSoup(site.content, 'html.parser')
table = soup.body.find_all('table', class_='MsoTableGrid')

Dados = []
for tabela in table:
    registros = tabela.find_all('p')
    for ref in registros:
        if ref.a and ref.a.get('href') != None and ref.a.get('href') != '#KINGS' and ref.a.get(
                'href') != '#TOPO' and ref.span.text != '':
            url = allowed_domains + '/' + ref.a.get('href').replace('..', '')
            album = ref.span.text.replace('TOPO', '').replace('\r\n', '').strip()
            Dados.append([album, url])
            resposta = requests.get(url)
            if resposta.status_code == requests.codes.OK:
                with open(album + '.zip', 'wb') as novo_arquivo:
                    novo_arquivo.write(resposta.content)
                print("Download finalizado. Salvo em: {}".format(album + '.zip'))
            else:
                resposta.raise_for_status()

            zf = zipcompact.ZipFile(album + '.zip')
            list = zf.namelist()

            for arquivo in list:
                zf.extract(arquivo, r'd:\test"\"' + arquivo)