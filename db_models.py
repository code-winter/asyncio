import asyncio

from sqlalchemy import Integer, String, Column
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import config

Base = declarative_base()

engine = create_async_engine(config.PG_DSN_ALC, echo=True)


class Character(Base):

    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), index=True)
    height = Column(String)
    mass = Column(String)
    hair_color = Column(String)
    skin_color = Column(String)
    eye_color = Column(String)
    birth_year = Column(String)
    gender = Column(String)
    homeworld = Column(String(128))
    films = Column(String(256))
    species = Column(String(128))
    vehicles = Column(String(128))
    starships = Column(String(128))


async def get_session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    async_session_maker = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    return async_session_maker

if __name__ == '__main__':  # для сброса и создания БД
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(get_session())
