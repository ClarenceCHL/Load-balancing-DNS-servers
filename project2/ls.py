import logging
import socket
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import queue

is_new_query_coming_in = False
# we'll trying to use multi-threading to do this work
executor = ThreadPoolExecutor(max_workers=2)
socket_pool = queue.Queue()


def recv_dns_query_result(data: bytes, addr: tuple):
    try:
        # retrieving socket instance if there exists socket instances in socket_pool
        if socket_pool.empty():
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(3)
        else:
            s = socket_pool.get_nowait()
        BUFFER_SIZE = 1024
        s.sendto(data, addr)
        response_bytes, addr = s.recvfrom(BUFFER_SIZE)
        socket_pool.put_nowait(s)
        return True, response_bytes
    except:
        return False, None


def main(listen_port: int, ts1_hostname: str, ts1_listen_port: int, ts2_hostname: str, ts2_listen_port: int):
    socket_for_this_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_for_this_server.bind(("localhost", listen_port))
    BUFFER_SIZE = 1024
    logging.info("\nServer ls started and is running on port %d!" % listen_port)
    while True:
        # recv dns query from client
        dns_query, client_addr = socket_for_this_server.recvfrom(BUFFER_SIZE)
        client_ip, unused = client_addr
        logging.info("\nA dns query for hostname %s from host %s is coming in..." %
                     (dns_query.decode("utf-8"), client_ip))
        # create tasks to get dns results from ts servers concurrently
        query_ts1_task = executor.submit(recv_dns_query_result, dns_query, (ts1_hostname, ts1_listen_port))
        query_ts2_task = executor.submit(recv_dns_query_result, dns_query, (ts2_hostname, ts2_listen_port))
        final_result = False  # indicate whether results of two tasks are both False
        for future in as_completed([query_ts1_task, query_ts2_task]):
            bool_result, response = future.result()
            final_result = final_result or bool_result
            if bool_result:
                # if we get a result from one of two ts server, we'll return this result to client
                socket_for_this_server.sendto(response, client_addr)
                logging.info("\nThe dns query for hostname %s from host %s is returned successfully! Result is %s:" %
                             (dns_query.decode("utf-8"), client_ip, response.decode("utf-8")))
                break
        # if final_result is False after getting all results of tasks,
        # this means current dns query has an Error:HOST NOT FOUND result
        if not final_result:
            response = dns_query.decode("utf-8") + " - Error: HOST NOT FOUND"
            socket_for_this_server.sendto(response.encode("utf-8"), client_addr)
            logging.info("\nThe dns query for hostname %s from host %s has <Error:HOST NOT FOUND> result!" %
                         (dns_query.decode("utf-8"), client_ip))
            continue


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                        level=logging.DEBUG)
    logging.info("\nServer ls is starting...")
    args = sys.argv
    # test validity of arguments
    if len(args) < 6:
        logging.error("\nThere must be 6 params - python_file_name ls_listen_port "
                      "ts1_hostname ts1_listen_port ts2_hostname ts2_listen_port!")
        sys.exit()
    ls_listen_port_str = args[1]
    ts1_listen_port_str = args[3]
    ts2_listen_port_str = args[5]
    if not ls_listen_port_str.isdigit() or not ts1_listen_port_str.isdigit() or not ts2_listen_port_str.isdigit():
        logging.error("\nThe three ports must be integers, while you typed :\n"
                      "ls_listen_port: %s\n"
                      "ts1_listen_port: %s\n"
                      "ts2_listen_port: %s."
                      % (ls_listen_port_str, ts1_listen_port_str, ts2_listen_port_str))
        sys.exit()
    main(int(ls_listen_port_str), args[2], int(ts1_listen_port_str), args[4], int(ts2_listen_port_str))
    logging.info("\n\nls server exit.")
