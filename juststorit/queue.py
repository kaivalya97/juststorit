from flask import Flask, request, jsonify
from collections import deque
import configparser

app = Flask(__name__)

queue = deque([])


@app.route('/queue', methods=["POST"])
def queueadd():
    if request.method == 'POST':
        global queue  #Access Global Queue
        jsonRes = request.get_json()  #Gets the JSON passed in request
        ##Fetching contents
        # uid=jsonRes['uid']
        # fname=jsonRes['filename']
        # op=jsonRes['op']
        ##Dictionary maintained for each request
        #user_req = {'uid': uid, 'fname': fname, 'op': op}
        ##Each request Dictionary appended in the queue
        queue.append(jsonRes)
        print 'Queue: ', queue
        return str("Success")
    else:
        return str("Fail")


@app.route('/queuepop', methods=["GET"])
def queuepop():
    try:
        if request.method == 'GET':
            global queue  #Access Global Queue
            ##Popping the oldest request
            user_req = queue.popleft()
            print 'Request Popped: ', user_req
            return user_req
        else:
            return str("Fail")
    except IndexError as e:
        return str(101)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8005, debug=True, threaded=True)
