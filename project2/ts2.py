import sys
import logging
import socket

# define the usable port range for this server
PORT_LOWER_BOUND = 10000
PORT_UPPER_BOUND = 65535

dns_file = "PROJ2-DNSTS2.txt"
file = open(dns_file, "r")
hostname_mapped_to_ip_dict = {}


def main(port: int):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("localhost", port))
    BUFFER_SIZE = 1024
    logging.info("\nServer ts2 started and is running on port %d!" % port)
    while True:
        data_not_decoded, client_addr = s.recvfrom(BUFFER_SIZE)
        ip, port = client_addr
        hostname = data_not_decoded.decode("utf-8")
        logging.info("\nA dns query for hostname %s from host %s is coming in..." % (hostname, ip))
        if hostname in hostname_mapped_to_ip_dict:
            response_str = hostname + ' ' + hostname_mapped_to_ip_dict[hostname]
            s.sendto(response_str.encode("utf-8"), client_addr)
            logging.info("\nResponse to dns query for hostname %s from host %s is sent successfully!" % (hostname, ip))
            continue
        logging.info("\nThere is no ip address for hostname %s! So server will not send any response!" % hostname)


def read_hostname_and_ip():
    """
    this function is defined to read all host names and their ips from specified file
    :return: nothing
    """
    while True:
        hostname_and_ip_str = file.readline()
        if not hostname_and_ip_str:
            return
        hostname_and_ip_arr = hostname_and_ip_str.split(' ')
        hostname_mapped_to_ip_dict.update({hostname_and_ip_arr[0]
                                           : hostname_and_ip_arr[1] + ' ' + hostname_and_ip_arr[2].replace('\n', '')})


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                        level=logging.DEBUG)
    args = sys.argv
    logging.info("\nServer ts2 is starting...")
    if len(args) < 2:
        logging.error("\nThere must be two params - python_file_name port!")
        sys.exit()
    if not args[1].isdigit() or (int(args[1]) < PORT_LOWER_BOUND or int(args[1]) > PORT_UPPER_BOUND):
        logging.error("\nThe first parameter(port) must be an integer which range from %d(included) and %d(included)!!"
                      % (PORT_LOWER_BOUND, PORT_UPPER_BOUND))
        sys.exit()
    read_hostname_and_ip()
    main(port=int(args[1]))
    logging.info("\n\nts1 server exit.")
