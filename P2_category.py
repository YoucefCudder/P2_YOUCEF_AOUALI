#!/usr/bin/python3
# coding: utf8


import requests
from bs4 import BeautifulSoup
import re
import csv

def get_url_from_all_categories(homepage_source_code):
    category_links_list = []
    try:

        find_category_links = homepage_source_code.find('ul', {'class': 'nav nav-list'})
        find_category_links = find_category_links.find_all('li')[1:57]
        for links in find_category_links:
            category_link = links.find('a')['href']
            category_link = homepage_url + category_link
            category_links_list.append(category_link)
        return category_links_list
    except Exception as error:
        print(f"Erreur lors de la reception urls des catégories : {error}")
def get_source_code_from_category_page(category_url):
    try:
        request_get_source_code = requests.get(category_url)
        category_page_html = BeautifulSoup(request_get_source_code.text, "html.parser")
        return category_page_html
    except Exception as error:
        print(f"Erreur lors de la reception du code source : {error}")

def get_max_page_to_scrap_of_category(category_url):
    max_page = 1 # Par défaut, nous avons une seule page à scrap.

    request_get_source_code = requests.get(category_url)
    category_page_html = BeautifulSoup(request_get_source_code.text, "html.parser")

    txt_max_pages = category_page_html.find("li", {"class": "current"})
    if txt_max_pages is not None: # Si il trouve le bloc de textes : "page 1 sur X"
        get_last_page_str = re.sub('Page 1 of ', '', txt_max_pages.text) # On supprime Page 1 of dans notre chaine de caracters. Il reste plus que des espaces et
        # le numéro de la derniere page. On peut donc le convertir en INT, vu qu'il n'y a plus de lettre :)
        max_page = int(get_last_page_str)

    return max_page
    
def scrap_page_of_category(category_url, total_pages):
    global category_page_html
    page_to_scrap = category_url
    books = []
    products_links_list = []
    link_products = category_page_html.find_all('h3')
    for link in link_products:
        product_link = link.find('a')['href']
        product_link = product_link.replace('../../../', 'https://books.toscrape.com/catalogue/')
        products_links_list.append(product_link)
    i = 0 # On initialise un compteur de boucle
    while i < total_pages:
        i += 1
        if i != 1:
            page_to_scrap = re.sub('index', f'page-{i}', category_url)
        # ICI TU SAIS COMMENT FAIRE, tu as le code pour récupérer les données des livres :)
        print(page_to_scrap)
        request_get_source_code = requests.get(page_to_scrap)
        category_page_html = BeautifulSoup(request_get_source_code.text, "html.parser")

        # books_to_scrap = category_page_html.find_all("li", {"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"})

        try:
                for product_link in products_links_list:
                    request_get_source_code = requests.get(str(product_link))
                    product_page_html = BeautifulSoup(request_get_source_code.text, "html.parser")

                    get_inner_page = product_page_html.find('div', {'class': 'container-fluid page'})
                    get_main_bloc = product_page_html.find('div', {'class': 'col-sm-6 product_main'})
                    book = []
                    book.append(product_link)

                    get_title = get_inner_page.find('h1').text
                    book.append(get_title)
                    get_upc = get_inner_page.find_all('td')[0].text
                    book.append(get_upc)
                    get_price_incl = get_inner_page.find_all('td')[2].text
                    book.append(get_price_incl)
                    get_price_excl = get_inner_page.find_all('td')[3].text
                    book.append(get_price_excl)

                    get_category = get_inner_page.find('ul', {'class': 'breadcrumb'}).find_all('li')[2].text
                    book.append(get_category)
                    get_description = get_inner_page.find('p', {'class': ''})
                    book.append(get_description)
                    get_number = get_inner_page.find_all('td')[5].text
                    book.append(get_number)

                    class_name = []
                    for element in get_main_bloc.find_all(class_='star-rating'):
                        class_name.extend(element["class"])
                        get_ratings = (class_name[1] + " out of five")
                    book.append(get_ratings)

                    to_get_image = get_inner_page.find('div', {'class': 'item active'}).find('img')
                    get_image_url = to_get_image['src'].replace('../../', 'http://books.toscrape.com/')
                    book.append(get_image_url)

                    books.append(book)

        except Exception as error:
            print(f"Erreur sur un bouquin : {error}")
            pass

    columns = ['URL_product', 'Title', 'UPC',
               'Price_including_tax', 'Price_excluding_tax',
               'Category', 'Description', 'Number_available',
               'Ratings', 'Image_URL']
    with open('book_category.csv', 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        columnz = writer.writerow(columns)
        for book in books:
            csv_books = writer.writerow(book)
    return books

# execution des fonctions

if __name__ == "__main__":
    try:

        category_urls = ['https://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html', 'https://books.toscrape.com/catalogue/category/books/travel_2/index.html']
        for category_url in category_urls:
            total_pages = get_max_page_to_scrap_of_category(category_url)
            category_page_html = get_source_code_from_category_page(category_url)

            print(f"Pour l'url {category_url} : je trouve {total_pages} page à scrap :) ")
            books_of_category = scrap_page_of_category(category_url, total_pages)
            print(books_of_category)

    except Exception as error:
        print(f"erreur lors de l'execution du script : {error}")
