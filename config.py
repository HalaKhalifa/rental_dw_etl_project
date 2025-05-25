from sqlalchemy import create_engine

# Connection strings (adjust user/pw as needed)
MYSQL_USER = "root"
MYSQL_PW = "newroot"
SOCKET_PATH = "/tmp/mysql.sock"

SRC_DB = "rental_dw"
STAR_DB = "rental_dw_star"

SRC_CONN_STRING = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PW}@localhost/{SRC_DB}?unix_socket={SOCKET_PATH}"
STAR_CONN_STRING = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PW}@localhost/{STAR_DB}?unix_socket={SOCKET_PATH}"

engine_src = create_engine(SRC_CONN_STRING)
engine_star = create_engine(STAR_CONN_STRING)