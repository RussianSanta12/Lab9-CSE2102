import uuid
from flask import Flask, request

app = Flask(__name__)

uuid = "e0fd05e6-cfaa-11f0-829e-000d3a8e16b7"

@app.route("/")
def hello():
   return " you called \n"

# curl -d "text=Hello!&param2=value2" -X POST http://localhost:5000/echo
@app.route("/echo", methods=['POST'])
def echo():
   return "You said: " + request.form['text']

# curl -d "uuid=e0fd05e6-cfaa-11f0-829e-000d3a8e16b7" -X POST http://localhost:5000/uuid
@app.route("/uuid", methods=['POST'])
def idcheck():
   myuuid = str(request.form['uuid'])
   if (myuuid == uuid):
      print("Yes")
   else:
      print("uuid check failed") 
   return "done" + uuid

if __name__ == "__main__":
   app.run(debug=True, host='0.0.0.0')