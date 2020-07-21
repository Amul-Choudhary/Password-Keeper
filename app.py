from flask import Flask, render_template, request, jsonify
import database as db

app = Flask(__name__)

@app.route('/app/user', methods=['POST'])
def register():
    details = request.form.to_dict()
    # print(details)
    user = details['username']
    password = details['password']

    status = 'exisiting account'
    if (db.register(user, password)):
        status = 'account created'

    print(status)

    return jsonify({'status': status})

@app.route('/app/user/auth', methods=['POST'])
def login():
    details = request.form.to_dict()
    # print(details)
    user = details['username']
    password = details['password']

    response = {'status': 'failure'}
    uid = db.login(user, password)
    if (uid):
        response['status'] = 'success'
        response['userId'] = uid

    return jsonify(response)


"""
CAN IMPLEMENT SESSION TRACKING HERE TO GET USER ID
FROM A SECURED SESSION VARIABLE TO AVOID ACCESS TO
OTHER USERS EVEN WHEN KNOWING THE UserId

CURRENTLY NOT IMPLEMENTED TO ALLOW AUTOMATED TEST
CASES TO BE PERFORMED ON THIS API SERVER
"""
@app.route('/app/sites/list/', methods=['GET'])
def getPasswordsList():
    uid = int(request.args.get('user'))

    return jsonify(db.getPasswords(uid))

@app.route('/app/sites', methods=['POST'])
def savePassword():
    uid = int(request.args.get('user'))

    details = request.form.to_dict()
    # print(details)
    user = details['username']
    password = details['password']
    website = details['website']

    status = 'failure'
    if (db.storePassword(uid, website, user, password)):
        status = 'success'

    return jsonify({'status': status})

if __name__ == '__main__':
    app.run('127.0.0.1', 8080)