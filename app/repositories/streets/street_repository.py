from app.db import DBConnection
from app.repositories.base_repository import Repository
from app.entities import Street
from app.configs import get_logger

_logger = get_logger(__name__)


class StreetRepository(Repository):

    def __init__(self, connection: DBConnection) -> None:
        super().__init__(connection)

    def insert(self, neighborhood_id: int, name: str) -> Street:
        try:
            query = '''
            INSERT INTO public.streets("name", neighborhood_id)
            VALUES(%(name)s, %(neighborhood_id)s)
            RETURNING id, name, neighborhood_id;
            '''

            raw_street = self.conn.execute(sql_statement=query, values={
                "name": name, "neighborhood_id": neighborhood_id
            })

            if raw_street:
                return Street(**raw_street)

        except Exception as error:
            _logger.error(f"Error: {str(error)}. Data: {dict(name=name)}")

    def select_by_id(self, id: int) -> Street:
        try:
            query = 'SELECT id, "name", neighborhood_id FROM public.streets WHERE id=%(id)s;'

            raw_street = self.conn.execute(sql_statement=query, values={"id": id})

            if raw_street:
                return Street(**raw_street)

        except Exception as error:
            _logger.error(f"Error: {str(error)}. Data: {dict(id=id)}")

    def select_by_name(self, name: str) -> Street:
        try:
            query = 'SELECT id, "name", neighborhood_id FROM public.streets WHERE name=%(name)s;'

            raw_street = self.conn.execute(sql_statement=query, values={"name": name})

            if raw_street:
                return Street(**raw_street)

        except Exception as error:
            _logger.error(f"Error: {str(error)}. Data: {dict(name=name)}")
