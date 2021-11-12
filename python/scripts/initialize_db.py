"""Initialize Database"""
from edgar_filing_searcher.api import create_app
from edgar_filing_searcher.database import db


def init_db():
    app = create_app()
    app.app_context().push()
    conn = db.engine.connect()
    create_extension_pg_trgm = db.text("CREATE EXTENSION IF NOT EXISTS pg_trgm")
    create_extension_btree_gin = db.text("CREATE EXTENSION IF NOT EXISTS btree_gin")
    conn.execute(create_extension_btree_gin)
    conn.execute(create_extension_pg_trgm)
    db.create_all()


if __name__ == '__main__':
    init_db()
