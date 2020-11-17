
# -*- coding: utf-8 -*-

# import socket
# import struct

# # creating a rawSocket for communications
# # PF_SOCKET (packet interface), SOCK_RAW (Raw socket) - htons (protocol) 0x08000 = IP Protocol
# rawSocket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))

# # deciding interface - packet sniffing and then injection
# rawSocket.bind(("eth0", socket.htons(0x0800)))

# # create a ethernet packet
# packet = struct.pack("!6s6s2s", '\xaa\xaa\xaa\xaa\xaa\xaa', '\xbb\xbb\xbb\xbb\xbb\xbb', '\x08\x00')
# # 6 dest address, 6 source address and 2 for ethtype = IP

# # inject a random string after the header
# rawSocket.send(packet + "Marico el que lo lea")


# '''
# 	Raw sockets on Linux
# '''

# # some imports
# import socket, sys, time
# from struct import *

# # checksum functions needed for calculation checksum
# def checksum(msg):
# 	s = 0
	
# 	# loop taking 2 characters at a time
# 	for i in range(0, len(msg), 2):
# 		w = ord(msg[i]) + (ord(msg[i+1]) << 8 )
# 		s = s + w
	
# 	s = (s>>16) + (s & 0xffff)
# 	s = s + (s >> 16)
	
# 	#complement and mask to 4 byte short
# 	s = ~s & 0xffff
	
# 	return s

# # the main function
# def main():

#     #create a raw socket
#     # try:
#     s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
#     # except socket.error.msg:
#     #     print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
#     #     sys.exit()

#     # tell kernel not to put in headers, since we are providing it, when using IPPROTO_RAW this is not necessary
#     # s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        
#     # now start constructing the packet
#     packet = ''

#     source_ip = '1.2.3.4'
#     dest_ip = '192.168.1.1'	# or socket.gethostbyname('www.google.com')

#     # ip header fields
#     ip_ihl = 5
#     ip_ver = 4
#     ip_tos = 0
#     ip_tot_len = 0	# kernel will fill the correct total length
#     ip_id = 54321	#Id of this packet
#     ip_frag_off = 0
#     ip_ttl = 255
#     ip_proto = socket.IPPROTO_TCP
#     ip_check = 0	# kernel will fill the correct checksum
#     ip_saddr = socket.inet_aton ( source_ip )	#Spoof the source ip address if you want to
#     ip_daddr = socket.inet_aton ( dest_ip )

#     ip_ihl_ver = (ip_ver << 4) + ip_ihl

#     # the ! in the pack format string means network order
#     ip_header = pack('!BBHHHBBH4s4s' , ip_ihl_ver, ip_tos, ip_tot_len, ip_id, ip_frag_off, ip_ttl, ip_proto, ip_check, ip_saddr, ip_daddr)

#     # tcp header fields
#     tcp_source = 1234	# source port
#     tcp_dest = 80	# destination port
#     tcp_seq = 454
#     tcp_ack_seq = 0
#     tcp_doff = 5	#4 bit field, size of tcp header, 5 * 4 = 20 bytes
#     #tcp flags
#     tcp_fin = 0
#     tcp_syn = 1
#     tcp_rst = 0
#     tcp_psh = 0
#     tcp_ack = 0
#     tcp_urg = 0
#     tcp_window = socket.htons (5840)	#	maximum allowed window size
#     tcp_check = 0
#     tcp_urg_ptr = 0

#     tcp_offset_res = (tcp_doff << 4) + 0
#     tcp_flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + (tcp_psh <<3) + (tcp_ack << 4) + (tcp_urg << 5)

#     # the ! in the pack format string means network order
#     tcp_header = pack('!HHLLBBHHH' , tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags,  tcp_window, tcp_check, tcp_urg_ptr)

#     user_data = 'Hello, how are you'

#     # pseudo header fields
#     source_address = socket.inet_aton( source_ip )
#     dest_address = socket.inet_aton(dest_ip)
#     placeholder = 0
#     protocol = socket.IPPROTO_TCP
#     tcp_length = len(tcp_header) + len(user_data)

#     psh = pack('!4s4sBBH' , source_address , dest_address , placeholder , protocol , tcp_length);
#     psh = psh + tcp_header + user_data;

#     tcp_check = checksum(psh)
#     #print tcp_checksum

#     # make the tcp header again and fill the correct checksum - remember checksum is NOT in network byte order
#     tcp_header = pack('!HHLLBBH' , tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags,  tcp_window) + pack('H' , tcp_check) + pack('!H' , tcp_urg_ptr)

#     # final full packet - syn packets dont have any data
#     packet = ip_header + tcp_header + user_data
    
#     # increase count to send more packets
#     count = 3
    
#     for i in range(count):
#         print ('sending packet...')
#         # Send the packet finally - the port specified has no effect
#         s.sendto(packet, (dest_ip , 0 ))	# put this in a loop if you want to flood the target 
#         print ('send')
#         time.sleep(1)
        
#     print ('all packets send')

# main()



# import socket
# import sys

# # the public network interface
# HOST = socket.gethostbyname(socket.gethostname())
# print (socket.gethostname())

# # create a raw socket and bind it to the public interface
# s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
# s.bind((HOST, 12345))

# # Include IP headers
# s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

# # receive all packages
# s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

# # receive a package
# print (s.recvfrom(65565))

# # disabled promiscuous mode
# s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)


import socket



# port = 8001                             # 端口和上面一致
# host = "localhost"                      # 服务器IP，这里服务器和客户端IP同一个
 
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# for i in range(10):
#     # sock.sendto("Successful! Message %s! " % i,(host, port))
#     sock.sendto("Successful! Message", host, port)


port = 8001
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", port))                     # 从给定的端口，从任何发送者，接收UDP数据报
print("Waiting for the port", port)
 
while True:
    data, address = sock.recvfrom(1024)   # 接收一个最大报文为1024字节的数据报
    print("Received:", data, "from", address)