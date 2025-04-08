import socket
import struct

# Create raw socket to listen to all traffic
s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))

print("Listening for UDP packets to port 1100...")

def checksum(data):
    if len(data) % 2 != 0:
        data += b'\x00'  # padding

    total = 0
    for i in range(0, len(data), 2):
        word = data[i] << 8 | data[i + 1]
        total += word

    while total >> 16:
        total = (total & 0xFFFF) + (total >> 16)

    return ~total & 0xFFFF


while True:
    raw_data, addr = s.recvfrom(65535)

    eth_length = 14
    eth_header = raw_data[:eth_length]

    # Parse IP header
    ip_header = raw_data[eth_length:eth_length + 20]
    iph = struct.unpack('!BBHHHBBH4s4s', ip_header)

    protocol = iph[6]
    if protocol != 17:  # 17 = UDP
        continue

    # Parse UDP header
    udp_start = eth_length + 20
    udp_header = raw_data[udp_start:udp_start + 8]
    udph = struct.unpack('!HHHH', udp_header)

    src_port = udph[0]
    dest_port = udph[1]

    # Filter packets to port 1100
    if dest_port == 1100:
        # Recalcula o checksum para verificar
        data = raw_data[udp_start + 8:]
        
        udp_length = 8 + len(data)
        source_ip = iph[8]
        dest_ip = iph[9]

        # Monta pseudo-header
        pseudo_header = struct.pack('!4s4sBBH',
            source_ip,
            dest_ip,
            0,
            socket.IPPROTO_UDP,
            udp_length
        )

        # Monta cabeçalho UDP com checksum zerado
        udp_header_zero_checksum = struct.pack('!HHHH',
            src_port,
            dest_port,
            udp_length,
            0
        )

        # Dados usados para o cálculo
        checksum_data = pseudo_header + udp_header_zero_checksum + data
        calculated_checksum = checksum(checksum_data)

        # Checksum recebido do pacote original
        received_checksum = udph[3]

        # Verificação
        if calculated_checksum == received_checksum:
            print(f"[✔] Checksum válido: {received_checksum:#04x}")
        else:
            print(f"[✘] Checksum inválido! Recebido: {received_checksum:#04x}, Calculado: {calculated_checksum:#04x}")

        print(f"Packet from port {src_port} to {dest_port}: {data.decode(errors='ignore')}")
