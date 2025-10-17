from flask import Flask, render_template, request, jsonify
import subprocess
import platform
import socket
import speedtest

app = Flask(__name__)

def run_ping(host):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '4', host]
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
        return output
    except subprocess.CalledProcessError as e:
        return e.output

def run_traceroute(host):
    command = ['tracert', host] if platform.system().lower() == 'windows' else ['traceroute', host]
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
        return output
    except subprocess.CalledProcessError as e:
        return e.output

def run_speed_test():
    st = speedtest.Speedtest()
    download_speed = st.download() / 1_000_000  # Mbps
    upload_speed = st.upload() / 1_000_000      # Mbps
    return {
        "download_speed": round(download_speed, 2),
        "upload_speed": round(upload_speed, 2)
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ping', methods=['POST'])
def ping():
    host = request.form['host']
    result = run_ping(host)
    return jsonify({'output': result})

@app.route('/traceroute', methods=['POST'])
def traceroute():
    host = request.form['host']
    result = run_traceroute(host)
    return jsonify({'output': result})

@app.route('/speedtest')
def speedtest_route():
    result = run_speed_test()
    return jsonify(result)

@app.route('/info')
def info():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    os_info = platform.platform()
    return jsonify({
        'hostname': hostname,
        'ip_address': ip_address,
        'os_info': os_info
    })

if __name__ == '__main__':
    app.run(debug=True)
