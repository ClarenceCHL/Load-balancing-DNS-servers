import logging
import socket
import sys

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                        level=logging.DEBUG)
    args = sys.argv
    # test the validity of arguments
    if len(args) < 3:
        logging.error("\nThere must be 3 params typed - python_file_name, ls_hostname, ls_listen_port!")
        sys.exit()
    ls_listen_port_str = args[2]
    if not ls_listen_port_str.isdigit():
        logging.error("\nThe ls_listen_port must be an integer, while you typed %s", ls_listen_port_str)
        sys.exit()
    ls_listen_port = int(ls_listen_port_str)
    ls_hostname = args[1]

    # create socket to send requests
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    BUFFER_SIZE = 1024

    src_file_path = "PROJ2-HNS.txt"
    src_file = open(src_file_path, "r")
    hostname = src_file.readline().replace('\n', '')

    output_file_path = "RESOLVED.txt"
    output_file = open(output_file_path, "wb")
    # send dns query and save results to file
    while hostname:
        s.sendto(hostname.encode("utf-8"), (ls_hostname, ls_listen_port))
        data_bytes, unused = s.recvfrom(BUFFER_SIZE)
        output_file.write(data_bytes)
        output_file.write("\n".encode("utf-8"))
        logging.info("\nQuery for hostname %s complete!" % hostname)
        hostname = src_file.readline().replace('\n', '')
    logging.info("\nSuccess! All DNS queries complete successfully and results have been written into RESOLVED.txt!")
    logging.info("\n\nClient exit.")
