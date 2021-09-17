from scalpr.database.database import DataBase
from scalpr.options import Options

def test_database_init():
    db = DataBase(options=Options())
    assert db.options == Options()