import socket

def check_http_service(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  # Set a timeout for the connection attempt
            s.connect((ip, port))
            return True
    except (socket.timeout, ConnectionRefusedError):
        return False

def scan_ips(start, end, port):
    for i in range(start, end + 1):
        ip = f'134.197.94.{i}'
        print('Trying for ..', ip)
        if check_http_service(ip, port):
            print(f'HTTP service found on {ip}:{port}')

if __name__ == "__main__":
    start_ip = 1
    end_ip = 255
    http_port = 80

    scan_ips(start_ip, end_ip, http_port)