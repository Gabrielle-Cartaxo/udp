import socket
import struct

def calcular_checksum_binario(mensagem):
    """
    Recebe uma mensagem (bytes), divide em blocos de 16 bits,
    soma tudo com carry-around e retorna o complemento de 1
    """
    if len(mensagem) % 2 == 1:
        mensagem += b'\x00'  # padding: se número de bytes for ímpar, adiciona zero

    soma = 0
    for i in range(0, len(mensagem), 2):
        # junta dois bytes para formar um bloco de 16 bits
        bloco = (mensagem[i] << 8) + mensagem[i+1]  # ex: 01001000 01100101
        soma += bloco

        # se passar de 16 bits, aplica carry-around (mantém só os 16 últimos bits e soma o resto)
        soma = (soma & 0xFFFF) + (soma >> 16)

    # complemento de 1 (inverte todos os bits)
    checksum = ~soma & 0xFFFF
    return checksum


# IPs e portas
ip_origem = "192.168.0.10"
ip_destino = "192.168.0.20"
porta_origem = 12345
porta_destino = 54321
mensagem = b"Hello UDP"

# Cabeçalho UDP:
# - source port (2 bytes)
# - dest port (2 bytes)
# - length (2 bytes)
# - checksum (2 bytes) ← será 0 no início
tamanho_udp = 8 + len(mensagem)  # 8 bytes do cabeçalho + dados

# Inicialmente, checksum = 0
cabecalho_sem_checksum = struct.pack('!HHHH',
    porta_origem,
    porta_destino,
    tamanho_udp,
    0  # checksum temporariamente 0
)

# ⚠️ Para calcular o checksum do UDP, o protocolo exige um pseudo-cabeçalho:
# [IP origem (4B) + IP destino (4B) + 0 (1B) + protocolo UDP (1B) + comprimento UDP (2B)]
protocolo_udp = 17  # número do protocolo UDP
pseudo_cabecalho = socket.inet_aton(ip_origem) + socket.inet_aton(ip_destino) + b'\x00' + bytes([protocolo_udp]) + struct.pack('!H', tamanho_udp)

# Dados para calcular o checksum: pseudo + cabeçalho + mensagem
dados_para_checksum = pseudo_cabecalho + cabecalho_sem_checksum + mensagem
checksum_udp = calcular_checksum_binario(dados_para_checksum)

# Monta o cabeçalho final com o checksum correto
cabecalho_udp = struct.pack('!HHHH',
    porta_origem,
    porta_destino,
    tamanho_udp,
    checksum_udp
)

# Pacote final UDP (só o cabeçalho + dados)
pacote_udp = cabecalho_udp + mensagem

# Cria socket RAW
sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)

# Envia pacote para o destino
sock.sendto(pacote_udp, (ip_destino, 0))

print(f"✔ Pacote UDP enviado de {ip_origem}:{porta_origem} para {ip_destino}:{porta_destino}")
print(f"🧮 Checksum calculado (em binário): {bin(checksum_udp)[2:].zfill(16)}")
