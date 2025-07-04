# NetCat Python — Ferramenta TCP Híbrida (Cliente/Servidor)

Ferramenta de conexão remota simples, desenvolvida em Python, com suporte a:

* Execução remota de comandos
* Upload de arquivos
* Modo cliente ou servidor (híbrido, como Netcat)

Inspirada no Netcat, mas focada em automação para SOCs, Red Team e ambientes de testes.

---

## ✅ Descrição

Este projeto utiliza **um único script** que pode funcionar como:

* **Servidor (modo escuta)** — aguarda conexões e permite execução remota de comandos, shell interativa e upload de arquivos.
* **Cliente (modo ativo)** — conecta-se ao servidor e envia comandos ou arquivos.

---

## ✅ Estrutura do Projeto

```
├── netcat.py   # Script principal (cliente e servidor)
├── README.md   # Documentação
```

---

## ✅ Funcionalidades

| Funcionalidade             | Descrição                                                       |
| -------------------------- | --------------------------------------------------------------- |
| Execução de comandos       | Permite executar comandos remotamente, com resposta automática. |
| Shell remota               | Abre uma shell interativa remota no servidor.                   |
| Upload de arquivos         | Faz upload de arquivos do cliente para o servidor.              |
| Híbrido (cliente/servidor) | Funciona como cliente ou servidor, configurável via argumentos. |

---

## ✅ Pré-requisitos

* Python 3.x instalado.
* Acesso de rede entre as máquinas (localhost, VM, ou rede real).

---

## ✅ Como Usar

### 🎯 1. Executar como Servidor (escutando conexões)

```bash
python3 netcat.py -t 0.0.0.0 -p 5555 -l -c
```

Esse comando:

* Escuta na porta 5555 em todas interfaces.
* Abre uma shell remota (modo comando interativo).

Outras opções:

* Executar um comando ao receber conexão:

```bash
python3 netcat.py -t 0.0.0.0 -p 5555 -l -e "ls -la"
```

* Receber um arquivo:

```bash
python3 netcat.py -t 0.0.0.0 -p 5555 -l -u /tmp/recebido.txt
```

---

### 🎯 2. Executar como Cliente (conectando ao servidor)

#### Enviar comandos interativos:

```bash
python3 netcat.py -t <IP_DO_SERVIDOR> -p 5555
```

#### Fazer upload de arquivos:

```bash
cat arquivo.txt | python3 netcat.py -t <IP_DO_SERVIDOR> -p 5555
```

---

## ✅ Comandos e Argumentos Principais

| Argumento         | Descrição                                  |
| ----------------- | ------------------------------------------ |
| `-t`, `--target`  | IP ou hostname de destino.                 |
| `-p`, `--port`    | Porta TCP alvo.                            |
| `-l`, `--listen`  | Ativa modo servidor (escuta conexões).     |
| `-e`, `--execute` | Executa um comando específico no servidor. |
| `-c`, `--command` | Abre uma shell interativa no servidor.     |
| `-u`, `--upload`  | Salva o arquivo recebido no servidor.      |

---

## ✅ Exemplos Rápidos

| Objetivo                     | Comando Exemplo                                                |                                                    |
| ---------------------------- | -------------------------------------------------------------- | -------------------------------------------------- |
| Escutar e abrir shell remota | `python3 netcat.py -t 0.0.0.0 -p 5555 -l -c`                   |                                                    |
| Executar comando ao conectar | `python3 netcat.py -t 0.0.0.0 -p 5555 -l -e "ls -la"`          |                                                    |
| Receber arquivo              | `python3 netcat.py -t 0.0.0.0 -p 5555 -l -u /tmp/recebido.txt` |                                                    |
| Conectar como cliente        | `python3 netcat.py -t <IP_DO_SERVIDOR> -p 5555`                |                                                    |
| Enviar arquivo               | \`cat arquivo.txt                                              | python3 netcat.py -t \<IP\_DO\_SERVIDOR> -p 5555\` |

---

## ⚠️ Avisos Importantes

* **Uso restrito a ambientes de teste e laboratórios.**
* Nunca utilize em redes sem autorização explícita.
* Ferramenta educacional, para aprendizado em redes e cibersegurança.

---

## ✅ Autoria

Desenvolvido por \[Seu Nome]
Inspirado em práticas de automação de SOCs, Red Team e pentest.
