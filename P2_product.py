#!/usr/bin/python3
# coding: utf8
import requests
from bs4 import BeautifulSoup


# Fonctions avec message d'exception prévu en cas d'erreur
def get_source_code_from_product_page():
    """
    récuperer le source code
    :return:
    """
    try:
        request_get_source_code = requests.get(PRODUCT_PAGE_URL)
        product_source_code_ = BeautifulSoup(request_get_source_code.text, "html.parser")

        return product_source_code_
    except Exception as _error:
        print(f"Erreur lors de la reception du code source : {_error}")


# fonctions permettant d'extraire et de transformer le code html sur le principe d'un entonnoire.


def get_product_main_bloc(product_source_code_):
    """
récupérer spécifiquement le bloc du haut dans le code html
    :param product_source_code_:
    :return:
    """
    try:
        product_main_bloc_ = product_source_code_.find(
            "div", {"class": "col-sm-6 product_main"}
        )

        return product_main_bloc_
    except Exception as error_:
        print(f"Erreur lors de la reception du code source : {error_}")


def get_other_from_inner_page(_product_source_code):
    """
    récupérer le bloc inner du code html
    :param _product_source_code:
    :return:
    """
    try:
        product_inner_page_ = product_source_code.find(
            "div", {"class": "container-fluid page"}
        )

        return product_inner_page_
    except Exception as _error_:
        print(f"Erreur lors de la récupération du code inner :{_error_}")


def get_title_from_product_page(product_inner_page__):
    """
    récupérer le titre du livre
    :param product_inner_page__:
    :return:
    """
    try:
        product_title_ = product_inner_page__.find(
            "h1"
        )
        print(product_title_.text)

        return product_title_.text
    except Exception as error_title:
        print(f"Erreur lors de la récupération du titre du produit : {error_title}")


def get_price_tax_incl_from_page(_product_inner_page_):
    """
    récupérer le prix taxe inclus
    :param _product_inner_page_:
    :return:
    """
    try:
        product_price_tax_incl_ = _product_inner_page_.find_all("td")[2]

        print(product_price_tax_incl_.text)
        return product_price_tax_incl_
    except Exception as error_priceincl:
        print(f"Erreur lors de la récupération du prix avec taxe: {error_priceincl}")


def get_price_tax_excl_from_page(product_inner_page__):
    """
    récupérer le prix taxe exclu
    :param product_inner_page__:
    :return:
    """
    try:
        product_price_tax_excl_ = product_inner_page__.find_all("td")[3]

        print(product_price_tax_excl_.text)
        return product_price_tax_excl_
    except Exception as error_priceexcl:
        print(f"Erreur lors de la récupération du prix sans taxe : {error_priceexcl}")


def get_upc_from_page(product_inner__page):
    """

    :param product_inner__page:
    :return:
    """
    try:
        product_upc_ = product_inner__page.find_all("td")[0]
        print(product_upc_.text)
        return product_upc_
    except Exception as error_upc:
        print(f"Erreur lors de la récupération de la valeur upc : {error_upc}")


def get_number_available_from_page(__product_inner_page):
    """
    récupérer le nombre disponible
    :param __product_inner_page:
    :return:
    """
    try:
        product_number_available_ = product_inner_page.find_all("td")[5]

        print(product_number_available_.text)
        return product_number_available_
    except Exception as error_number:
        print(f"Erreur lors de la récupération du nombre disponible :{error_number}")


def get_rating_from_main_bloc(_product_main_bloc):
    """
    récupérer le rating du livre
    :param _product_main_bloc:
    :return:
    """
    try:
        class_name = []
        for element in product_main_bloc.find_all(class_="star-rating"):
            class_name.extend(element["class"])

        print(class_name[1] + " out of five")
        return class_name[1] + " out of five"
    except Exception as error_rating:
        print(f"Erreur lors de la récupération du rating :{error_rating}")


def get_category_from_inner_page(product__inner_page):
    """
    récupérer la catégorie
    :param product__inner_page:
    :return:
    """
    try:
        product_category_ = product__inner_page.find("ul", {"class": "breadcrumb"})
        product_category_ = product_category_.find_all("li")[2]

        print(product_category_.text)
        return product_category_
    except Exception as error_category:
        print(f"Erreur lors de la récupération de la catégorie :{error_category}")


def get_description_from_inner_page(product__inner__page):
    """
    récupérer la description
    :param product__inner__page:
    :return:
    """
    try:
        product_description_ = product__inner__page.find("p", {"class": ""}).text

        print(product_description_)
        return product_description_
    except Exception as error_description:
        print(f"Erreur lors de la récupération de la description :{error_description}")


def get_image_url_from_inner_page(_product_inner_page_):
    """

    :param _product_inner_page_:
    :return:
    """
    try:
        product_image_url_ = product_inner_page.find("div", {"class": "item active"})
        product_image_url_ = product_image_url_.find("img")
        product_image_url_ = product_image_url_["src"].replace(
            "../../", "http://books.toscrape.com/"
        )

        print(product_image_url_)
        return product_image_url_
    except Exception as error_image:
        print(f"Erreur lors de la récupération de l'url de l'image :{error_image}")


# Executions du programme

if __name__ == "__main__":
    try:
        PRODUCT_PAGE_URL = (
            "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
        )
        product_source_code = get_source_code_from_product_page()
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
