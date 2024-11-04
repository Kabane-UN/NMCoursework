from random import randint

def generate_cities(cities_num: int, max_size: int) -> list[tuple[int]]:
    return [(randint(0, max_size), randint(0, max_size)) for _ in range(cities_num)]

