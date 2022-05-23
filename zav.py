import serial
from threading import Lock
from flask import Flask, render_template, session, request, jsonify, url_for
from flask_socketio import SocketIO, emit, disconnect
import time
import MySQLdb
import configparser as ConfigParser

ser = serial.Serial("/dev/ttyUSB0", 9600) # ser.baudrate = 9600

async_mode = None
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

# DATABASE CONFIG
config = ConfigParser.ConfigParser()
config.read('config.cfg')
myhost = config.get('mysqlDB', 'host')
myuser = config.get('mysqlDB', 'user')
mypasswd = config.get('mysqlDB', 'passwd')
mydb = config.get('mysqlDB', 'db')
print(myhost)

def background_thread(args):
    count = 0
    dataList = []
    db = MySQLdb.connect(host=myhost,user=myuser,passwd=mypasswd,db=mydb)
    while True:
        if args:
          A = dict(args).get('A')
          btnV = dict(args).get('btn_value')
          dbV = dict(args).get('db_value')
        else:
          A = 1
          btnV = 'null'
          dbV = 'nieco'
        socketio.sleep(2)
        print(A)
        print(btnV)
        print(dbV)
        if btnV == "start":
            count += 1
            print("start")

            read_ser = ser.readline()
            hodnoty = read_ser.decode()
            vlhkost = hodnoty[0:5]
            teplota = hodnoty[6:11]
            relTeplota = hodnoty[12:17]
            print(hodnoty)

            dataDict = {
                "t": time.time(),
                "x": count,
                "vlhkost": vlhkost,
                "teplota": teplota}
            dataList.append(dataDict)
            if len(dataList)>0:
                write = str(dataList).replace("'", "\"")
                # print(write)
                # write2file(write)
                socketio.emit('my_response',
                            {'data': dataDict, 'count': count},
                            namespace='/test')
        else:
            print("STOP")

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@app.route('/tabs')
def tabs():
    return render_template('tabs.html', async_mode=socketio.async_mode)

@app.route('/graphlive', methods=['GET', 'POST'])
def graphlive():
    return render_template('graphlive.html', async_mode=socketio.async_mode)

@socketio.on('my_event', namespace='/test')
def test_message(message):   
    session['receive_count'] = session.get('receive_count', 0) + 1 
    session['A'] = message['value']
    emit('my_response',
         {'data': message['value'], 'count': session['receive_count']})

@socketio.on('db_event', namespace='/test')
def db_message(message):
    session['db_value'] = message['value']

@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()

@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread, args=session._get_current_object())
    emit('my_response', {'data': 'Connected', 'count': 0})

@socketio.on('click_event', namespace='/test')
def db_message(message):
    session['btn_value'] = message['value']

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)

@socketio.on('click_event', namespace='/test')
def db_message(message):
    session['btn_value'] = message['value']

# DB routes
@app.route('/db')
def db():
  db = MySQLdb.connect(host=myhost,user=myuser,passwd=mypasswd,db=mydb)
  cursor = db.cursor()
  # cursor.execute('''SELECT  hodnoty FROM  graph WHERE id=1''')
  cursor.execute('''SELECT * FROM monitoring''')
  rv = cursor.fetchall()
  return str(rv)

@app.route('/dbadd/<string:insertTemp>/<string:insertHum>')
def add(insertTemp, insertHum):
  db = MySQLdb.connect(host=myhost,user=myuser,passwd=mypasswd,db=mydb)
  cursor = db.cursor()
  cursor.execute("SELECT MAX(id) FROM monitoring")
  maxid = cursor.fetchone() 
  print(maxid[0]+1)
  print(insertTemp)
  cursor.execute("INSERT INTO monitoring (id, temperature, humidity) VALUES (%s,%s,%s)",(maxid[0]+1,insertTemp,insertHum))
  db.commit()
  return "Done"

@app.route('/dbdata/<int:num>', methods=['GET', 'POST'])
def dbdata(num):
  db = MySQLdb.connect(host=myhost,user=myuser,passwd=mypasswd,db=mydb)
  cursor = db.cursor()
  print(num)
  cursor.execute("SELECT humidity, temperature FROM monitoring WHERE id=%s", num)
  rv = cursor.fetchone()
  print(rv)
  return str(rv[0])


# FILES
@app.route('/write')
def write2file(val):
    # print(val)
    fo = open("static/files/output.txt","a+")
    fo.write("%s\r\n" %val)
    return "done"

@app.route('/read/<string:num>')
def readmyfile(num):
    fo = open("static/files/output.txt","r")
    rows = fo.readlines()
    return rows[int(num)-1]

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)