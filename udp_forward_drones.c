#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <string.h>
#include <netdb.h>

// Listen on listen_ip:listen_port and forward packets to forward_ip:forward_port
// gcc -o udp_forward udp_forward.c

int main(int argc, char *argv[])
{
    char listen_ip[] = "0.0.0.0\0";
    char listen_port[] = "11111\0";
    char destination_ports[][6] = {"14001\0", "14002\0", "14003\0", "14004\0", "14005\0"};
  
  // Create UDP socket
  int sock = socket(PF_INET, SOCK_DGRAM, IPPROTO_IP);

  // Listen address
  struct sockaddr_in listen_addr;
  listen_addr.sin_family = AF_INET;
  listen_addr.sin_addr.s_addr = inet_addr(listen_ip);
  listen_addr.sin_port = htons((uint16_t) atoi(listen_port));  // htons() flips the byte order

  // Bind socket to listen address
  if (bind(sock, (struct sockaddr *) &listen_addr, sizeof(listen_addr)) == -1) {
    printf("Cannot bind address %s:%s\n", argv[1], argv[2]);
    exit(1);
  }

  printf("Listening on %s:%s\n", listen_ip, listen_port);
    socklen_t listen_addr_len = sizeof(listen_addr);

    const char hostname[] = "localhost";

    /* resolve hostname */
    struct hostent* he;
    if ( (he = gethostbyname(hostname) ) == NULL ) {
        exit(1); /* error */
    }
    
    /* copy the network address to sockaddr_in structure */
    struct sockaddr_in destination_addr;
    memcpy(&destination_addr.sin_addr.s_addr, he->h_addr_list[0], he->h_length);
    destination_addr.sin_family = AF_INET;

  while (1) {
    char buf[65535];

    // Where the packet came from

    // Receive a packet
    ssize_t n = recvfrom(sock, buf, sizeof(buf), 0, (struct sockaddr *) &listen_addr, &listen_addr_len);
    if (n <= 0) {
      continue;
    }else{
        // get ip and forward the message to port based on the ip
        char* ipString = inet_ntoa(listen_addr.sin_addr);
        size_t ipLen = strlen(ipString);
        int port_index = (uint16_t) atoi(&ipString[ipLen-1])-1; //last number in ip address - 1
        
        // forward the message to localhost:destination port
        // destination_addr.sin_port = destination_ports[0];
        destination_addr.sin_port = htons((uint16_t) atoi(destination_ports[port_index]));
        
        sendto(sock, buf, (size_t) n, 0, (struct sockaddr *) &destination_addr, sizeof(destination_addr));
        
        // reset buffer 
        memset(buf, 0, sizeof(buf));

        // for debugging
        printf("%d\n",port_index);
        printf("%s\n",ipString);
        printf("destination %d:%d\n",destination_addr.sin_addr.s_addr,destination_addr.sin_port);
        printf("%s\n",buf);
    }
  }
}
