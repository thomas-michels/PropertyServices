from app.callbacks.callback_interface.callback_base import Callback
from app.db import DBConnection
from app.dependencies import RedisClient
from app.dependencies.worker.utils.event_schema import EventSchema
from app.dependencies.worker import KombuProducer
from app.composers import property_composer
from app.configs import get_logger, get_environment
from datetime import datetime

_logger = get_logger(__name__)
_env = get_environment()


class InactivePropertyCallback(Callback):

    def __init__(self, conn: DBConnection, redis_conn: RedisClient) -> None:
        super().__init__(conn, redis_conn)
        self.__property_services = property_composer(connection=self.conn, redis_connection=self.redis_conn)

    def handle(self, message: EventSchema) -> bool:
        url = message.payload["property_url"]
    
        property_in_db = self.__property_services.search_by_url(url=url)

        if property_in_db:
            self.__property_services.delete(id=property_in_db.id)
            _logger.info(f"Property deleted with id={property_in_db.id}")

        new_message = EventSchema(
            id=message.id,
            origin=message.sent_to,
            sent_to=_env.PROPERTY_OUT_CHANNEL,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        KombuProducer.send_messages(conn=self.conn, message=new_message)

        return True
