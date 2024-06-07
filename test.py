from sqlalchemy import create_engine, MetaData

engine = create_engine('sqlite:///celerydb.sqlite')
metadata = MetaData(bind=engine)
metadata.create_all()