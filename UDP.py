import socket, ssl

port = 53
host = "0.0.0.0"
dns = "1.1.1.1"
certificate = "/etc/ssl/certs/ca-bundle.crt"

def send_message(dns, query, certificate):
    cloudflare = (dns, 853)
    dns_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dns_sock.settimeout(80)
    cer = ssl.create_default_context()
    cer = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    cer.verify_mode = ssl.CERT_REQUIRED
    cer.check_hostname = True
    cer.load_verify_locations(certificate)
    wrapped_socket = cer.wrap_socket(dns_sock, server_hostname=dns)
    wrapped_socket.connect(cloudflare)
    tcp_msg = "\x00".encode() + chr(len(query)).encode() + query
    wrapped_socket.send(tcp_msg)
    data = wrapped_socket.recv(1024)
    return data

while True:
    dns_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dns_sock.bind((host, port))
    data, address = dns_sock.recvfrom(1024)
    answer = send_message(dns, data, certificate)
    return_ans = answer[2:]
    dns_sock.sendto(return_ans, address)
    dns_sock.close()
    