#!/usr/bin/python3
# coding: utf8
import requests
from bs4 import BeautifulSoup


# Fonctions avec message d'exception prévu en cas d'erreur
def get_source_code_from_product_page(product_page_url):
    try:
        request_get_source_code = requests.get(product_page_url)
        product_source_code = BeautifulSoup(request_get_source_code.text, "html.parser")

        return product_source_code
    except Exception as error:
        print(f"Erreur lors de la reception du code source : {error}")


# fonctions permettant d'extraire et de transformer le code html sur le principe d'un entonnoire. 

def get_product_main_bloc(product_source_code):
    try:
        product_main_bloc = product_source_code.find('div', {'class': 'col-sm-6 product_main'})

        return product_main_bloc
    except Exception as error:
        print(f"Erreur lors de la reception du code source : {error}")


def get_other_from_inner_page(product_source_code):
    try:
        product_inner_page = product_source_code.find('div', {'class': 'container-fluid page'})

        return product_inner_page
    except Exception as error:
        print(f"Erreur lors de la récupération du code inner :{error}")



def get_title_from_product_page(product_inner_page):
    try:
        product_title = product_inner_page.find('h1')  #  attrs={'class': 'col-sm-6 product_main'})
        print(product_title.text)

        return product_title.text
    except Exception as error:
        print(f"Erreur lors de la récupération du titre du produit : {error}")


def get_price_tax_incl_from_page(product_inner_page):
    try:
        product_price_tax_incl = product_inner_page.find_all('td')[2]

        print(product_price_tax_incl.text)
        return product_price_tax_incl
    except Exception as error:
        print(f"Erreur lors de la récupération du prix avec taxe: {error}")


def get_price_tax_excl_from_page(product_inner_page):
    try:
        product_price_tax_excl = product_inner_page.find_all('td')[3]

        print(product_price_tax_excl.text)
        return product_price_tax_excl
    except Exception as error:
        print(f"Erreur lors de la récupération du prix sans taxe : {error}")


def get_upc_from_page(product_inner_page):
    try:
        product_upc = product_inner_page.find_all('td')[0]
        print(product_upc.text)
        return product_upc
    except Exception as error:
        print(f"Erreur lors de la récupération de la valeur upc : {error}")


def get_number_available_from_page(product_inner_page):
    try:
        product_number_available = product_inner_page.find_all('td')[5]

        print(product_number_available.text)
        return product_number_available
    except Exception as error:
        print(f"Erreur lors de la récupération du nombre disponible :{error}")


def get_rating_from_main_bloc(product_main_bloc):
    try:
        class_name = []
        for element in product_main_bloc.find_all(class_='star-rating'):
            class_name.extend(element["class"])

        print(class_name[1] + " out of five")
        return class_name[1] + " out of five"
    except Exception as error:
        print(f"Erreur lors de la récupération du rating :{error}")


def get_category_from_inner_page(product_inner_page):
    try:
        product_category = product_inner_page.find('ul', {'class': 'breadcrumb'})
        product_category = product_category.find_all('li')[2]

        print(product_category.text)
        return product_category
    except Exception as error:
        print(f"Erreur lors de la récupération de la catégorie :{error}")


def get_description_from_inner_page(product_inner_page):
    try:
        product_description = product_inner_page.find('p', {'class': ''}).text

        print(product_description)
        return product_description
    except Exception as error:
        print(f"Erreur lors de la récupération de la description :{error}")


def get_image_url_from_inner_page(product_inner_page):
    try:
        product_image_url = product_inner_page.find('div', {'class': 'item active'})
        product_image_url = product_image_url.find('img')
        product_image_url = product_image_url['src'].replace('../../', 'http://books.toscrape.com/')

        print(product_image_url)
        return product_image_url
    except Exception as error:
        print(f"Erreur lors de la récupération de l\'url de l'image :{error}")


# Executions du programme

if __name__ == "__main__":
    try:
        product_page_url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
        product_source_code = get_source_code_from_product_page(product_page_url)
        product_main_bloc = get_product_main_bloc(product_source_code)
        product_inner_page = get_other_from_inner_page(product_source_code)

        product_title = get_title_from_product_page(product_main_bloc)
        product_price_tax_incl = get_price_tax_incl_from_page(product_inner_page)
        product_price_tax_excl = get_price_tax_excl_from_page(product_inner_page)
        product_upc = get_upc_from_page(product_inner_page)
        product_number_available = get_number_available_from_page(product_inner_page)
        product_description = get_description_from_inner_page(product_inner_page)
        product_rating = get_rating_from_main_bloc(product_main_bloc)
        product_image_url = get_image_url_from_inner_page(product_inner_page)
        product_category = get_category_from_inner_page(product_inner_page)

    except Exception as error:
        print(f"erreur lors de l'execution du script : {error}")
