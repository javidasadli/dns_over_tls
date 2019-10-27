import socket, ssl

port = 53
host = "0.0.0.0"
dns = "1.1.1.1"
certificate = "/etc/ssl/certs/ca-bundle.crt"

def send_message(dns, query, certificate):
    cloudflare = (dns, 853)
    dns_sock_cloud = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dns_sock_cloud.settimeout(80)
    cer = ssl.create_default_context()
    cer = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    cer.verify_mode = ssl.CERT_REQUIRED
    cer.check_hostname = True
    cer.load_verify_locations(certificate)
    wrapped_socket = cer.wrap_socket(dns_sock_cloud, server_hostname=dns)
    wrapped_socket.connect(cloudflare)
    wrapped_socket.send(query)
    data = wrapped_socket.recv(4096)
    return data

dns_sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dns_sock_tcp.bind((host, port))
dns_sock_tcp.listen(5)

while True:
    clientsocket_tcp, address = dns_sock_tcp.accept()
    data = clientsocket_tcp.recv(1024)
    answer = send_message(dns, data, certificate)
    clientsocket_tcp.send(answer)
    clientsocket_tcp.close()