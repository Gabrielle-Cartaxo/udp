
# 🛰️ Cliente e Servidor Raw UDP com Checksum

Olá! Este é uma atividade que desenvolvi para entender melhor o funcionamento do protocolo UDP em baixo nível, incluindo o cálculo manual do **checksum**. Aqui, tanto o cliente quanto o servidor foram implementados usando **sockets RAW** em Python, o que me deu um controle completo sobre os cabeçalhos e os dados enviados.

## Vídeo de demonstração

O vídeo de demonstração pode ser visto [AQUI]()

---

## 📦 Estrutura do Projeto

```
src/
├── client.py
└── server.py
```

---

## 🚀 Objetivo

O principal objetivo foi:

- Construir pacotes UDP manualmente (sem usar o socket UDP padrão).
- Calcular o checksum conforme especificação do protocolo.
- Validar a integridade da mensagem recebida no servidor.
- Entender como o UDP funciona de fato.

---

## ⚙️ Como funciona?

### 📤 Cliente (`cliente.py`)

Eu crio um pacote UDP do zero. Isso inclui:

1. **Cabeçalho UDP** com:
   - Porta de origem
   - Porta de destino
   - Comprimento do pacote
   - Checksum (calculado manualmente)

2. **Pseudo-cabeçalho IP**, necessário para o cálculo do checksum, composto por:
   - IP de origem
   - IP de destino
   - Protocolo (17 para UDP)
   - Tamanho do segmento UDP

3. **Mensagem/Payload**, como `"Hello via raw UDP!"`.

Eu somo todos os blocos de 16 bits (do pseudo-cabeçalho + cabeçalho UDP + payload), aplico o complemento de 1 e uso isso como checksum.

Depois disso, envio o pacote usando um socket `AF_INET, SOCK_RAW, IPPROTO_UDP`.

### 📥 Servidor (`servidor.py`)

O servidor:

1. Fica escutando com um socket RAW.
2. Quando recebe um pacote, separa:
   - Cabeçalho IP
   - Cabeçalho UDP
   - Payload

3. Reconstrói o **pseudo-cabeçalho** usando os IPs da mensagem.
4. Recalcula o checksum localmente com base nas mesmas regras.
5. Compara com o checksum que veio no pacote:
   - Se bater: imprime a mensagem
   - Se não: avisa que o checksum está incorreto

---

## 🧪 Como testar

### Pré-requisitos
- Linux (por causa dos sockets RAW)
- Python 3
- Rodar com `sudo` (sockets RAW exigem privilégio de root)

### 1. Rode o servidor
```bash
sudo python3 servidor.py
```

### 2. Em outro terminal, rode o cliente
```bash
sudo python3 cliente.py
```

---

## ✅ Exemplo de funcionamento

**Servidor:**
```
[✔] Checksum válido: 0b1010101010101010
Mensagem recebida: Hello via raw UDP!
```

**Cliente:**
```
[→] Enviando pacote para 127.0.0.1:1100
```

---

## 🤔 Por que usar o pseudo-cabeçalho no checksum?

Mesmo que ele não seja enviado, o pseudo-cabeçalho ajuda o receptor a verificar se o pacote chegou no IP certo, se o protocolo é o correto (UDP) e se o tamanho bate. Isso torna o checksum mais completo e confiável.

---
