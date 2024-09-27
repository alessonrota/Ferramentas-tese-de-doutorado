from requests_html import HTMLSession
import requests
import warnings
warnings.filterwarnings("ignore")

DEFAULT_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'

session = HTMLSession();
headers = {'User-Agent': DEFAULT_USER_AGENT}

DOMAIN = 'https://digital.bbm.usp.br/handle/bbm/'
SHORT_DOMAIN = 'https://digital.bbm.usp.br'
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
    pdf_url = SHORT_DOMAIN + buttons[2].attrs.get('href')
    # print(pdf_url)
    return pdf_url

def download_pdf(url, file_name):

    response = requests.get(url, headers=headers, verify=False)

    with open('./usp/' + file_name + '.pdf', 'wb') as w:
        w.write(response.content)

def download_image(bookId):
    # folder.create_folder(str(bookId))
    url = DOMAIN + str(bookId)
    response = session.get(url, headers=headers, verify=False)
    response.html.render()
    author = response.html.find('.dc_contributor_author')

    # print("\n\n")
    # print("Autor: " + parse_author(author[1].text) + "\n")

    title = response.html.find('.dc_title');
    # print("Título: " + title[1].text + "\n")

    issued_date = response.html.find('.dc_date_issued');
    # print("Data: " + issued_date[1].text + "\n")


    file_name = generate_file_name(author[1].text, title[1].text, issued_date[1].text)
    pdf_url = get_pdf_url(response)
    download_pdf(pdf_url, file_name)

    print("================================== DOWNLOAD COMPLETO ==================================\n\n")


for id in range(1, 8200):
    print("\n==================================== BAIXANDO " + str(id) + " ====================================")
    try:
        download_image(id)
    except Exception as e:
        print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX ID ' + str(id) + ' NÃO EXISTE! XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n\n')
        pass

    




