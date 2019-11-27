from repositories import product_repository


def get_products_from_place(id_place):
    return product_repository.get_products_from_place(id_place)
