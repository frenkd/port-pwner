import os
from flask import Flask, render_template, redirect, url_for, request
from portscan import scan, get_last, get_path, get_scan, get_scans, get_service_name, get_scans_from_target
import json
from datetime import datetime
from servicer import get_latest_version
from pprint import pprint
from time import sleep

# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
)


@app.route('/')
def base():
    scans = get_scans()
    for scan in scans:
        scan['time'] = datetime.fromtimestamp(
        float(scan['id'])).strftime('%Y-%m-%d, %H:%M:%S')
    return render_template('index.html', scans=scans, scans_str=str(scans))


@app.route('/<target>')
def for_target(target):
    scans = get_scans_from_target(target)
    for scan in scans:
        scan['time'] = datetime.fromtimestamp(
            float(scan['id'])).strftime('%Y-%m-%d, %H:%M:%S')
    return render_template('target_view.html', scans=scans, scans_str=str(scans))

@app.route('/periodic_scan')
def periodic_scan():
    return render_template('periodic_scan.html')


@app.route('/start_scan', methods=['POST'])
def start_scan():
    target = request.form['target']
    if target == "":
        target = "localhost"
    results = scan(target)
    return json.dumps(results)


@app.route('/<target>/<scanId>')
def view_scan(target, scanId):
    scan = get_scan(scanId, str(target))
    scan = add_curr_version(scan)
    scan_str = str(scan)
    scan_date = datetime.fromtimestamp(
        float(scanId)).strftime('%Y-%m-%d, %H:%M:%S')
    return render_template('scan_view.html', scan=scan, scan_date=scan_date, scan_str=scan_str, target=target)


@app.route('/start_periodic_scan', methods=['POST'])
def start_periodic_scan():
    target = request.form['target']
    interval = int(request.form['interval'])
    scan_num = int(request.form['scan_num'])

    results = []
    for i in range(scan_num):
        result = scan(target)
        results.append(result)
        sleep(interval)
        
    return json.dumps(results)

def add_curr_version(scan):
    del scan['target']
    del scan['summary']
    print(scan)
    for port in scan:
        if("removed" in scan[port]):
            continue
        scan[port]['latest_version'] = get_latest_version(
            scan[port]['serviceID'])
        if scan[port]['response'] is not None:
            scan[port]['response'] = scan[port]['response'] if len(
                scan[port]['response']) < 100 else scan[port]['response'][:100]+'...'
    return scan


if __name__ == '__main__':
    app.run(debug=True)
