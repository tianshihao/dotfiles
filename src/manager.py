from .log_helper import *
import platform

from .models import ActionDesc
from .worker import Worker

class Manager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Manager, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, 'initialized'):  # Prevents re-initialization
            self.platform: str = platform.system()
            self.worker = Worker(self.platform)
            self.initialized = True  # Mark as initialized

    def retrieve_from_host(self) -> None:
        self.worker.filter()
        self.worker.run('path_on_host', 'path_in_repo', ActionDesc.RETRIEVE)

    def dispatch_to_host(self) -> None:
        self.worker.run('path_in_repo', 'path_on_host', ActionDesc.DISPATCH)

    def validate(self) -> None:
        self.worker.run('path_in_repo', 'path_on_host', ActionDesc.VALIDATE)
