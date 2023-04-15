import threading
import time
from flask import Flask, request, jsonify
import os
import queue
import uuid

app = Flask(__name__)
queue = queue.Queue(-1)
list = []

@app.route('/poll', methods=['GET'])
def poll():
    id = request.args.get('id')
    index = None

    for x in range(len(list)):
        if(list[x]["id"] == id):
            index = x
    if index is not None:
        data = list[index]
        if data["status"] == "FINISHED":
            list.remove(data)
        return jsonify(data)
    else:
        return jsonify({
            "error": "id is not found"
        })

@app.route('/separate', methods=['GET'])
def main():
    id = request.args.get('id')
    if(trackExists(id)):
        return jsonify({
            "error": "Similarly named track is already being processed."
        })
    else:
        data = {
            "id": id,
            "status": "QUEUED",
            "vocals": None,
            "no_vocals": None
        }
        queue.put(data)
        list.append(data)
        return jsonify(data)

@app.route('/status', methods=['GET'])
def status():
    status = request.args.get('filter')
    data = []
    
    for item in list:
        info = {
            "id": item["id"],
            "status": item["status"]
        }
        if status == item["status"] or status == "ALL":
            data.append(info)
        
    return jsonify(data)

def trackExists(track):
    for item in list:
        if item["id"] == track:
            return True
        
    return False

def limitReached():
    limit = 2
    counter = 0

    for item in list:
        if item["status"] == "PROCESSING":
            counter+=1

    if counter > limit:
        return True
    
    return False

def process(id, index):
    os.system(f"python3 -m demucs -n htdemucs_ft --out /data/output --two-stems=vocals /data/input/{id}.wav")
    list[index]["vocals"] = os.path.join(os.path.join("htdemucs_ft", "song"), "vocals.wav")
    list[index]["no_vocals"] = os.path.join(os.path.join("htdemucs_ft", "song"), "no_vocals.wav")
    status = "FINISHED"
    list[index]["status"] = status

def process_queue():
    while(True):
        if limitReached():
            time.sleep(3)
        else:
            data = queue.get()

            id = data["id"]
            status = data["status"]
            index = None

            for x in range(len(list)):
                if(list[x]["id"] == id):
                    index = x

            if index is not None:
                status = "PROCESSING"
                list[index]["status"] = status
                process_thread = threading.Thread(target=process, args=(id, index), name=f"process-demucs-{id}")
                process_thread.start()


if __name__ == "__main__":
    processing_thread = threading.Thread(target=process_queue, name=f"demucs-queue")
    processing_thread.start()
    app.run(port=5001, host='0.0.0.0')