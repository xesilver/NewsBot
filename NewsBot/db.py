from config import host, port, user, password, db_name
import aiomysql


class DbConnection:
    '''
    Class which allows to perform connection to a database and interact with it.
    '''

    def __init__(self):
        self.pool = None

    async def create_pool(self) -> None:
        '''
        Creates a connection pool to the database.
        '''
        try:

            self.pool = await aiomysql.create_pool(
                host=host,
                port=port,
                user=user,
                password=password,
                db=db_name,
                cursorclass=aiomysql.cursors.DictCursor,
                minsize=1,
                maxsize=10
            )

        except Exception as ex:
            print(f'An error occurred in method create_pool() in db.py \n{ex}')

    async def delete_news(self, paper_name: str) -> None:
        '''
        Deletes all news from the table of a paper you provide in a variable `paper_name`.
        '''

        try:
            async with self.pool.acquire() as connenction:
                async with connenction.cursor() as cursor:
                    delete_query = f'TRUNCATE TABLE {paper_name}'
                    await cursor.execute(delete_query)
                    await connenction.commit()

        except Exception as ex:
            print(f'An error occurred in method delete_news() in db.py \n{ex}')

    async def update_news(self, paper_name: str, news: list) -> None:
        '''
        Replaces news in a table of a paper you provide in a variable `paper_name`,
        on relevant news which you provide in a variable `news`.
        '''

        try:
            async with self.pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    delete_query = f'TRUNCATE TABLE {paper_name}'
                    await cursor.execute(delete_query)
                    await connection.commit()

                    for section in news:
                        insert_query = f'INSERT INTO {paper_name} (article, link) VALUES (%s, %s);'
                        await cursor.execute(insert_query, (section[0], section[1]))
                    await connection.commit()

        except Exception as ex:
            print(f'An error occurred in method update_news() in db.py \n{ex}')

    async def get_news(self, paper_name: str) -> list:
        '''
        Allows to receive news from the table of a paper you provide in a variable `paper_name`.
        '''

        try:
            async with self.pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    select_query = f'SELECT * FROM {paper_name}'
                    await cursor.execute(select_query)
                    rows = await cursor.fetchall()
                    return rows

        except Exception as ex:
            print(f'An error occurred in method get_news() in db.py \n{ex}')
