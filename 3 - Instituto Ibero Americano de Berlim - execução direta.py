from requests_html import HTMLSession
import os

# URLs base para download de imagens
DOMAIN = 'https://digital.iai.spk-berlin.de/viewer/api/v1/records/'
SHORT_DOMAIN = 'https://digital.iai.spk-berlin.de/viewer/image/'

# ID do livro
ID = '837302463'

# Parâmetros para o download de imagens em alta resolução
SIZE = '.tif/full/2048,/0/default.jpg'

# Diretório principal onde os arquivos serão salvos
parent_dir = "G:/Banco de dados/Base de dados/new germany restantes/alema"

# Define o User-Agent para simular um navegador real ao fazer as requisições
DEFAULT_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'

# Inicializa uma sessão HTML para gerenciar requisições
session = HTMLSession()
headers = {'User-Agent': DEFAULT_USER_AGENT}

# Função para criar uma pasta para salvar o livro
def create_folder(name):
    try:
        # Cria o diretório com base no nome fornecido
        path = os.path.join(parent_dir, name)
        os.mkdir(path)
        print(f"Diretório '{name}' criado.")
    except OSError as e:
        # Se o diretório já existir, exibe uma mensagem e ignora o erro
        if e.errno == 17:
            print(f"Diretório '{name}' já existe.")
            pass

# Função para carregar os livros que serão processados
def load_books():
    # Mapa que relaciona IDs dos livros com suas configurações (neste caso, a página inicial)
    map = {}
    map["828135681"] = [0]  # Exemplo de livro a ser baixado
    return map

# Carrega os livros a partir da função `load_books`
books = load_books()

# Índice de início (primeira página)
start = 0

# Função para configurar a URL de download de cada página do livro
def setup_url(bookId, index):
    images = bookId + '/files/images/'
    page = start + index
    url = DOMAIN + images + str(page).zfill(8) + SIZE  # Formata a URL com o número da página preenchido com zeros à esquerda
    return url

# Função para obter o número de páginas do livro a partir da URL da biblioteca
def get_number_of_pages(bookId):
    url = SHORT_DOMAIN + str(bookId)
    response = session.get(url, headers=headers)
    response.html.render()
    number_of_pages = response.html.find('.navigate_last')
    print("Número de páginas: ", number_of_pages[0].text)
    return int(number_of_pages[0].text)

# Função para fazer o download da imagem de uma página
def download_image(bookId, url, page):
    print(f"Baixando Página: {page}")
    response = session.get(url, headers=headers)
    response.html.render()
    img = response.html.find('img')  # Localiza a tag 'img', embora não pareça ser usada
    with open(os.path.join(parent_dir, bookId, f'page-{str(page).zfill(3)}.jpg'), 'wb') as w:
        w.write(response.content)  # Salva o conteúdo da imagem no diretório apropriado

# Função principal para baixar todas as páginas de um livro
def download_book(bookId):
    print(f"\nBaixando livro: {bookId}")
    pagesWithError = []
    create_folder(bookId)  # Cria o diretório para armazenar as páginas do livro
    config = books.get(bookId)
    numberOfPages = get_number_of_pages(bookId)  # Obtém o número total de páginas
    numberOfPages += 1  # Incrementa o número total de páginas para a contagem correta
    for index in range(1, numberOfPages):
        url = setup_url(bookId, index)
        try:
            download_image(bookId, url, index)  # Tenta baixar cada página
        except Exception as e:
            print(e)
            pagesWithError.append(index)  # Armazena as páginas que não puderam ser baixadas

    # Tenta baixar novamente as páginas que tiveram erro
    print("\n\nPáginas com erro: ", pagesWithError)
    print("\n")
    while len(pagesWithError) > 0:
        print(f"Número de páginas restantes: {len(pagesWithError)}")
        index = pagesWithError.pop()
        url = setup_url(bookId, index)
        try:
            download_image(bookId, url, index)
        except Exception as e:
            pagesWithError.append(index)

# Loop que percorre todos os livros carregados e inicia o processo de download
for bookId in books:
    download_book(bookId)
