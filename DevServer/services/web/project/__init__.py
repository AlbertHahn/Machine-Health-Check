from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from random import randrange
import psycopg2



app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)


class Machine(db.Model):
    __tablename__ = "machines"

    id = db.Column(db.Integer, primary_key=True)
    machine = db.Column(db.String(128), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, machine):
        self.machine = machine

def get_machines():

    print("lets go")
    conn = None
    dataset = ()
    try:
        dsn = 'postgresql://hello_flask:hello_flask@db:5432/hello_flask_dev'
        conn = psycopg2.connect(dsn)
        cur = conn.cursor()
        cur.execute("SELECT * FROM machines")
        print("Counter: ", cur.rowcount)
        row = cur.fetchone()

        dataset = row
        while row is not None:
            row = cur.fetchone()

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


    return dataset



@app.route("/",methods=["GET"])
def index():

    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    print("date and time:",date_time)	
    Machinedata = get_machines()
    print(Machinedata)

    Randomnumber = randrange(100)

    data_details = {
        'id': Machinedata[0],
        'machine': Machinedata[1],
        'active': Machinedata[2],
        'currenTime' : date_time,
        'randomNumber' : Randomnumber
    }

    return render_template("index.html", data=data_details)
