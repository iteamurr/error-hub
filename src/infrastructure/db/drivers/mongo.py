from pymongo import ASCENDING, MongoClient
from pymongo.collection import Collection

import src.infrastructure.config.config as app_config


class MongoDriver:
    def __init__(self, cfg: app_config.MongoConfig = app_config.MongoConfig()) -> None:
        self.client = MongoClient(cfg.URI, **cfg.WRITE_CONCERN)
        self.db = self.client[cfg.DB_NAME]
        self.collection = self.db[cfg.COLL_NAME]

        self._ensure_indexes()

    def _ensure_indexes(self) -> None:
        self.collection.create_index(
            [("hash", ASCENDING)],
            name="idx_hash",
            background=True,
        )
        self.collection.create_index(
            [("header.$**", ASCENDING)],
            name="idx_header_wild",
            background=True,
        )
        self.collection.create_index(
            [("body.$**", ASCENDING)],
            name="idx_body_wild",
            background=True,
        )

    def get_collection(self) -> Collection:
        return self.collection
