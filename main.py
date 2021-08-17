from flask import Flask, jsonify, request, json

#Characters which might cause sql injection
injection = ['\'','1=1','""=""']

app = Flask(__name__)

@app.route("/v1/sanitized/input/",methods=['POST'])
def index():    
    if request.method=='POST':
        data_string = request.get_data()
        try:
            data = json.loads(data_string)
        except Exception as e:
            return str(e)

        if len(data) :
            if validate(data):
                return jsonify({'result':'sanitized'})
            return jsonify({'result':'unsanitized'})
        else:
            return 'Bad Request', 400
    
    return "Method not allowed"
    
def validate(data):
    for key in data:
        value = str(data[key])
        for char in injection:
            if char in key.split() or char in value.split():
                return False
        return True

 
@app.route("/")
def hello_world():
    return "<b>Hello, World!</b>"

if __name__=="__main__":
    app.run(debug=True)
