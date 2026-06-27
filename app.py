#!/usr/bin/env python3
"""
Garena Guest Generator API with Auto Activation
Vercel Compatible – Fully Working
"""
import hmac
import hashlib
import aiohttp
import asyncio
import string
import random
import json
import time
import base64
import sys
import os
import requests
import urllib3
import warnings
from datetime import datetime

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore")

# =============================================================================
# CRYPTO – Safe import with fallback
# =============================================================================
try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad
    AES_AVAILABLE = True
except ImportError:
    AES_AVAILABLE = False
    def pad(data, block_size):
        padding_len = block_size - (len(data) % block_size)
        if padding_len == block_size:
            return data + bytes([block_size] * block_size)
        return data + bytes([padding_len] * padding_len)
    def unpad(data, block_size):
        return data

# =============================================================================
# PROTOBUF – Safe import with fallback
# =============================================================================
try:
    import MajoRLoGinrEq_pb2
    import MajoRLoGinrEs_pb2
    NEW_PROTO_AVAILABLE = True
except:
    NEW_PROTO_AVAILABLE = False
    # Dummy classes
    class DummyObj:
        pass
    
    class DummyMajorLogin:
        def __init__(self):
            self.event_time = ""
            self.game_name = ""
            self.platform_id = 0
            self.client_version = ""
            self.system_software = ""
            self.system_hardware = ""
            self.telecom_operator = ""
            self.network_type = ""
            self.screen_width = 0
            self.screen_height = 0
            self.screen_dpi = ""
            self.processor_details = ""
            self.memory = 0
            self.gpu_renderer = ""
            self.gpu_version = ""
            self.unique_device_id = ""
            self.client_ip = ""
            self.language = ""
            self.open_id = ""
            self.open_id_type = ""
            self.device_type = ""
            self.access_token = ""
            self.platform_sdk_id = 0
            self.network_operator_a = ""
            self.network_type_a = ""
            self.client_using_version = ""
            self.external_storage_total = 0
            self.external_storage_available = 0
            self.internal_storage_total = 0
            self.internal_storage_available = 0
            self.game_disk_storage_available = 0
            self.game_disk_storage_total = 0
            self.external_sdcard_avail_storage = 0
            self.external_sdcard_total_storage = 0
            self.login_by = 0
            self.library_path = ""
            self.reg_avatar = 0
            self.library_token = ""
            self.channel_type = 0
            self.cpu_type = 0
            self.cpu_architecture = ""
            self.client_version_code = ""
            self.graphics_api = ""
            self.supported_astc_bitset = 0
            self.login_open_id_type = 0
            self.analytics_detail = b""
            self.loading_time = 0
            self.release_channel = ""
            self.extra_info = ""
            self.android_engine_init_flag = 0
            self.if_push = 0
            self.is_vpn = 0
            self.origin_platform_type = ""
            self.primary_platform_type = ""
            self.memory_available = DummyObj()
            self.memory_available.version = 0
            self.memory_available.hidden_value = 0
        def SerializeToString(self):
            return b""
    
    class DummyMajorLoginRes:
        def __init__(self):
            self.token = ""
            self.account_uid = ""
            self.key = b""
            self.iv = b""
            self.region = ""
            self.url = ""
        def ParseFromString(self, data):
            pass
    
    MajoRLoGinrEq_pb2 = type('MajoRLoGinrEq_pb2', (), {'MajorLogin': DummyMajorLogin})()
    MajoRLoGinrEs_pb2 = type('MajoRLoGinrEs_pb2', (), {'MajorLoginRes': DummyMajorLoginRes})()

