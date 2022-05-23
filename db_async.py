import asyncio
import asyncpg
from more_itertools import chunked
import config


def get_values(char_list):  # пришлось вручную задать порядок, т.к. значения могут быть не по порядку
    values = []
    ids = []
    for person in char_list:
        if person.get('name'):
            data = (
                int(person['id']), person['name'], person['height'], person['mass'], person['hair_color'],
                person['skin_color'], person['eye_color'], person['birth_year'], person['gender'], person['homeworld'],
                person['films'], person['species'], person['vehicles'], person['starships']
            )
            ids.append(int(person['id']))
            values.append(data)
        else:  # failsafe для недоступных персонажей (https://swapi.dev/api/people/17/ к примеру)
            data = ((ids[-1] + 1), 'Not Found', '', '', '', '', '', '', '', '', '', '', '', '')
            values.append(data)
    return values


async def insert_chars(pool, values):
    query = '' \
            'INSERT INTO characters (' \
            'id, name, height, mass, hair_color, skin_color, eye_color,' \
            ' birth_year, gender, homeworld, films, species, vehicles, starships' \
            ') VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)'
    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.executemany(query, values)


async def load_to_db(char_list, chunk_size):
    pool = await asyncpg.create_pool(config.PG_DSN, min_size=20, max_size=20)
    coroutines = []
    for chars_chunked in chunked(char_list, chunk_size):
        values = get_values(chars_chunked)
        coroutines.append(asyncio.create_task(insert_chars(pool, values)))
    await asyncio.gather(*coroutines)
    await pool.close()




