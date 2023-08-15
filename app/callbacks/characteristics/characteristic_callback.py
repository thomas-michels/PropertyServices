from app.callbacks.callback_interface.callback_base import Callback
from app.db import DBConnection
from app.dependencies.worker.utils.event_schema import EventSchema
from app.dependencies.worker import KombuProducer
from app.configs import get_environment
import requests
from requests.exceptions import HTTPError

_env = get_environment()


class CharacteristicCallback(Callback):

    def __init__(self, conn: DBConnection) -> None:
        super().__init__(conn)

    def handle(self, message: EventSchema) -> bool:
        ...
