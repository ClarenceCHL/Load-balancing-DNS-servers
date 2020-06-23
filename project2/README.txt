# Question 1 - LS functionality of tracking which TS responded to the query and timing out if neither TS responded
### Answer: 
1. We used `ThreadPoolExecutor` to do this work
2. Firstly, we create a socket instance which is used to recv dns query from client in a `While` loop.
3. Then we defined a function `recv_dns_query_result`. In this function, we should get a socket instance first, but we cannot create a socket instance while the function is executed, so we create a queue `socket_pool` to store the socket instances created. We retrieve one to send and recv udp request if there are socket instances in the queue.
4. The timeout attribute of all socket instances has been set to 3 seconds, which means if all sockets have a timeout occurrence, we'll return Error to client.
5. With those implementations, the LS function works successfully.

# Question 2 - Are there known issues or functions that aren't working currently in your attached code?
### Answer:
After testing, we think there is no issues or functions that aren't working, but maybe there are some bugs that we didn't identify.

# Question 3 - What problems did you face developing code for this project?
### Answer:
Concurrent coding using `ThreadPoolExecutor` is the biggest problem we faced, because we were not familiar with it. Nevertheless, we made it to work by using online resources and modifying codes many times.

# Question 4 - What did you learn by working on this project?
### Answer
The most significant thing that we have learnt is the rudiments of concurrency in python. This is really helpful for our code learning in the future because we have learnt a powerful tool to solve many problems.