#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import socket
import struct
import time
import re
import urllib.request
import json
from datetime import datetime

# CONFIGURACIÓN ANSI ESTILO HACKER NEXUS (VERDE NEÓN, CIAN OSCURO Y ROJO CYBER)
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
except ImportError:
    class Fore:
        BLACK = '\033[30m'; RED = '\033[91m'; GREEN = '\033[92m'; YELLOW = '\033[93m'
        BLUE = '\033[34m'; MAGENTA = '\033[95m'; CYAN = '\033[36m'; WHITE = '\033[97m'
        LIGHTBLACK_EX = '\033[90m'; LIGHTRED_EX = '\033[91m'; LIGHTGREEN_EX = '\033[92m'
        LIGHTYELLOW_EX = '\033[93m'; LIGHTBLUE_EX = '\033[94m'; LIGHTMAGENTA_EX = '\033[95m'
        LIGHTCYAN_EX = '\033[96m'; LIGHTWHITE_EX = '\033[97m'; RESET = '\033[0m'
    class Style:
        BRIGHT = '\033[1m'; UNDERLINE = '\033[4m'; RESET_ALL = '\033[0m'
    class Back:
        BLUE = '\033[44m'; RESET = '\033[49m'

# TRADUCTOR DE COLORES MC § A COLORES HACKER DE LA TERMINAL
def formatear_colores_minecraft(texto):
    mapa_colores = {
        '0': Fore.BLACK, '1': Fore.BLUE, '2': Fore.GREEN, '3': Fore.CYAN,
        '4': Fore.RED, '5': Fore.MAGENTA, '6': Fore.YELLOW, '7': Fore.WHITE,
        '8': Fore.LIGHTBLACK_EX, '9': Fore.LIGHTBLUE_EX, 'a': Fore.LIGHTGREEN_EX,
        'b': Fore.LIGHTCYAN_EX, 'c': Fore.LIGHTRED_EX, 'd': Fore.LIGHTMAGENTA_EX,
        'e': Fore.LIGHTYELLOW_EX, 'f': Fore.WHITE, 'r': Fore.RESET
    }
    partes = re.split(r'§([0-9a-fk-or])', texto, flags=re.IGNORECASE)
    resultado = ""
    color_actual = Fore.RESET
    for i, parte in enumerate(partes):
        if i % 2 == 1:
            color_actual = mapa_colores.get(parte.lower(), Fore.RESET)
        else:
            resultado += color_actual + parte
    return resultado + Fore.RESET

# BANNER COMPACTO, ELEGANTE, ESTILO NEXUS TERMINAL
BANNER = f"""
{Fore.CYAN}☠️ ═════════════════════════════════════════════════════════════ ☠️
{Fore.GREEN}   _  _______  ___  VM   _  _______ _   _ _   _ _   _ ____  
{Fore.GREEN}  | |/ /  _  \/ _ \ / _ \ | |/ /  ___| | | | | | | | / ___| 
{Fore.CYAN}  | ' /| | | / /_\ / /_\ \| ' /| |__ | |_| | |_| | | \___ \ 
{Fore.CYAN}  | . \| | | |  _  |  _  || . \|  __||  _  |  _  | | |___) |
{Fore.GREEN}  |_|\_\_| |_|_| |_|_| |_|_|\_\____|_| |_|_| |_|_| |_|____/ 
{Fore.CYAN}              [ NEXUS CYBER ARCH ARCHITECTURE v12.0 ]
{Fore.CYAN}☠️ ═════════════════════════════════════════════════════════════ ☠️
"""

# SISTEMA DE LOGEO - SOLO EL DUEÑO ENTRA
def sistema_login():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(BANNER)
    print(f"{Fore.CYAN}[🔒 SYSTEM] ACCESO RESTRINGIDO - INGRESE CREDENCIALES")
    
    usuario = input(f"{Fore.GREEN}👤 USER: {Fore.WHITE}").strip()
    password = input(f"{Fore.GREEN}🔑 PASS: {Fore.WHITE}").strip()
    
    if usuario == "admin" and password == "admin1234":
        print(f"\n{Fore.GREEN}[🔓 ACCESS GRANTED] Inicializando Kernel Nexus...")
        time.sleep(1)
        return True
    else:
        print(f"\n{Fore.RED}[🚨 ACCESS DENIED] Credenciales Incorrectas. Abortando.")
        time.sleep(1.5)
        sys.exit(1)

