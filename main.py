import asyncio
from swapi_async import get_data_from_swapi
from db_async import load_to_db

COUNT = 82
CHUNK_SIZE = 10


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    characters = asyncio.run(get_data_from_swapi(COUNT, CHUNK_SIZE))
    print('Data gathered from API successfully')
    asyncio.run(load_to_db(characters, CHUNK_SIZE))
    print('Data loaded to database successfully')

