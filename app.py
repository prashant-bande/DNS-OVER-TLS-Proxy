#!/usr/bin/env python3

# Importing libraries
import socket
import ssl
import binascii
import threading
from argparse import ArgumentParser

def send_message(dns, query, cert):
    """
    Function to create SSL session and return full message which is formatted according to RFC-1035.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(60)

    context = ssl.create_default_context()
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.load_verify_locations(cert)

    wrapped_socket = context.wrap_socket(sock, server_hostname=dns)
    wrapped_socket.connect((dns, 853))

    tcp_msg = "\x00".encode() + chr(len(query)).encode() + query

    wrapped_socket.send(tcp_msg)
    data = wrapped_socket.recv(1024)

    return data

def thread(data, address, socket, dns, cert):
    """
    This function is used as callable inside threading.Tread in main function to handle multiple incoming request.
    """
    answer = send_message(dns, data, cert)
    if answer:
        rcode = binascii.hexlify(answer[:6]).decode("utf-8")
        rcode = rcode[11:]
        if int(rcode, 16) == 1:
            print(rcode)
        else:
            return_ans = answer[2:]
            socket.sendto(return_ans, address)
    else:
        print("Got empty reply from server.")


def main():
    """
    Main function
    """
    parser = ArgumentParser(description="DNS to DNS-over-TLS proxy.")
    
    parser.add_argument("-p", "--port", type=int, default=53, required=False, help="Port on which proxy listen. default: 53")
    parser.add_argument("-d", "--dns", type=str, default="1.1.1.1", required=False, help="Domain server with TLS. default: 1.1.1.1")
    parser.add_argument("-a", "--address", type=str, default="0.0.0.0", required=False, help="Proxy network interface Address. default: 0.0.0.0")
    parser.add_argument("-c", "--cert", type=str, default="/etc/ssl/cert.pem", required=False, help="Path to the certificates file. default: /etc/ssl/cert.pem")

    args = parser.parse_args()
    port = args.port
    host = args.address
    dns = args.dns
    cert = args.cert
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((host, port))
        while True:
            data, address = sock.recvfrom(4096)
            threading.Thread(target=thread, args=(data, address, sock, dns, cert)).start()
    except Exception as e:
        print(e)
    finally:
        sock.close()

if __name__ == "__main__":
    main()
