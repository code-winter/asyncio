import aiohttp
import asyncio
from more_itertools import chunked

URL = 'https://swapi.dev/api/people/'


async def get_person(person_id, session):
    async with session.get(f'{URL}{person_id}') as response:
        person_data = await response.json()
        return person_data


async def get_vehicle(url, session):
    async with session.get(url) as response:
        data = await response.json()
        return data['name']


async def get_species(url, session):
    async with session.get(url) as response:
        data = await response.json()
        return data['name']


async def get_films(url, session):
    async with session.get(url) as response:
        data = await response.json()
        return data['title']


async def get_starships(url, session):
    async with session.get(url) as response:
        data = await response.json()
        return data['name']


def clean_character_data(char_list):
    for person in char_list:
        if person.get('name'):
            person_id = person['url'].split(URL)[-1].strip('/')
            person.setdefault('id', person_id)
            person.pop("created")
            person.pop("edited")
            person.pop("url")
    return char_list


async def get_data_from_swapi(count, chunk_size):
    id_range = range(1, count+1)
    characters_list = []
    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        for chunk_ids in chunked(id_range, chunk_size):
            coroutines = [get_person(person_id, session) for person_id in chunk_ids]
            characters = await asyncio.gather(*coroutines)
            for person in characters:
                if person.get('name'):  # пропускаем недоступных персонажей
                    coros = [get_vehicle(url, session) for url in person['vehicles']]
                    vehicles = await asyncio.gather(*coros)
                    person['vehicles'] = ','.join(vehicles)
                    coros = [get_species(url, session) for url in person['species']]
                    species = await asyncio.gather(*coros)
                    person['species'] = ','.join(species)
                    coros = [get_starships(url, session) for url in person['starships']]
                    starships = await asyncio.gather(*coros)
                    person['starships'] = ','.join(starships)
                    coros = [get_films(url, session) for url in person['films']]
                    films = await asyncio.gather(*coros)
                    person['films'] = ','.join(films)
            characters_list.append(clean_character_data(characters))
        all_chars = []
        for char_slice in characters_list:  # сшиваем обратно вложенные списки в один список
            for char in char_slice:
                all_chars.append(char)
        return all_chars