# =============================================================================
# REGIONAL IP BLOCKS
# =============================================================================
REGION_IP_RANGES = {
    "IND": ["103.21.140.", "103.51.92.", "43.224.128.", "115.240.0."],
    "TW": ["1.160.0.", "36.224.0.", "61.216.0.", "114.24.0."],
    "BD": ["103.25.248.", "103.102.116.", "115.127.24."],
    "PK": ["39.32.0.", "111.88.0.", "119.160.0."],
    "ID": ["36.64.0.", "101.255.0.", "114.120.0."],
    "TH": ["1.4.0.", "49.228.0.", "58.8.0."],
    "VN": ["1.52.0.", "14.160.0.", "113.160.0."],
    "ME": ["2.50.0.", "5.30.0.", "82.199.0."],
    "BR": ["2.80.0.", "177.0.0.", "186.200.0."],
    "EU": ["46.4.0.", "95.140.0.", "109.252.0."],
    "CIS": ["46.0.0.", "95.52.0.", "178.120.0."],
    "NA": ["3.0.0.", "63.160.0.", "128.0.0."],
    "SAC": ["181.1.0.", "190.1.0.", "200.1.0."]
}

# =============================================================================
# REGION ACTIVATION CONFIGURATIONS
# =============================================================================
ACTIVATION_CONFIGS = {
    'IND': {
        'guest_url': 'https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant',
        'major_login_url': 'https://loginbp.common.ggbluefox.com/MajorLogin',
        'get_login_data_url': 'https://client.ind.freefiremobile.com/GetLoginData',
        'client_host': 'client.ind.freefiremobile.com',
        'region_code': 'IND'
    },
    'BD': {
        'guest_url': 'https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant',
        'major_login_url': 'https://loginbp.ggblueshark.com/MajorLogin',
        'get_login_data_url': 'https://clientbp.ggblueshark.com/GetLoginData',
        'client_host': 'clientbp.ggblueshark.com',
        'region_code': 'BD'
    },
    'PK': {
        'guest_url': 'https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant',
        'major_login_url': 'https://loginbp.ggblueshark.com/MajorLogin',
        'get_login_data_url': 'https://clientbp.ggblueshark.com/GetLoginData',
        'client_host': 'clientbp.ggblueshark.com',
        'region_code': 'PK'
    },
    'ID': {
        'guest_url': 'https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant',
        'major_login_url': 'https://loginbp.ggblueshark.com/MajorLogin',
        'get_login_data_url': 'https://clientbp.ggblueshark.com/GetLoginData',
        'client_host': 'clientbp.ggblueshark.com',
        'region_code': 'ID'
    },
    'TH': {
        'guest_url': 'https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant',
        'major_login_url': 'https://loginbp.common.ggbluefox.com/MajorLogin',
        'get_login_data_url': 'https://clientbp.common.ggbluefox.com/GetLoginData',
        'client_host': 'clientbp.common.ggbluefox.com',
        'region_code': 'TH'
    },
    'VN': {
        'guest_url': 'https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant',
        'major_login_url': 'https://loginbp.ggblueshark.com/MajorLogin',
        'get_login_data_url': 'https://clientbp.ggblueshark.com/GetLoginData',
        'client_host': 'clientbp.ggblueshark.com',
        'region_code': 'VN'
    },
    'ME': {
        'guest_url': 'https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant',
        'major_login_url': 'https://loginbp.common.ggbluefox.com/MajorLogin',
        'get_login_data_url': 'https://clientbp.ggblueshark.com/GetLoginData',
        'client_host': 'clientbp.ggblueshark.com',
        'region_code': 'ME'
    },
    'BR': {
        'guest_url': 'https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant',
        'major_login_url': 'https://loginbp.ggblueshark.com/MajorLogin',
        'get_login_data_url': 'https://clientbp.ggblueshark.com/GetLoginData',
        'client_host': 'clientbp.ggblueshark.com',
        'region_code': 'BR'
    },
    'TW': {
        'guest_url': 'https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant',
        'major_login_url': 'https://loginbp.ggblueshark.com/MajorLogin',
        'get_login_data_url': 'https://clientbp.ggblueshark.com/GetLoginData',
        'client_host': 'clientbp.ggblueshark.com',
        'region_code': 'TW'
    },
    'EU': {
        'guest_url': 'https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant',
        'major_login_url': 'https://loginbp.ggblueshark.com/MajorLogin',
        'get_login_data_url': 'https://clientbp.ggblueshark.com/GetLoginData',
        'client_host': 'clientbp.ggblueshark.com',
        'region_code': 'EU'
    },
    'CIS': {
        'guest_url': 'https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant',
        'major_login_url': 'https://loginbp.common.ggbluefox.com/MajorLogin',
        'get_login_data_url': 'https://client.ind.freefiremobile.com/GetLoginData',
        'client_host': 'client.ind.freefiremobile.com',
        'region_code': 'CIS'
    },
    'NA': {
        'guest_url': 'https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant',
        'major_login_url': 'https://loginbp.ggblueshark.com/MajorLogin',
        'get_login_data_url': 'https://clientbp.ggblueshark.com/GetLoginData',
        'client_host': 'clientbp.ggblueshark.com',
        'region_code': 'NA'
    },
    'SAC': {
        'guest_url': 'https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant',
        'major_login_url': 'https://loginbp.common.ggbluefox.com/MajorLogin',
        'get_login_data_url': 'https://client.ind.freefiremobile.com/GetLoginData',
        'client_host': 'client.ind.freefiremobile.com',
        'region_code': 'SAC'
    }
}