class NexusMonitor:
    def __init__(self, target_host, port):
        self.target_host = target_host
        self.port = port
        self.numeric_ip = "Calculando..."
        self.provider = "Escaneando..."
        self.provider_url = "N/A"
        
        self.raw_motd = "Desconocido"
        self.version = "Desconocida"
        self.protocol = "Desconocido"
        self.jugadores_count = 0
        self.max_jugadores = 0
        self.api_software = "Buscando..."
        self.ping_ms = 0
        self.players_list = []
        
        # Historial de estados y DDoS
        self.hora_encendido = "---"
        self.hora_apagado = "---"
        self.ultimo_estado = None 
        self.conteo_fallas = 0
        self.cyber_status = "STABLE" # STABLE, UNDER ATTACK, OFFLINE_DDOS
        
        self.MAGIC = b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78'

    def rastrear_infraestructura(self):
        try:
            self.numeric_ip = socket.gethostbyname(self.target_host)
        except:
            self.numeric_ip = self.target_host

        # Diccionario Inteligente con las empresas solicitadas por el usuario
        try:
            url = f"http://ip-api.com/json/{self.numeric_ip}?fields=status,org,isp"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=3.0) as response:
                res_data = json.loads(response.read().decode())
                if res_data.get("status") == "success":
                    org = res_data.get("org") or res_data.get("isp") or "Desconocido"
                    self.provider = org
                    org_low = org.lower()
                    
                    if "ovh" in org_low: self.provider_url = "https://www.ovhcloud.com"
                    elif "aternos" in org_low: self.provider_url = "https://aternos.org"
                    elif "shock" in org_low: self.provider_url = "https://shockbyte.com"
                    elif "falix" in org_low or "felix" in org_low: self.provider_url = "https://falixnodes.net"
                    elif "holy" in org_low: self.provider_url = "https://holynodes.com"
                    elif "leme" in org_low: self.provider_url = "https://lemehost.com"
                    elif "bean" in org_low: self.provider_url = "https://beanshosting.com"
                    elif "opti" in org_low: self.provider_url = "https://optilink.net"
                    else:
                        self.provider_url = "N/A (Host Privado)"
        except:
            self.provider = "Local / Shield Proxy"
            self.provider_url = "N/A"

    def interrogar_servidor(self):
        hora_mexico = datetime.now().strftime("%I:%M:%S %p")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(1.2)
            
            packet = bytearray()
            packet.extend(b'\x01')
            packet.extend(struct.pack('>Q', int(time.time())))
            packet.extend(self.MAGIC)
            packet.extend(b'\x00' * 8)
            
            t_start = time.time()
            sock.sendto(bytes(packet), (self.numeric_ip, self.port))
            data, addr = sock.recvfrom(4096)
            self.ping_ms = int((time.time() - t_start) * 1000)
            sock.close()
            
            if data and len(data) > 35:
                self.conteo_fallas = 0
                self.cyber_status = "✅ STABLE / ONLINE"
                
                info_str = data[35:].decode('utf-8', errors='ignore')
                campos = info_str.split(';')
                
                if len(campos) >= 6:
                    antiguo_count = self.jugadores_count
                    self.raw_motd = campos[1]
                    self.protocol = campos[2]
                    
                    if self.protocol in ['45', '46', '47', '48']:
                        self.version = "0.14.x Clásico"
                    elif self.protocol in ['70', '71', '72', '80']:
                        self.version = "0.15.x Clásico"
                    else:
                        self.version = campos[3]
                        
                    try: self.jugadores_count = int(campos[4])
                    except: self.jugadores_count = 0
                    try: self.max_jugadores = int(campos[5])
                    except: self.max_jugadores = 0
                    
                    if "astral" in info_str.lower(): self.api_software = "Astral API Core"
                    elif len(campos) > 7: self.api_software = campos[7]
                    else: self.api_software = "PocketMine-MP"
                    
                    # Extraer nombres reales de los players expuestos en el buffer
                    self.players_list = []
                    for c in campos[6:]:
                        c_clean = re.sub(r'§[0-9a-fk-or]', '', c).strip()
                        if c_clean and not c_clean.isdigit() and c_clean != self.api_software and len(c_clean) > 2:
                            if c_clean not in self.players_list: self.players_list.append(c_clean)

                    if self.ultimo_estado is not True:
                        self.hora_encendido = hora_mexico
                        self.ultimo_estado = True
                    
                    alerta = ""
                    if antiguo_count != self.jugadores_count:
                        alerta = f"[📡 NETWORK EVENT] Jugadores actuales cambiaron a: {self.jugadores_count} / {self.max_jugadores}"
                    return True, alerta
        except socket.timeout:
            self.conteo_fallas += 1
        except:
            self.conteo_fallas += 1
            
        # Algoritmo de Detección de Ataques / Estado DDoS
        if self.conteo_fallas == 1:
            self.cyber_status = "⚠️ SERVER BAJO ATAQUE (LAG / FLOOD)"
        elif self.conteo_fallas >= 2:
            if self.ultimo_estado is True:
                self.hora_apagado = hora_mexico
                self.ultimo_estado = False
            self.cyber_status = "🚨 SERVER OFF / CAUSA DDOS"
            
        return False, ""

    def dibujar_interfaz(self, online, alerta=""):
        os.system('clear' if os.name == 'posix' else 'cls')
        print(BANNER)
        
        # Estado de Jugabilidad por Ping
        if not online: play_status = f"{Fore.RED}IMPOSIBLE JUGAR"
        elif self.ping_ms < 90: play_status = f"{Fore.GREEN}EXCELENTE PARA JUGAR AHORITA"
        elif self.ping_ms < 190: play_status = f"{Fore.YELLOW}JUGABLE (LAG MODERADO)"
        else: play_status = f"{Fore.RED}MUCHO RETRASO / INESTABLE"

        print(f"{Fore.GREEN}⚡ ESTADO DIGITAL: {self.cyber_status}")
        print(f"{Fore.CYAN}🌐 IP REAL:       {Fore.WHITE}{self.numeric_ip}:{self.port}")
        print(f"{Fore.CYAN}🏢 PROVEEDOR:     {Fore.GREEN}{self.provider} {Fore.LIGHTBLACK_EX}({self.provider_url})")
        print(f"{Fore.CYAN}⏱️  HORARIOS MX:   {Fore.GREEN}ON: {self.hora_encendido} {Fore.CYAN}| {Fore.RED}OFF: {self.hora_apagado}")
        print(f"{Fore.CYAN}🔌 LATENCIA PING: {Fore.YELLOW}{self.ping_ms} ms {Fore.CYAN}({play_status}{Fore.CYAN})")
        
        print(f"{Fore.GREEN}─────────────────────────────────────────────────────────────")
        motd_fix = formatear_colores_minecraft(self.raw_motd) if online else f"{Fore.RED}Offline"
        print(f"{Fore.CYAN}📝 MOTD NATIVO:   {motd_fix}")
        print(f"{Fore.CYAN}⚙️  API CORE:      {Fore.WHITE}{self.api_software} {Fore.LIGHTBLACK_EX}({self.version})")
        print(f"{Fore.CYAN}👥 CONTADOR:      {Fore.YELLOW}{self.jugadores_count} / {self.max_jugadores}")
        
        print(f"{Fore.GREEN}─────────────────────────────────────────────────────────────")
        print(f"{Fore.GREEN}[👥 JUGADORES EN LÍNEA INTERNOS]:")
        if online and self.players_list:
            print(f"{Fore.WHITE}, ".join(self.players_list))
        elif online:
            print(f"{Fore.LIGHTBLACK_EX}Ninguno dentro o el Core oculta el Query.")
        else:
            print(f"{Fore.RED}Servidor caído. Datos inaccesibles.")
            
        if alerta:
            print(f"\n{Fore.YELLOW}🔥 {alerta}")

def main():
    if not sistema_login():
        return

    default_ip = "15.204.51.206"
    default_port = 16942

    print(f"\n{Fore.LIGHTBLACK_EX}ENTER para usar {default_ip}:{default_port}")
    ip_in = input(f"{Fore.GREEN}👾 IP/DOMINIO: {Fore.WHITE}").strip()
    if not ip_in: ip_in = default_ip

    port_in = input(f"{Fore.GREEN}👾 PUERTO:     {Fore.WHITE}").strip()
    port = int(port_in) if port_in.isdigit() else default_port

    monitor = NexusMonitor(ip_in, port)
    monitor.rastrear_infraestructura()
    
    try:
        while True:
            is_on, evento = monitor.interrogar_servidor()
            monitor.dibujar_interfaz(is_on, evento)
            time.sleep(1.2)
    except KeyboardInterrupt:
        print(f"\n{Fore.GREEN}[✅] Nexus Monitor Desconectado De Forma Segura.{Fore.RESET}\n")

if __name__ == "__main__":
    main()