from flask import Flask, jsonify, request

#Characters which might cause sql injection
injection = ['\'','1=1','""=""']

app = Flask(__name__)

@app.route("/v1/sanitized/input/",methods=['POST'])
def index():    
    if request.method=='POST':
        
        payload = request.get_json()

        if validate(payload):
            return jsonify({'result':'sanitized'})
        
        return jsonify({'result':'unsanitized'})
    else:
        return jsonify({"error":'method not allowed'})

def validate(payload):
    for key in payload:
        value = str(payload[key])
        for char in injection:
            if char in key.split() or char in value.split():
                return False
        return True

 
@app.route("/")
def hello_world():
    return "<b>Hello, World!</b>"

if __name__=="__main__":
    app.run(debug=True)