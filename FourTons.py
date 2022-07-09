from bs4 import BeautifulSoup
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import shutil
import requests
import zipfile
import os
import re
import wget

URL = 'http://www.4tons.com.br/03discos.htm'
allowed_domains = 'http://www.4tons.com.br'
headers = {'User_agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " +
                         "(KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}

site = requests.get(URL, headers=headers)
soup = BeautifulSoup(site.content, 'html.parser')
table = soup.body.find_all('table', class_='MsoTableGrid')

Dados = []
contador = 0
for tabela in table:
    Registros = tabela.find_all('p')
    for ref in Registros:
        contador = contador + 1
        print(r"Registro {} de {}".format(contador, len(Registros)))
        if ref.a and ref.a.get('href') is not None and ref.a.get('href') != '#KINGS' and ref.a.get(
                'href') != '#TOPO' and ref.span.text != '':
            url = allowed_domains + '/' + ref.a.get('href').replace('../', '').replace(r"%20", " ")
            album = ref.span.text.replace('TOPO', '').replace('\r\n', '').strip()
            Dados.append([album, url])
            try:
                resposta = wget.download(url, album + r".zip")
                print("Download finalizado. Salvo em: {}".format(album + '.zip'))
            except Exception as e:
                print(r"Falha ao baixar o arquivo: {}".format(album + r".zip"))

            my_dir = r"C:\Users\Heinz2\Music\The King's Heralds\Teste"
            if not os.path.exists(album + '.zip'):
                continue

            try:
                with zipfile.ZipFile(album + '.zip') as filezip:
                    if filezip.testzip() is not None:
                        os.remove(album + '.zip')
                        print(r"Erro ao descompactar o arquivo {}".format(album + '.zip'))
                        continue

                    for membro in filezip.namelist():
                        if not membro.endswith(".mp3"):
                            continue
                        nomeArquivo = os.path.basename(membro)
                        if os.path.dirname(membro) == '':
                            Folder = "The King's Heralds - " + album
                        else:
                            Folder = "The King's Heralds - " + os.path.dirname(membro)

                        if not nomeArquivo:
                            os.remove(album + '.zip')
                            print(r"Erro ao descompactar o arquivo {}".format(album + '.zip'))
                            continue

                        folderDestino = my_dir + r"\\" + Folder
                        if not os.path.isdir(folderDestino):
                            os.mkdir(folderDestino)

                        source = filezip.open(membro)
                        target = open(os.path.join(folderDestino, nomeArquivo), "wb")
                        with source, target:
                            shutil.copyfileobj(source, target)

                        Musica = MP3(os.path.join(folderDestino, nomeArquivo), ID3=EasyID3)
                        titulo = re.sub(r"[^a-zA-Z ]", r"", nomeArquivo.replace('.mp3', ''))
                        Musica['title'] = titulo
                        Musica['album'] = os.path.dirname(membro)
                        Musica['artist'] = r"The King's Heralds"
                        Musica['albumartist'] = "The King's Heralds"
                        Musica['genre'] = "Teste"
                        Musica.save()

                os.remove(album + '.zip')
                filezip.close()
            except zipfile.error as ex:
                os.remove(album + '.zip')
                print(r"Erro ao descompactar o arquivo {}".format(album + '.zip'))
                continue
