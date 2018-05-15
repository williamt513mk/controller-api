from flask import Flask, request, render_template
app = Flask(__name__)
import updata_database

#I just want to be able to manipulate the parameters
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print('POST: input uid & pwd: %s, %s' % (username,password))

    else:#call example: http://127.0.0.1:3361/login?username=flsak&password=12346 
     
        username = request.args.get('username')
        
        password = request.args.get('password')
        print('GET: input uid & pwd: %s, %s' % (username,password))
        
    return 'Hello ' + username + password + '!'

@app.route('/realtimesignal', methods=['GET', 'POST'])
def realtimesignal():
    if request.method == 'POST':
        grafana_name = request.form['channel']
        value = request.form['value']
        print('POST: channel=%s' % (channel))
    else:#call example: http://127.0.0.1:3361/realtimesignal?channel=TPM K1
        grafana_name = request.args.get('channel')
        value = request.args.get('value')
        print('GET: channel=%s' % (grafana_name))
        if grafana_name is None:  return render_template('realtimesignal.html')
    
    value = 1 if value is None else value
    updata_database.connect(grafana_name,value)
    
    return 'give signal ' + grafana_name + '!'
    
@app.route('/')
def hello_world():
    return render_template('hello.html')
    #return 'Hello World'

if __name__ == '__main__':
   app.run(host='0.0.0.0',port=3361,debug=True)
