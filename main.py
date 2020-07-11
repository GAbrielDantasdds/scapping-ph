from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from urllib.request  import Request
from time import sleep


class noticia():
    """ Noticia de um dos jornais eletrôncicos. """

    def __init__(self: object, titulo: str, data_e_hora: list, autor: str, link: str, texto: str, link_img: str, editora: str) -> None:
        self.titulo   = titulo
        self.data     = data_e_hora
        self.autor    = autor
        self.link_img = link_img
        self.editora  = editora
        self.texto    = texto
        self.link_noticia = link

    def salvar_em_txt(self: object) -> None:
        """ Escreve em um arquivo .txt os dados da notícia. """

        div  = '-' * 60
        line = div + 'X-X-X' + div

        with open('noticias.txt', 'a') as file:
            file.write(f"{line}\n\nTitulo: {self.titulo}\
            \nData: {self.data[0]} {self.data[1]}\
            \nAutor: {self.autor}\
            \nLink: {self.link_noticia}\nLink imagem: {self.link_img}\
            \nTexto da Materia: \n{self.texto}Editora: {self.editora}\n")


def tratar_link(link: str) -> str:
    """ Filtra os links para apenas conteúdos do AM. Além disso adiciona parte do link. """

    if link.split('/')[1] == 'amazonas':
        return 'https://www.portaldoholanda.com.br' + link


def tratar_data(data: str) -> list:
    """ Separa a data da hora. """

    data = data.split()
    return [data[0], data[2]]


def tratar_autor(autor: str) -> str:
    """ Ajusta o nome do autor. """
    autor = autor.split()
    return ' '.join(autor)


def tratar_texto(texto: str) -> str:
    """ Trata a b-str para  str. """

    texto = texto.replace("\r", '')
    texto = texto.replace("\t", '')
    return texto


def obter_links() -> list:
    """ Entra no site, na parte do AM e pega os links das notícias. """

    lista_de_noticias = []
    req = Request('https://www.portaldoholanda.com.br/amazonas', headers={ 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' })
    site = urlopen(req)
    pag = site.read().decode("utf-8")
    soup = bs(pag, 'html.parser')
    feed = soup.find_all(attrs={"rel": "bookmark"})
    for f in feed:
        link = f.get_attribute_list('href')[0]
        if link not in lista_de_noticias:
            novo_link = tratar_link(link)
            if novo_link:
                lista_de_noticias.append(novo_link)

    return lista_de_noticias


def varrer_links(links: list) -> None:
    """ Pega os links e extrai as informações. """

    for url in links:
        req = Request(url, headers={ 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' })
        site = urlopen(req)
        pag = site.read().decode("utf-8")
        soup = bs(pag, 'html.parser')

        titulo = soup.find_all(class_='link_title')[0].getText()
        data   = tratar_data(soup.find_all(class_='post-date updated')[0].text)
        autor  = tratar_autor(soup.find_all(attrs={'rel': 'author'})[0].text)

        img_link    = 'https://www.portaldoholanda.com.br' + soup.find_all(class_='mvp-reg-img wp-post-image')[0].get_attribute_list('src')[0]

        texto = []

        para  = soup.find_all('p')[4:-2]

        for p in para:
            if len(list(p.children)) > 1:
                texto.append(p.contents[0])
            else:
                texto.append(p.text)

        texto = ''.join(texto)
        texto = tratar_texto(texto)

        nova_noticia = noticia(titulo, data, autor, url, texto, img_link, editora='Portal do Holanda')
        nova_noticia.salvar_em_txt()
        sleep(5)
        print("Notícia extraída...")


if __name__ == '__main__':
    print("Iniciando scraping...")
    varrer_links(obter_links())
