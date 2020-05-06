import json
import psycopg2
from psycopg2.extras import RealDictCursor

from app import app

db_user = app.config['DB_USER']
db_password = app.config['DB_PASSWORD']
db_host = app.config['DB_HOST']
db_name = app.config['DB_NAME']

def execute_query(sql):
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port="5432")
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(sql)
    res=cur.fetchall()

    ## dump result into json
    # d = json.dumps(res, indent=2, default=str)
    # l = json.loads(d)
    return res

def execute_change(sql):
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port="5432")
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(sql)
    conn.commit()

    ## dump result into json
    # d = json.dumps(res, indent=2, default=str)
    # l = json.loads(d)
    return 'deleted'