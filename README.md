# DNS to DNS-over-TLS proxy
DNS-Over-TLS is used to send DNS queries over encrypted connection. By default DNS queries are sent over the plan test connection. This "DNS-to-DNS-over-TLS-proxy" is acting as DNS forwarder and resolve queries using an Cloudflare DNS which encrypt connection. 

# Instruction to get started

* app.py - Python script for DNS-Over-TLS proxy
* Dockerfile - Dockerfile to create image

## Usage:

Note: This is tested on Docker host which is setup on EC2 instance with Amazon Linux. 

1. Download the zip file provided and Extract it
2. Changed to directory "DNS-OVER-TLS-Proxy"
3. Create a Docker image using 
    - $ docker image build -t secureDns .
4. Create a Docker container 
    - $ docker run -d --rm -p 53:53/tcp -p 53:53/udp secureDns
5. Run dig queries 
    - $ dig @127.0.0.1 google.com 

Note: Look for DNS padding done by Cloudflare

```
[ec2-user@ip-172-31-38-59 ~]$ dig @0.0.0.0 google.com

; <<>> DiG 9.11.4-P2-RedHat-9.11.4-26.P2.amzn2.2 <<>> @0.0.0.0 google.com
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 62050
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
; PAD: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 (".........................................................................................................................................................................................................................................................................................................................................................................................................................")
;; QUESTION SECTION:
;google.com.			IN	A

;; ANSWER SECTION:
google.com.		133	IN	A	172.217.164.174

;; Query time: 68 msec
;; SERVER: 127.0.0.1#53(0.0.0.0)
;; WHEN: Fri Mar 12 13:25:05 UTC 2021
;; MSG SIZE  rcvd: 468

[ec2-user@ip-172-31-38-59 ~]$ 
```

## What would be the security concerns you would raise?
When a browser send request to the DNS-Over-TLS proxy server and then proxy server will create TCP connection with cloudflare DNS server, In between one can spoof traffic between browser and dns server and add or edit datagram and send it over the TCP connection.

## How would you integrate that solution in a distributed, microservices-oriented and containerized architecture?
We can use it in microservice as it is highly available, scalable. Security is depending on complete architecture of microservice. It can be deployed into kubernetes to scale and highly available and can be easily integrated into miscroservice deployment. We can make use of jenkins to automate the deployment into docker or kubernetes. 

## What other improvements do you think would be interesting to add to the project?
1. Logging can be enabled.
2. Other DNS-Over-TLS server can be used such as Quad9.
3. We can use caching features for faster query and better performance.
4. Update proxy ip in browser setting to handle request from browser.
5. We can maintain the socket connection for specific time period. This reduce overhead of TLS connection.
6. Queries can be stored in Database along with the time of query and status, etc.

