import os
import sys
import threading
import webbrowser
from datetime import datetime

from flask import Flask, jsonify, render_template, request

from autotune import (detect_miners, get_system_info, monitor_and_adjust,
                      restart_bitaxe)
from autotune import stop_autotuning as stop_autotune_logic
from config import (add_miner, get_miners, load_config, remove_miner,
                    save_config)

# --- Globals ---
app = Flask(__name__)
log_messages = []
autotune_threads = []
autotune_running = False

# --- Logging ---
def log_message(message, level="info"):
    global log_messages
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"[{timestamp}] [{level.upper()}] {message}"
    print(formatted_message)  # Also print to console
    log_messages.append(formatted_message)
    # Limit log size
    if len(log_messages) > 200:
        log_messages = log_messages[-200:]

# --- API Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/logs', methods=['GET'])
def get_logs():
    return jsonify(log_messages)

@app.route('/api/miners', methods=['GET'])
def get_all_miners():
    return jsonify(get_miners())

@app.route('/api/miners', methods=['POST'])
def add_new_miner():
    data = request.json
    nickname = data.get('nickname')
    ip = data.get('ip')
    if not ip:
        return jsonify({"message": "IP address is required."}), 400
    add_miner("Unknown", ip, nickname)
    log_message(f"Manually added miner {nickname or ip}", "success")
    return jsonify(get_miners())

@app.route('/api/miners/<string:ip>', methods=['DELETE'])
def delete_miner_by_ip(ip):
    remove_miner(ip)
    log_message(f"Removed miner {ip}", "success")
    return jsonify({"message": "Miner removed."})

@app.route('/api/miners/save', methods=['POST'])
def save_miner_settings():
    data = request.json.get('miners', [])
    config = load_config()
    
    existing_miners_map = {m['ip']: m for m in config.get('miners', [])}
    
    updated_miners_list = []
    for miner_data in data:
        ip = miner_data.get('ip')
        if ip in existing_miners_map:
            existing_miner = existing_miners_map[ip]
            existing_miner['nickname'] = miner_data.get('nickname', existing_miner['nickname'])
            existing_miner['type'] = miner_data.get('type', existing_miner['type'])
            updated_miners_list.append(existing_miner)
        else:
            updated_miners_list.append({
                "nickname": miner_data.get('nickname'),
                "type": miner_data.get('type'),
                "ip": ip
            })
    
    config['miners'] = updated_miners_list
    save_config(config)
    log_message("Saved miner settings to config.json", "success")
    return jsonify({"message": "Settings saved."})
    
@app.route('/api/miner-info/<string:ip>', methods=['GET'])
def get_miner_info(ip):
    info = get_system_info(ip)
    if isinstance(info, str):
        return jsonify({"message": info}), 500
    return jsonify(info)

@app.route('/api/scan', methods=['POST'])
def scan_network():
    data = request.json
    start_ip = data.get('start_ip')
    end_ip = data.get('end_ip')
    log_message(f"Network scan initiated from {start_ip} to {end_ip}", "info")
    
    def scan_task():
        found_ips = detect_miners(start_ip, end_ip)
        log_message(f"Scan complete. Found {len(found_ips)} new miners.", "success")

    threading.Thread(target=scan_task, daemon=True).start()
    return jsonify({"message": "Scan started in background."})

@app.route('/api/settings', methods=['GET'])
def get_settings():
    return jsonify(load_config())

@app.route('/api/settings', methods=['POST'])
def update_settings():
    new_settings = request.json
    save_config(new_settings)
    log_message("Global and Autotuner settings updated.", "success")
    return jsonify({"message": "Settings updated."})

@app.route('/api/autotune/start', methods=['POST'])
def start_autotuning():
    global autotune_threads, autotune_running
    if autotune_running:
        return jsonify({"message": "Autotuner is already running."}), 400

    config = load_config()
    active_miners = [m for m in config.get("miners", []) if m.get("enabled")]
    if not active_miners:
        log_message("Start command received, but no miners are enabled for autotuning.", "warning")
        return jsonify({"message": "No miners enabled for autotuning."}), 404

    log_message("Starting autotuning for enabled miners...", "success")
    autotune_running = True
    autotune_threads.clear()

    for miner in active_miners:
        thread = threading.Thread(
            target=monitor_and_adjust,
            args=(
                miner['ip'],
                miner.get('type', 'Unknown'),
                config.get('monitor_interval', 10),
                log_message,
                miner.get("min_freq"),
                miner.get("max_freq"),
                miner.get("min_volt"),
                miner.get("max_volt"),
                miner.get("max_temp"),
                miner.get("max_watts"),
                miner.get("start_freq"),
                miner.get("start_volt"),
                miner.get("max_vr_temp")
            )
        )
        thread.daemon = True
        thread.start()
        autotune_threads.append(thread)

    return jsonify({"message": "Autotuning started."})

@app.route('/api/autotune/stop', methods=['POST'])
def stop_autotuning():
    global autotune_running
    log_message("Stopping autotuning...", "warning")
    stop_autotune_logic()
    autotune_running = False
    autotune_threads.clear()
    return jsonify({"message": "Autotuning stopped."})

@app.route('/api/restart-miner/<string:ip>', methods=['POST'])
def restart_miner_api(ip):
    log_message(f"Restarting miner at {ip}...", "warning")
    msg = restart_bitaxe(ip)
    log_message(msg, "info")
    return jsonify({"message": msg})

@app.route('/api/open-web-ui/<string:ip>', methods=['GET'])
def open_web_ui(ip):
    url = f"http://{ip}"
    log_message(f"Opening web UI for miner at {url}", "info")
    webbrowser.open(url)
    return jsonify({"message": f"Attempted to open {url} in browser."})
