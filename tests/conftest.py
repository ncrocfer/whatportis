import pytest
from click.testing import CliRunner
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
from tinydb import TinyDB

import whatportis.db


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def create_ports(tmpdir, monkeypatch):
    def _create_ports(ports):
        def get_db():
            tmp_db = tmpdir.join("db.json")
            db = TinyDB(
                str(tmp_db),
                storage=CachingMiddleware(JSONStorage)
            )

            for port in ports:
                db.insert({
                    'name': port[0],
                    'port': port[1],
                    "description": port[2],
                    "protocol": port[3]
                })
            return db

        return monkeypatch.setattr(whatportis.db, "get_database", get_db)
    return  _create_ports