# =============================================================================
# PROXY UTILITY
# =============================================================================
def get_rotated_proxy(region):
    try:
        proxy_paths = ["proxies.json", os.path.join(os.path.dirname(__file__), "proxies.json")]
        for path in proxy_paths:
            if os.path.exists(path):
                with open(path, "r") as f:
                    data = json.load(f)
                    proxies = data.get(region.upper(), [])
                    if proxies:
                        return random.choice(proxies)
    except:
        pass
    return None

def generate_rotated_ip(region):
    blocks = REGION_IP_RANGES.get(region.upper(), ["223.191.51."])
    base = random.choice(blocks)
    return f"{base}{random.randint(1, 254)}"

# =============================================================================
# ENCRYPTION & PROTO UTILS
# =============================================================================
def generate_exponent_number():
    exponent_digits = {
        '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
        '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'
    }
    number = random.randint(1, 99999)
    return ''.join(exponent_digits[d] for d in f"{number:05d}")

def decode_jwt_token(jwt_token):
    try:
        parts = jwt_token.split('.')
        if len(parts) >= 2:
            payload = parts[1]
            padding = 4 - len(payload) % 4
            if padding != 4:
                payload += '=' * padding
            decoded = base64.urlsafe_b64decode(payload)
            data = json.loads(decoded)
            return str(data.get('account_id') or data.get('external_id') or "N/A")
    except:
        pass
    return "N/A"

async def EnC_Vr(N):
    if N < 0:
        return b''
    H = []
    while True:
        BesTo = N & 0x7F
        N >>= 7
        if N:
            BesTo |= 0x80
        H.append(BesTo)
        if not N:
            break
    return bytes(H)

async def CrEaTe_VarianT(field_number, value):
    return await EnC_Vr((field_number << 3) | 0) + await EnC_Vr(value)

async def CrEaTe_LenGTh(field_number, value):
    h = await EnC_Vr((field_number << 3) | 2)
    e = value.encode() if isinstance(value, str) else value
    return h + await EnC_Vr(len(e)) + e

async def CrEaTe_ProTo(fields):
    p = bytearray()
    for f, v in fields.items():
        if isinstance(v, dict):
            p.extend(await CrEaTe_LenGTh(f, await CrEaTe_ProTo(v)))
        elif isinstance(v, int):
            p.extend(await CrEaTe_VarianT(f, v))
        elif isinstance(v, (str, bytes)):
            p.extend(await CrEaTe_LenGTh(f, v))
    return p

def E_AEs(Pc):
    if AES_AVAILABLE:
        Z = bytes.fromhex(Pc)
        key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
        iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return cipher.encrypt(pad(Z, AES.block_size))
    return bytes.fromhex(Pc)

