from flask import Flask, request, render_template, jsonify

import psycopg2
from configparser import ConfigParser

import json


app = Flask(__name__)



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
        # display the PostgreSQL database server version
        #result = cur.fetchall()
        #print(result)
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
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print('POST: input uid & pwd: %s, %s' % (username,password))

    else:#call example: http://127.0.0.1:3361/login?username=flsak&password=12346 #
     
        username = request.args.get('username')#
        
        password = request.args.get('password')#
        print('GET: input uid & pwd: %s, %s' % (username,password))#
        
    return 'Hello ' + username + password + '!'



# @app.route('/realtimesignal', methods=['GET', 'POST'])
@app.route('/query', methods=['GET', 'POST'])
def realtimesignal():
    if request.method == 'POST':
        # grafana_name = request.form['channel']
        # value = request.form['value']
        # print('POST: channel=%s' % (channel))


        # --- ADDITONAL CODE ---
        obj_req = request.get_json(silent=True)	# get post json
        print("POST request")
        print(obj_req)

        if obj_req == None:
            return jsonify({
                'EXEC_DESC': '62',
                'message': 'request body is wrong'
            }), 400

        # process grafana request
        try:
            req_param = obj_req['targets'][0]['target']
            req_param = req_param.replace("\"", "") # replace " to 
            req_param = req_param.replace("'", "\"")    # replace ' to "
            req_param = json.loads(req_param)

        except Exception as e:
            print({'msg': str(e)})
            return jsonify({'msg': str(e)}), 500
        
        
        print("request param")
        print(req_param)


        # get value from request param
        try:
            grafana_name = req_param['channel']
            value = req_param['value']
            print("channel: " + grafana_name)
            print("value: " + value)
        except Exception as e:
            print({'msg': str(e)})
            return jsonify({'msg': str(e)}), 500

        # --- -------- ---

    else:#call example: http://127.0.0.1:3361/realtimesignal?channel=TPM K1
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



@app.route("/search", methods=['GET','POST'])
def search():
    """
    for simple json
    
    controller for firehose write in this function.
    """
    str_msg = 'test simple json with /search'

    return jsonify({'msg': str_msg}), 200




if __name__ == '__main__':
   app.run(host='0.0.0.0',port=8080,debug=True)
