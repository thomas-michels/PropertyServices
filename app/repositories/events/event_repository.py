from app.db import DBConnection
from app.repositories.base_repository import Repository
from app.dependencies.worker.utils.event_schema import EventSchema
from app.configs import get_logger
import datetime
from json import dumps

_logger = get_logger(__name__)

def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


class EventRepository(Repository):

    def __init__(self, connection: DBConnection) -> None:
        super().__init__(connection)

    def insert(self, event: EventSchema) -> None:
        try:
            query = '''
            INSERT INTO public.events
            (id, created_at, updated_at, sent_to, payload, origin)
            VALUES(%(id)s, %(created_at)s, %(updated_at)s, %(sent_to)s, %(payload)s, %(origin)s)
            RETURNING 1;
            '''
            self.conn.execute(sql_statement=query, values={
                "id": event.id,
                "created_at": event.created_at,
                "updated_at": event.updated_at,
                "sent_to": event.sent_to,
                "payload": dumps(event.payload, default=default),
                "origin": event.origin,
            })
            self.conn.commit()

        except Exception as error:
            _logger.error(f"Error: {str(error)}. Data: {event.model_dump_json()}")
