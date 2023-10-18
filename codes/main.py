from flask import Flask, jsonify, request
from databases import databases

app = Flask(__name__)

@app.route("/api/createUser", methods=["POST"])
def createUser():
    databaseObj = databases()
    
    username = request.values["username"]
    password = request.values["password"]

    result = databaseObj.createUser(username, password)

    print(result)

    if(result):
        return jsonify({"success": 1, "message": "Operation successful!!"})

    return jsonify({"success": 0, "message": "There is a registered user with this username!!"})

@app.route("/api/getToken", methods=["POST"])
def getToken():
    databaseObj = databases()
    
    username = request.values["username"]
    password = request.values["password"]

    result = databaseObj.getToken(username, password)

    if not result:
        return jsonify({"success": 0, "message": "The login information is incorrect!"})
    
    return jsonify({"success": 1, "message": "Operation successful!!","token": result})

@app.route("/api/checkMd5", methods=["POST"])
def checkMd5():
    databaseObj = databases()
    
    token = request.values["token"]
    md5 = request.values["md5"]
    
    result = databaseObj.checkMd5(token, md5)

    if result == token:
        return jsonify({"success": 0, "message": "Token invalid"})

    if result:
        return jsonify({"success": 1, "message": "The file is infected!", "file_infected": 1})

    return jsonify({"success": 1, "message": "The file is clean", "file_infected": 0})
        
   
if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5000)
