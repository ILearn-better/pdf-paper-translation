from flask import Flask, jsonify, request
import time
import threading

app = Flask(__name__)

# 存储任务状态的字典，用于记录任务状态
task_status = {}

# 长时间运行的任务
def long_running_task(task_id):
    task_status[task_id] = "in_progress"
    # 长时间运行的功能
    for i in range(5):
        time.sleep(2)  # 模拟长时间运行
        task_status[task_id] = f"Step {i + 1} completed"
    task_status[task_id] = "completed"

@app.route('/start_long_task', methods=['POST'])
def start_long_task():
    task_id = request.form['task_id']
    # 使用线程来执行长时间运行的任务，避免阻塞主线程
    task_thread = threading.Thread(target=long_running_task, args=(task_id,))
    task_thread.start()
    return jsonify({"message": "Task started"}), 202

@app.route('/get_task_status', methods=['GET'])
def get_task_status():
    task_id = request.args.get('task_id')
    status = task_status.get(task_id, "not_found")
    return jsonify({"status": status})

if __name__ == '__main__':
    app.run(debug=True)
