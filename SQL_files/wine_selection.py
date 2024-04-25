import requests
from bs4 import BeautifulSoup
from SQL_files.BD import create_conection, execute_query, execute_read_query, delete_wine, create_wine_table, output_wine

headers = {
   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
}

def get_page(url):
    s = requests.Session()
    response = s.get(url=url, headers=headers)

    with open("index.html", "w", encoding="utf-8") as file:
        file.write(response.text)


def from_soup():
    html_file = ("index.html")
    html_file = open(html_file, encoding='UTF-8').read()
    soup = BeautifulSoup(html_file, 'lxml')

    wine = []
    for link in zip(soup.find_all('div', id="snippet-buy-block"), soup.find_all('div', class_=["snippet-price__total", "snippet-price__total snippet-price__total-black"])):
        W = (link[0].get('data-product-name'), link[1].get('content'), link[0].get('data-product-country'), link[0].get('data-product-wine-label'),link[0].get('data-product-type'), 'https://simplewine.ru' + link[0].get('data-product-href'))
        if W not in wine:
            wine.append(W)


    wine_records = ", ".join(["%s"] * len(wine))

    insert_query = (
        f"INSERT INTO wine (name, price, country, color, sugar, link) VALUES {wine_records}"
    )

    connection = create_conection()
    execute_query(connection, delete_wine)
    execute_query(connection, create_wine_table)

    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(insert_query, wine)
    except:
        pass
  
   



def filters(prc_from='', prc_to='', *args):
    gastronomy = {
        'Говядина': 'govyadina',
        'Рыба': 'ryba',
        'Выдержанный сыр': 'vyderzhannyy_syr',
        'Морепродукты': 'moreprodukty',
        'Утка': 'utka',
        'Сыр': 'syr',
        'Закуски, салаты и антипасто': 'zakuski_salaty_i_antipasto',
        'Курица': 'kuritsa',
        'Свинина': 'svinina',
        'Ягненок': 'yagnenok',
        'Паста': 'pasta',
        'Мягкий сыр': 'myagkiy_syr',
        'Овощи': 'ovoshchi',
        'Азиатская кухня': 'aziatskaya_kukhnya',
        'Десерты и выпечка': 'deserty_i_vypechka',
        'Кролик': 'krolik',
        'Оленина': 'olenina',
        'Ризотто': 'rizotto',
        'Грибы': 'griby',
        'Фрукты и ягоды': 'frukty_i_yagody',
        'Хамон': 'khamon',
        'Салями': 'salyami',
        'Японская кухня': 'yaponskaya_kukhnya',
        'Шоколад': 'burger',
        'Бургер': 'shokolad'
    }

    food = 'food-'
    args = sorted(args)
    food += gastronomy[args[0]]
    if len(args) > 1:
        for arg in args[1:]:
            food += '-or-' + gastronomy[arg]
        
    price_from = '-from-'+ prc_from
    price_to = '-to-' + prc_to
    if prc_from == '':
        price = 'main' + price_to + '/'
    elif prc_to == '':
        price = 'main' + price_from + '/'
    elif prc_from != '' and prc_to != '':
        price = 'main'+ price_from + price_to + '/'
    else:
        price = ''


    return 'filter/' + food + '/' + price



def bd_wine(prc_from, prc_to, *args):
    
    url = "https://simplewine.ru/catalog/vino/" + filters(prc_from, prc_to, *args)
    get_page(url)
    from_soup()


