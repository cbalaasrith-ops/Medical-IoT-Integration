from scapy.all import *

packets = []

# Capture MQTT traffic
def capture_mqtt_packet(packet):
    if packet.haslayer(TCP):
        if packet[TCP].dport == 1883 or packet[TCP].sport == 1883:
            packets.append(packet)
            print(f"[*] Captured packet: {packet.summary()}")

# Save packets to pcap file
def save_packets_to_file():
    if packets:
        wrpcap("mqtt_traffic.pcap", packets)
        print("[*] Packets saved to mqtt_traffic.pcap")
    else:
        print("[!] No packets captured")

# Sniff and save
if __name__ == "__main__":
    sniff(iface="lo0", filter="tcp port 1883", prn=capture_mqtt_packet, timeout=300)  # Sniff for 30 seconds
