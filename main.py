from flask import Flask, jsonify, request, json, render_template
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
mysql = MySQL(app)

#Characters which might cause sql injection
injection = ['\'','1=1','""=""','true','/*','*/','+','||','admin\'--',";","') or ('1'='1--","' or 1=1#","' or 1=1--","admin' #"]

@app.route("/v1/sanitized/input/",methods=['GET','POST'])
def index():    
    if request.method=='POST':
        data_string = request.get_data()
        try:
            data = json.loads(data_string)
        except Exception as e:
            return str(e)

    
        if len(data) : 
            if validate(data):
                cur = mysql.connection.cursor()
                for key in data:
                    resultValue = cur.execute("SELECT name,password FROM users where name=%s and password=%s",(key,data[key]))
                cur.close()
                return jsonify({'result':'sanitized'})
            return jsonify({'result':'unsanitized'})
        else:
            return 'Bad Request', 400
    else:
        cur = mysql.connection.cursor()
        resultValue = cur.execute("SELECT * FROM users")
        if resultValue > 0:
            userDetails = cur.fetchall()
            return render_template('users.html',userDetails=userDetails)
    
def validate(data):
    
    for key in data:
        value = str(data[key])
        for char in injection:
            if str(char) in key or char in value:
                return False
        return True

 
@app.route("/")
def hello_world():
    return "<b>Hello, World!</b>"

if __name__=="__main__":
    app.run(debug=True)
