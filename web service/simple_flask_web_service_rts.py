#import flask 這個套件
from flask import Flask, request, render_template
app = Flask(__name__)


#使用模塊的connect()功能psycopg2
import psycopg2
#以下config()函數讀取database.ini文件並返回連接參數
from configparser import ConfigParser

#以下config()函數讀取database.ini文件並返回連接參數
def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
 
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
 
    return db
 
def connect(channel_name,value=1):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
 
        # create a cursor
        cur = conn.cursor()
        
        # execute a statement
        print('update realtime_web_service table:')
        #PG SQL 語法
        #clear all to 0
        SQL = 'UPDATE realtime_web_service.realtime_web_service SET "IfUse" = \'{0}\''.format(0)
        print(SQL)
        cur.execute(SQL)
        conn.commit()
        #update specific channel
        SQL = 'UPDATE realtime_web_service.realtime_web_service SET "IfUse" = \'{0}\' WHERE "channelID" = \'{1}\''.format(value,channel_name)
        print(SQL)
        cur.execute(SQL)        
        conn.commit()
        #SQL = "SELECT * FROM realtime_web_service.realtime_web_service WHERE channel_name='%s'" % (channel_name)
        #print('perform checking: %s' % SQL)
        cur.execute(SQL)
        #cur.execute("SELECT * FROM realtime_web_service.realtime_web_service WHERE channel_name='TPM K1廢氣風扇(西) 背輥/工輥 驅動側軸承'")
        # display the PostgreSQL database server version
        #result = cur.fetchall()
        #print(result)
        #print([n.name for n in cur.description]) #找出欄位名稱
        # close the communication with the PostgreSQL
        print('perform close & commit:')
        cur.close()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
 
#I just want to be able to manipulate the parameters
#使用者輸/login 如果等於post執行下列 def login
@app.route('/login', methods=['GET', 'POST'])
def login():
    #確認是否為POST
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print('POST: input uid & pwd: %s, %s' % (username,password))

    else:#call example: http://127.0.0.1:3361/login?username=flsak&password=12346 #確認是否直接輸入http網址
     
        username = request.args.get('username')#讀取username值
        
        password = request.args.get('password')#讀取password值
        print('GET: input uid & pwd: %s, %s' % (username,password))#列印出GET:input 於DOS畫面
        
    return 'Hello ' + username + password + '!'#於網頁上顯示出結果

@app.route('/realtimesignal', methods=['GET', 'POST'])
def realtimesignal():
    if request.method == 'POST':
        grafana_name = request.form['channel']
        value = request.form['value']
        print('POST: channel=%s' % (channel))
    else:#call example: http://127.0.0.1:3361/realtimesignal?channel=TPM K1廢氣風扇(西) 背輥/工輥 驅動側軸承&value=1
        grafana_name = request.args.get('channel')
        value = request.args.get('value')
        print('GET: channel=%s' % (grafana_name))
        if grafana_name is None:  return render_template('realtimesignal.html')
    
    value = 1 if value is None else value
    connect(grafana_name,value)
    
    return 'give signal ' + grafana_name + '!'
    
@app.route('/')
def hello_world():
    return render_template('hello.html')
    #return 'Hello World'

if __name__ == '__main__':
   app.run(host='0.0.0.0',port=3361,debug=True)