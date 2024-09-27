from requests_html import HTMLSession
import requests
import warnings
warnings.filterwarnings("ignore")
import os

DEFAULT_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'

session = HTMLSession();
headers = {'User-Agent': DEFAULT_USER_AGENT}

# https://bdor.sibi.ufrj.br/handle/doc/100
DOMAIN = 'https://bdor.sibi.ufrj.br/handle/doc/'
SHORT_DOMAIN = 'https://bdor.sibi.ufrj.br'
MAX_LENGTH = 63


def parse_author(author):
    list = author.split(" ")
    #return author
    return list[0] + list[1]

def generate_file_name(rawAuthor, title, issued_date):
    author = parse_author(rawAuthor)
    maxTitleLength = MAX_LENGTH - 6 - len(author)
    partialTitle = title[0:maxTitleLength].replace(":", "_");
    file_name = author + '@' + partialTitle + '$' + str(issued_date)
    # print(file_name)
    return file_name

def get_pdf_url(response):
    buttons = response.html.find('.btn-primary')
    pdf_url = SHORT_DOMAIN + buttons[1].attrs.get('href')
    # print(pdf_url)
    return pdf_url

def get_file_size(file_name):
    return os.path.getsize('./ufrj/' + file_name + '.pdf')

def download_pdf(url, file_name):

    response = requests.get(url, headers=headers, verify=False)

    with open('./ufrj/' + file_name + '.pdf', 'wb') as w:
        w.write(response.content)

    if (get_file_size(file_name) == 0):
        download_pdf(url, file_name)

def download_book(bookId):
    # folder.create_folder(str(bookId))
    url = DOMAIN + str(bookId)
    response = session.get(url, headers=headers, verify=False)
    response.html.render()

    if (response.status_code == 404):
        print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX ID ' + str(bookId) + ' NÃO EXISTE! XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n\n')
        return

    # print(response.status_code)
    author = response.html.find('.author')

    # print("\n\n")
    # print("Autor: " + parse_author(author[0].text) + "\n")

    title = response.html.find('.metadataFieldValue');
    # print("Título: " + title[1].text + "\n")

    issued_date = response.html.find('.metadataFieldValue');
    # print("Data: " + issued_date[9].text + "\n")


    file_name = generate_file_name(author[0].text, title[1].text, issued_date[9].text)
    pdf_url = get_pdf_url(response)
    download_pdf(pdf_url, file_name)

    print("================================== DOWNLOAD COMPLETO ==================================\n\n")



# download_book(100)

for id in range(1, 1000):
    print("\n==================================== BAIXANDO " + str(id) + " ====================================")
    try:
        download_book(id)
    except Exception as e:
        print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX ID ' + str(id) + ' NÃO EXISTE! XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n\n')
        pass

    




