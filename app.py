from flask import Flask, render_template, request
import socket
import nmap
import ipaddress

app = Flask(__name__)
scanner = nmap.PortScanner()

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []

    if request.method == 'POST':
        mode = request.form.get('mode')
        if mode == 'single':
            target = request.form.get('single_target')
            scan_result = scan_ip(target)
            results.append(scan_result)

        elif mode == 'range':
            start_ip = request.form.get('start_ip').strip()
            end_ip = request.form.get('end_ip').strip()
            try:
                # Convert to IP objects
                start = ipaddress.IPv4Address(start_ip)
                end = ipaddress.IPv4Address(end_ip)
                for ip_int in range(int(start), int(end) + 1):
                    ip_str = str(ipaddress.IPv4Address(ip_int))
                    scan_result = scan_ip(ip_str)
                    results.append(scan_result)
            except Exception as e:
                results.append({'input': f"{start_ip} → {end_ip}", 'ip': 'Invalid range', 'reverse': '', 'ports': [str(e)]})

    return render_template('index.html', results=results)

def scan_ip(target):
    result = {'input': target}

    try:
        result['ip'] = socket.gethostbyname(target)
    except:
        result['ip'] = "Could not resolve"

    try:
        result['reverse'] = socket.gethostbyaddr(target)[0]
    except:
        result['reverse'] = "No reverse DNS"

    try:
        scanner.scan(target, arguments='-T4 -p 22,80,443')
        ports = []
        for proto in scanner[target].all_protocols():
            for port in scanner[target][proto].keys():
                state = scanner[target][proto][port]['state']
                ports.append(f"{port}/{proto}: {state}")
        result['ports'] = ports if ports else ["No open ports"]
    except Exception as e:
        result['ports'] = [f"Scan failed: {str(e)}"]

    return result

if __name__ == '__main__':
    app.run(debug=True)
