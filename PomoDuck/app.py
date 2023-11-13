from flask import Flask, render_template, jsonify
import time
import threading

app = Flask(__name__, static_url_path=="/static")


def pomodoro_timer(minutes):
    try:
        time.sleep(minutes * 60)
        return jsonify({'message': 'Pomodoro Completed!'})
    except KeyboardInterrupt:
        return jsonify({'message': 'Timer stopped.'})


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start_timer/<int:work_duration>/<int:break_duration>')
def start_timer_route(work_duration, break_duration):
    return start_timer(work_duration, break_duration)

def start_timer(work_duration, break_duration):
    work_timer_thread = threading.Thread(
        target=pomodoro_timer, args=(work_duration,))
    break_timer_thread = threading.Thread(
        target=pomodoro_timer, args=(break_duration,))

    work_timer_thread.start()
    # Wait for the work timer to finish before starting the break timer
    work_timer_thread.join()
    break_timer_thread.start()

    return jsonify({'message': f'Pomodoro timer started! Work: {work_duration} minutes, Break: {break_duration} minutes'})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