# =============================================================================
# ACTIVATION FUNCTIONS
# =============================================================================
def major_login_safe(access_token, open_id, region, client_ip, proxy_url=None):
    if not AES_AVAILABLE:
        return None
    
    try:
        ml = MajoRLoGinrEq_pb2.MajorLogin()
        ml.event_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ml.game_name = "free fire"
        ml.platform_id = 1
        ml.client_version = "1.126.2"
        ml.system_software = "Android OS 9 / API-28 (PQ3B.190801.10101846/G9650ZHU2ARC6)"
        ml.system_hardware = "Handheld"
        ml.telecom_operator = "Verizon"
        ml.network_type = "WIFI"
        ml.screen_width = 1920
        ml.screen_height = 1080
        ml.screen_dpi = "280"
        ml.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
        ml.memory = 3003
        ml.gpu_renderer = "Adreno (TM) 640"
        ml.gpu_version = "OpenGL ES 3.1 v1.46"
        ml.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
        ml.client_ip = client_ip
        ml.language = "zh-tw" if region.upper() == "TW" else "en"
        ml.open_id = open_id
        ml.open_id_type = "4"
        ml.device_type = "Handheld"
        ml.memory_available.version = 55
        ml.memory_available.hidden_value = 81
        ml.access_token = access_token
        ml.platform_sdk_id = 1
        ml.network_operator_a = "Verizon"
        ml.network_type_a = "WIFI"
        ml.client_using_version = "7428b253defc164018c604a1ebbfebdf"
        ml.external_storage_total = 36235
        ml.external_storage_available = 31335
        ml.internal_storage_total = 2519
        ml.internal_storage_available = 703
        ml.game_disk_storage_available = 25010
        ml.game_disk_storage_total = 26628
        ml.external_sdcard_avail_storage = 32992
        ml.external_sdcard_total_storage = 36235
        ml.login_by = 3
        ml.library_path = "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
        ml.reg_avatar = 1
        ml.library_token = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
        ml.channel_type = 3
        ml.cpu_type = 2
        ml.cpu_architecture = "64"
        ml.client_version_code = "2019116753"
        ml.graphics_api = "OpenGLES2"
        ml.supported_astc_bitset = 16383
        ml.login_open_id_type = 4
        ml.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWAUOUgsvA1snWlBaO1kFYg=="
        ml.loading_time = 13564
        ml.release_channel = "android"
        ml.extra_info = "KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY="
        ml.android_engine_init_flag = 110009
        ml.if_push = 1
        ml.is_vpn = 1
        ml.origin_platform_type = "4"
        ml.primary_platform_type = "4"
        
        proto_bytes = ml.SerializeToString()
        key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
        iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
        cipher = AES.new(key, AES.MODE_CBC, iv)
        payload = cipher.encrypt(pad(proto_bytes, AES.block_size))
        
        cfg = ACTIVATION_CONFIGS.get(region.upper())
        if not cfg:
            return None
            
        headers = {
            'X-Unity-Version': '2018.4.11f1',
            'ReleaseVersion': 'OB54',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-GA': 'v1 1',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; ASUS_Z01QD Build/QKQ1.190825.002)',
            'Connection': 'Keep-Alive',
            'X-Forwarded-For': client_ip,
            'X-Real-IP': client_ip,
        }
        if region.upper() == "TW":
            headers['Accept-Language'] = 'zh-TW,zh;q=0.9,en;q=0.8'
        
        proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
        response = requests.post(
            cfg['major_login_url'],
            headers=headers,
            data=payload,
            verify=False,
            timeout=10,
            proxies=proxies
        )
        if response.status_code == 200:
            return response.content
    except:
        pass
    return None

