from sqlalchemy import create_engine

from services.authentication.authHandler import config
db_user = config["DB_USER"]
db_password = config["DB_PASSWORD"]
db_host = config["DB_HOST"]
db_port = int(config["DB_PORT"])
db_database = config["DB_DATABASE"]
db_sslmode = bool(config["DB_SSLMODE"])
db_engine = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}"
create_engine(db_engine)
engine = create_engine(db_engine)
conn = engine.connect()