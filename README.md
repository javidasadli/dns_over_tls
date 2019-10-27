Simple proxy which listens 53 TCP/UDP port that capturing DNS requests and redirecting it to Cloudflare's 1.1.1.1 DNS over an encrypted channel over TLS.
Currently, I am using two seperate python script to listen TCP and UDP. 
Usage is just run it with python3.
python3 udp.py


I could not finish it totally and it is not final version. I need to add there logging, error exceptions, limit connections and etc. 