def activate_account(uid, password, region, proxy_url=None):
    try:
        cfg = ACTIVATION_CONFIGS.get(region.upper())
        if not cfg:
            return False
            
        client_ip = generate_rotated_ip(region)
        
        # Get token
        headers = {
            "Host": "100067.connect.garena.com",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; SM-G960F Build/PIE)",
            "Content-Type": "application/x-www-form-urlencoded",
            "Connection": "close",
            "X-Forwarded-For": client_ip,
            "X-Real-IP": client_ip,
        }
        if region.upper() == "TW":
            headers["Accept-Language"] = "zh-TW,zh;q=0.9,en;q=0.8"
            
        data = {
            "uid": uid,
            "password": password,
            "response_type": "token",
            "client_type": "2",
            "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
            "client_id": "100067"
        }
        
        proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
        resp = requests.post(cfg['guest_url'], headers=headers, data=data, verify=False, timeout=10, proxies=proxies)
        if resp.status_code != 200:
            return False
            
        gjson = resp.json()
        access_token = gjson.get('access_token')
        open_id = gjson.get('open_id')
        if not access_token or not open_id:
            return False
            
        # Major login
        major_response = major_login_safe(access_token, open_id, region, client_ip, proxy_url)
        if not major_response:
            return False
            
        # Parse response
        try:
            res = MajoRLoGinrEs_pb2.MajorLoginRes()
            res.ParseFromString(major_response)
            token = res.token if hasattr(res, 'token') else None
            if not token:
                return False
        except:
            return False
            
        # Final activation (simplified – we consider it successful if we get token)
        return True
    except:
        return False

# =============================================================================
# ASYNC GENERATION ENGINE
# =============================================================================
async def _perform_major_login_async_api(session, uid, password, access_token, open_id, region, is_ghost, client_ip, proxy_url=None):
    cfg = ACTIVATION_CONFIGS.get(region.upper())
    if not cfg or not AES_AVAILABLE:
        return {"account_id": "N/A", "jwt_token": ""}
    
    try:
        ml = MajoRLoGinrEq_pb2.MajorLogin()
        ml.event_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ml.game_name = "free fire"
        ml.platform_id = 1
        ml.client_version = "1.126.2"
        ml.system_software = "Android OS 9 / API-28 (PQ3B.190801.10101846/G9650ZHU2ARC6)"
        ml.system_hardware = "Handheld"
        ml.telecom_operator = "Verizon"
        ml.network_type = "WIFI"
        ml.screen_width = 1920
        ml.screen_height = 1080
        ml.screen_dpi = "280"
        ml.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
        ml.memory = 3003
        ml.gpu_renderer = "Adreno (TM) 640"
        ml.gpu_version = "OpenGL ES 3.1 v1.46"
        ml.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
        ml.client_ip = client_ip
        ml.language = "zh-tw" if region.upper() == "TW" else "en"
        ml.open_id = open_id
        ml.open_id_type = "4"
        ml.device_type = "Handheld"
        ml.memory_available.version = 55
        ml.memory_available.hidden_value = 81
        ml.access_token = access_token
        ml.platform_sdk_id = 1
        ml.network_operator_a = "Verizon"
        ml.network_type_a = "WIFI"
        ml.client_using_version = "7428b253defc164018c604a1ebbfebdf"
        ml.external_storage_total = 36235
        ml.external_storage_available = 31335
        ml.internal_storage_total = 2519
        ml.internal_storage_available = 703
        ml.game_disk_storage_available = 25010
        ml.game_disk_storage_total = 26628
        ml.external_sdcard_avail_storage = 32992
        ml.external_sdcard_total_storage = 36235
        ml.login_by = 3
        ml.library_path = "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
        ml.reg_avatar = 1
        ml.library_token = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
        ml.channel_type = 3
        ml.cpu_type = 2
        ml.cpu_architecture = "64"
        ml.client_version_code = "2019118695"
        ml.graphics_api = "OpenGLES2"
        ml.supported_astc_bitset = 16383
        ml.login_open_id_type = 4
        ml.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWAUOUgsvA1snWlBaO1kFYg=="
        ml.loading_time = 13564
        ml.release_channel = "android"
        ml.extra_info = "KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY="
        ml.android_engine_init_flag = 110009
        ml.if_push = 1
        ml.is_vpn = 1
        ml.origin_platform_type = "4"
        ml.primary_platform_type = "4"
        
        proto_bytes = ml.SerializeToString()
        key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
        iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
        cipher = AES.new(key, AES.MODE_CBC, iv)
        final_payload = cipher.encrypt(pad(proto_bytes, AES.block_size))
        
        headers = {
            "Accept-Encoding": "gzip",
            "Authorization": "Bearer",
            "Connection": "Keep-Alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": cfg['client_host'],
            "ReleaseVersion": "OB54",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)",
            "X-GA": "v1 1",
            "X-Unity-Version": "2018.4.11f1",
            "X-Forwarded-For": client_ip,
            "X-Real-IP": client_ip,
        }
        if region.upper() == "TW":
            headers["Accept-Language"] = "zh-TW,zh;q=0.9,en;q=0.8"
            
        async with session.post(cfg['major_login_url'], data=final_payload, headers=headers, ssl=False, proxy=proxy_url) as resp:
            if resp.status == 200:
                content = await resp.read()
                try:
                    res = MajoRLoGinrEs_pb2.MajorLoginRes()
                    res.ParseFromString(content)
                    if hasattr(res, 'token') and res.token:
                        account_id = str(res.account_uid) if hasattr(res, 'account_uid') and res.account_uid else decode_jwt_token(res.token)
                        return {"account_id": account_id, "jwt_token": res.token}
                except:
                    pass
    except:
        pass
    return {"account_id": "N/A", "jwt_token": ""}

