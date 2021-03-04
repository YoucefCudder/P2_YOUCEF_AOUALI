#!/usr/bin/python3
# coding: utf8
import re
import csv
import os
import requests
from bs4 import BeautifulSoup
import wget


# fonction pour extraire les infos brutes

def get_source_code_from_homepage():
    """
récupérer le code source
    :return:
    """
    try:
        requests_get_source_code = requests.get(HOMEPAGE_URL)
        homepage_code_souce: BeautifulSoup = BeautifulSoup(
            requests_get_source_code.text, "html.parser"
        )

        return homepage_code_souce
    except Exception as error_:
        print(f"Erreur lors de la reception du code source : {error_}")


def get_bloc_products_from_category_page(homepage_code_source):
    """
    récuperer le bloc prouduit dans le code source
    :param homepage_code_source:
    :return:
    """
    try:
        bloc_products = homepage_code_source.find_all(
            "article", {"class": "product_pod"}
        )

        return bloc_products
    except Exception as error__:
        print(f"Erreur lors de la reception des produits de la catégorie :{error__}")


def get_url_from_all_categories(homepage_source_code_):
    """
    récupérer les urls des catégories
    :param homepage_source_code_:
    :return:
    """
    category_links_list = []
    try:
        find_category_links_ = homepage_source_code_.find("ul", {"class": "nav nav-list"})
        find_category_links_ = find_category_links_.find_all("li")[1:57]
        for links in find_category_links_:
            category_link = links.find("a")["href"]
            category_link = HOMEPAGE_URL + category_link
            category_links_list.append(category_link)
        return category_links_list
    except Exception as _error:
        print(f"Erreur lors de la reception urls des catégories : {_error}")


def get_source_code_from_category_page(category_url_):
    """
    récupérer les codes sources des pages catégories
    :param category_url_:
    :return:
    """

    try:
        request_get_source_code = requests.get(category_url_)
        category_page_html = BeautifulSoup(request_get_source_code.text, "html.parser")
        return category_page_html
    except Exception as _error_:
        print(f"Erreur lors de la reception du code source : {_error_}")


def get_max_page_to_scrap_of_category(_category_url):
    """
    récupérer toutes les pages en détectant les pages suivantes
    :param _category_url:
    :return:
    """

    max_page = 1  # Par défaut, nous avons une seule page à scrap.

    request_get_source_code = requests.get(_category_url)
    CATEGORY_PAGE_HTML_ = BeautifulSoup(request_get_source_code.text, "html.parser")

    txt_max_pages = CATEGORY_PAGE_HTML_.find("li", {"class": "current"})
    if txt_max_pages is not None:  # Si il trouve le bloc de textes : "page 1 sur X"
        get_last_page_str = re.sub("Page 1 of ", "", txt_max_pages.text)
        # On supprime Page 1 of dans notre chaine de caracters. Il reste plus que des espaces et
        # le numéro de la derniere page. On peut donc le convertir en INT,
        # vu qu'il n'y a plus de lettre
        max_page = int(get_last_page_str)

    return max_page


def scrap_page_of_category(category_url_, total_pages):
    """
    scraper les produits en passant par les pages des catégories
    :param category_url_:
    :param total_pages:
    :return:
    """
    books = []
    i = 0  # On initialise un compteur de boucle
    products_links_list = []
    link_products = CATEGORY_PAGE_HTML.find_all("h3")
    for link in link_products:
        product_link = link.find("a")["href"]
        product_link = product_link.replace(
            "../../../", "https://books.toscrape.com/catalogue/"
        )
        products_links_list.append(product_link)
    while i < total_pages:
        i += 1
        if i != 1:
            page_to_scrap = re.sub("index", f"page-{i}", category_url_)

            print(page_to_scrap)

        try:

            for product_link in products_links_list:
                request_get_source_code = requests.get(str(product_link))
                product_page_html = BeautifulSoup(
                    request_get_source_code.text, "html.parser"
                )

                get_inner_page = product_page_html.find(
                    "div", {"class": "container-fluid page"}
                )
                get_main_bloc = product_page_html.find(
                    "div", {"class": "col-sm-6 product_main"}
                )
                book = [product_link]

                get_title = get_inner_page.find("h1").text
                book.append(get_title)
                get_upc = get_inner_page.find_all("td")[0].text
                book.append(get_upc)
                get_price_incl = get_inner_page.find_all("td")[2].text
                book.append(get_price_incl)
                get_price_excl = get_inner_page.find_all("td")[3].text
                book.append(get_price_excl)

                get_category = (
                    get_inner_page.find("ul", {"class": "breadcrumb"})
                    .find_all("li")[2]
                    .text
                )
                book.append(get_category)
                get_description = get_inner_page.find("p", {"class": ""})
                book.append(get_description)
                get_number = get_inner_page.find_all("td")[5].text
                book.append(get_number)

                class_name = []
                for element in get_main_bloc.find_all(class_="star-rating"):
                    class_name.extend(element["class"])
                    get_ratings = class_name[1] + " out of five"
                    book.append(get_ratings)

                to_get_image = get_inner_page.find(
                    "div", {"class": "item active"}
                ).find("img")
                get_image_url = to_get_image["src"].replace(
                    "../../", "http://books.toscrape.com/"
                )
                book.append(get_image_url)

                os.makedirs("image", exist_ok=True)
                wget.download(
                    get_image_url, out="image"
                )  # télécharge les images de tous les livres du site
                books.append(book)
        except Exception as error__:
            print(f"Erreur sur un bouquin : {error__}")
    # Fonction csv hors de la boucle pour télécharger les informations demandées dans un tableau

    columns = [
        "URL_product",
        "Title",
        "UPC",
        "Price_including_tax",
        "Price_excluding_tax",
        "Category",
        "Description",
        "Number_available",
        "Ratings",
        "Image_URL",
    ]
    with open("book_infos.csv", "a", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerow(columns)
        writer.writerows(books)

    return books


if __name__ == "__main__":
    try:
        HOMEPAGE_URL = "https://books.toscrape.com/"
        homepage_source_code = get_source_code_from_homepage()
        find_category_links = get_url_from_all_categories(homepage_source_code)
        category_urls = find_category_links
        for category_url in category_urls:
            TOTAL_PAGES = get_max_page_to_scrap_of_category(category_url)
            CATEGORY_PAGE_HTML = get_source_code_from_category_page(category_url)
            scrap_page_of_category(category_url, TOTAL_PAGES)
            print(f"Pour l'url {category_url} : je trouve {TOTAL_PAGES} page à scrap  ")

            # print(books_of_category)
    except Exception as error:
        print(f"erreur lors de l'execution du script : {error}")