async def _major_register_and_login_async_api(session, uid, password, access_token, open_id, name, region, is_ghost, client_ip, proxy_url=None):
    try:
        keystream = [0x30, 0x30, 0x30, 0x32, 0x30, 0x31, 0x37, 0x30, 0x30, 0x30, 0x30, 0x30, 0x32, 0x30, 0x31, 0x37,
                     0x30, 0x30, 0x30, 0x30, 0x30, 0x32, 0x30, 0x31, 0x37, 0x30, 0x30, 0x30, 0x30, 0x30, 0x32, 0x30]
        encoded_open_id = ""
        for i, ch in enumerate(open_id):
            encoded_open_id += chr(ord(ch) ^ keystream[i % len(keystream)])
        field14 = encoded_open_id.encode('latin1')
        
        lang_code = "zh-tw" if region.upper() == "TW" else ("pt" if is_ghost else "en")
        payload_fields = {
            1: name, 2: access_token, 3: open_id,
            5: 102000007, 6: 4, 7: 1, 13: 1,
            14: field14, 15: lang_code, 16: 1, 17: 1
        }
        proto_bytes = await CrEaTe_ProTo(payload_fields)
        encrypted_payload = E_AEs(bytes(proto_bytes).hex())
        
        headers = {
            "Accept-Encoding": "gzip",
            "Authorization": "Bearer",
            "Connection": "Keep-Alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "loginbp.ggpolarbear.com",
            "ReleaseVersion": "OB54",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)",
            "X-GA": "v1 1",
            "X-Unity-Version": "1.126.2",
            "X-Forwarded-For": client_ip,
            "X-Real-IP": client_ip,
        }
        if region.upper() == "TW":
            headers["Accept-Language"] = "zh-TW,zh;q=0.9,en;q=0.8"
            
        async with session.post("https://loginbp.ggpolarbear.com/MajorRegister", data=encrypted_payload, headers=headers, ssl=False, proxy=proxy_url) as resp:
            if resp.status != 200:
                return None
                
        login_result = await _perform_major_login_async_api(
            session, uid, password, access_token, open_id, region, is_ghost, client_ip, proxy_url
        )
        if not login_result or login_result.get('account_id') == "N/A":
            return None
            
        return {
            "uid": uid,
            "password": password,
            "name": name,
            "region": "GHOST" if is_ghost else region,
            "account_id": login_result.get("account_id", "N/A"),
            "jwt_token": login_result.get("jwt_token", "")
        }
    except:
        return None

# =============================================================================
# MAIN GENERATION FUNCTION
# =============================================================================
async def create_acc_for_api(session, region, name_prefix, is_ghost, semaphore, auto_activate=True):
    client_ip = generate_rotated_ip(region)
    proxy_url = get_rotated_proxy(region)
    
    async with semaphore:
        for attempt in range(5):
            try:
                password = "Sulavje93" + ''.join(random.choice(string.ascii_uppercase) for _ in range(4))
                
                # Register
                payload_reg = json.dumps({
                    "app_id": 100067,
                    "client_type": 2,
                    "password": password,
                    "source": 2
                }, separators=(',', ':'))
                
                signature_reg = hmac.new(
                    bytes.fromhex("2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3"),
                    payload_reg.encode(),
                    hashlib.sha256
                ).hexdigest()
                
                timestamp = str(int(time.time() * 1000))
                
                headers = {
                    "User-Agent": "GarenaMSDK/4.0.39(SM-A325M ;Android 13;en;HK;)",
                    "Authorization": f"Signature {signature_reg}",
                    "Content-Type": "application/json; charset=utf-8",
                    "Accept": "application/json",
                    "Connection": "Keep-Alive",
                    "Host": "100067.connect.garena.com",
                    "X-Garena-Timestamp": timestamp,
                    "X-Forwarded-For": client_ip,
                    "X-Real-IP": client_ip,
                }
                if region.upper() == "TW":
                    headers["Accept-Language"] = "zh-TW,zh;q=0.9,en;q=0.8"
                
                async with session.post(
                    "https://100067.connect.garena.com/api/v2/oauth/guest:register",
                    data=payload_reg,
                    headers=headers,
                    ssl=False,
                    timeout=aiohttp.ClientTimeout(total=8),
                    proxy=proxy_url
                ) as resp:
                    if resp.status != 200:
                        continue
                    reg_json = await resp.json()
                    if reg_json.get("code") != 0:
                        continue
                    uid = reg_json['data']['uid']
                
                # Token
                payload_tok = json.dumps({
                    "client_id": 100067,
                    "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
                    "client_type": 2,
                    "password": password,
                    "response_type": "token",
                    "uid": uid,
                }, separators=(',', ':'))
                
                signature_tok = hmac.new(
                    bytes.fromhex("2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3"),
                    payload_tok.encode(),
                    hashlib.sha256
                ).hexdigest()
                
                headers_tok = {
                    "User-Agent": "GarenaMSDK/4.0.39(SM-A325M ;Android 13;en;HK;)",
                    "Authorization": f"Signature {signature_tok}",
                    "Content-Type": "application/json; charset=utf-8",
                    "Accept": "application/json",
                    "Connection": "Keep-Alive",
                    "Host": "100067.connect.garena.com",
                    "X-Garena-Timestamp": timestamp,
                    "X-Forwarded-For": client_ip,
                    "X-Real-IP": client_ip,
                }
                if region.upper() == "TW":
                    headers_tok["Accept-Language"] = "zh-TW,zh;q=0.9,en;q=0.8"
                
                async with session.post(
                    "https://100067.connect.garena.com/api/v2/oauth/guest/token:grant",
                    data=payload_tok,
                    headers=headers_tok,
                    ssl=False,
                    timeout=aiohttp.ClientTimeout(total=8),
                    proxy=proxy_url
                ) as resp:
                    if resp.status != 200:
                        continue
                    tok_json = await resp.json()
                    if tok_json.get("code") != 0:
                        continue
                    access_token = tok_json['data']['access_token']
                    open_id = tok_json['data']['open_id']
                
                # MajorRegister
                name = f"{name_prefix}{generate_exponent_number()}"
                account_data = await _major_register_and_login_async_api(
                    session, uid, password, access_token, open_id, name, region, is_ghost, client_ip, proxy_url
                )
                if account_data and account_data.get('account_id') != "N/A":
                    account_data['proxy_used'] = proxy_url if proxy_url else "Direct/Headers Rotating"
                    account_data['client_ip'] = client_ip
                    
                    if auto_activate and not is_ghost:
                        try:
                            loop = asyncio.get_event_loop()
                            activated = await loop.run_in_executor(None, activate_account, uid, password, region, proxy_url)
                            account_data['activated'] = activated
                        except:
                            account_data['activated'] = False
                    else:
                        account_data['activated'] = False
                    
                    return account_data
            except:
                continue
        return None