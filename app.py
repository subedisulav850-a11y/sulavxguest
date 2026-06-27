#!/usr/bin/env python3
"""
Garena Guest Generator API with Auto Activation
Professional Version - Fully Vercel Compatible
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
from typing import Dict, Any, Optional, List, Union
import threading
from concurrent.futures import ThreadPoolExecutor

# =============================================================================
# ENVIRONMENT DETECTION
# =============================================================================
IS_VERCEL = bool(os.environ.get('VERCEL') or os.environ.get('NOW'))
IS_SERVERLESS = bool(os.environ.get('AWS_LAMBDA') or os.environ.get('VERCEL'))

# =============================================================================
# DISABLE SSL WARNINGS
# =============================================================================
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore")

# =============================================================================
# PROTOBUF FALLBACK - Handles missing proto files gracefully
# =============================================================================
try:
    import MajoRLoGinrEq_pb2
    import MajoRLoGinrEs_pb2
    NEW_PROTO_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    NEW_PROTO_AVAILABLE = False
    
    # Dummy classes for when proto files are missing
    class DummyMemoryAvailable:
        version = 0
        hidden_value = 0
    
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
            self.memory_available = DummyMemoryAvailable()
        
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
# CRYPTO FALLBACK
# =============================================================================
try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad
    AES_AVAILABLE = True
except ImportError:
    AES_AVAILABLE = False
    def pad(data: bytes, block_size: int) -> bytes:
        padding_len = block_size - (len(data) % block_size)
        if padding_len == block_size:
            return data + bytes([block_size] * block_size)
        return data + bytes([padding_len] * padding_len)
    
    def unpad(data: bytes, block_size: int) -> bytes:
        return data

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
def get_rotated_proxy(region: str) -> Optional[str]:
    """Reads proxies.json and returns a single rotated proxy URL for the region"""
    try:
        # Check multiple possible locations for proxies.json
        proxy_paths = [
            "proxies.json",
            os.path.join(os.path.dirname(__file__), "proxies.json"),
            os.path.join(os.getcwd(), "proxies.json")
        ]
        
        for proxy_path in proxy_paths:
            if os.path.exists(proxy_path):
                with open(proxy_path, "r") as f:
                    data = json.load(f)
                    proxies_list = data.get(region.upper(), [])
                    if proxies_list:
                        return random.choice(proxies_list)
    except Exception:
        pass
    return None

def generate_rotated_ip(region: str) -> str:
    """Generates a random, valid IP address based on the region's subnet blocks"""
    blocks = REGION_IP_RANGES.get(region.upper(), ["223.191.51."])
    base = random.choice(blocks)
    return f"{base}{random.randint(1, 254)}"

# =============================================================================
# ENCRYPTION & PROTO UTILS
# =============================================================================
def generate_exponent_number() -> str:
    """Generate a random 5-digit number with superscript formatting"""
    exponent_digits = {
        '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
        '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'
    }
    number = random.randint(1, 99999)
    return ''.join(exponent_digits[d] for d in f"{number:05d}")

def decode_jwt_token(jwt_token: str) -> str:
    """Decode JWT token to extract account ID"""
    try:
        parts = jwt_token.split('.')
        if len(parts) >= 2:
            payload_part = parts[1]
            padding = 4 - len(payload_part) % 4
            if padding != 4:
                payload_part += '=' * padding
            decoded = base64.urlsafe_b64decode(payload_part)
            data = json.loads(decoded)
            return str(data.get('account_id') or data.get('external_id') or "N/A")
    except:
        pass
    return "N/A"

async def EnC_Vr(N: int) -> bytes:
    """Encode variable integer for protobuf"""
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

async def CrEaTe_VarianT(field_number: int, value: int) -> bytes:
    """Create protobuf variant field"""
    return await EnC_Vr((field_number << 3) | 0) + await EnC_Vr(value)

async def CrEaTe_LenGTh(field_number: int, value) -> bytes:
    """Create protobuf length-delimited field"""
    h = await EnC_Vr((field_number << 3) | 2)
    e = value.encode() if isinstance(value, str) else value
    return h + await EnC_Vr(len(e)) + e

async def CrEaTe_ProTo(fields: dict) -> bytes:
    """Create protobuf message from fields"""
    p = bytearray()
    for f, v in fields.items():
        if isinstance(v, dict):
            p.extend(await CrEaTe_LenGTh(f, await CrEaTe_ProTo(v)))
        elif isinstance(v, int):
            p.extend(await CrEaTe_VarianT(f, v))
        elif isinstance(v, (str, bytes)):
            p.extend(await CrEaTe_LenGTh(f, v))
    return p

def E_AEs(Pc: str) -> bytes:
    """AES encryption"""
    if AES_AVAILABLE:
        Z = bytes.fromhex(Pc)
        key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
        iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
        K = AES.new(key, AES.MODE_CBC, iv)
        return K.encrypt(pad(Z, AES.block_size))
    return bytes.fromhex(Pc)

# =============================================================================
# ACTIVATION CORE
# =============================================================================
def build_safe_major_login_payload(open_id: str, access_token: str, region: str, client_ip: str) -> Optional[bytes]:
    """Build encrypted MajorLogin protobuf payload"""
    if not AES_AVAILABLE:
        return None
    try:
        major_login = MajoRLoGinrEq_pb2.MajorLogin()
        major_login.event_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        major_login.game_name = "free fire"
        major_login.platform_id = 1
        major_login.client_version = "1.126.2"
        major_login.system_software = "Android OS 9 / API-28 (PQ3B.190801.10101846/G9650ZHU2ARC6)"
        major_login.system_hardware = "Handheld"
        major_login.telecom_operator = "Verizon"
        major_login.network_type = "WIFI"
        major_login.screen_width = 1920
        major_login.screen_height = 1080
        major_login.screen_dpi = "280"
        major_login.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
        major_login.memory = 3003
        major_login.gpu_renderer = "Adreno (TM) 640"
        major_login.gpu_version = "OpenGL ES 3.1 v1.46"
        major_login.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
        major_login.client_ip = client_ip
        major_login.language = "zh-tw" if region.upper() == "TW" else "en"
        major_login.open_id = open_id
        major_login.open_id_type = "4"
        major_login.device_type = "Handheld"
        major_login.memory_available.version = 55
        major_login.memory_available.hidden_value = 81
        major_login.access_token = access_token
        major_login.platform_sdk_id = 1
        major_login.network_operator_a = "Verizon"
        major_login.network_type_a = "WIFI"
        major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
        major_login.external_storage_total = 36235
        major_login.external_storage_available = 31335
        major_login.internal_storage_total = 2519
        major_login.internal_storage_available = 703
        major_login.game_disk_storage_available = 25010
        major_login.game_disk_storage_total = 26628
        major_login.external_sdcard_avail_storage = 32992
        major_login.external_sdcard_total_storage = 36235
        major_login.login_by = 3
        major_login.library_path = "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
        major_login.reg_avatar = 1
        major_login.library_token = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
        major_login.channel_type = 3
        major_login.cpu_type = 2
        major_login.cpu_architecture = "64"
        major_login.client_version_code = "2019116753"
        major_login.graphics_api = "OpenGLES2"
        major_login.supported_astc_bitset = 16383
        major_login.login_open_id_type = 4
        major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWAUOUgsvA1snWlBaO1kFYg=="
        major_login.loading_time = 13564
        major_login.release_channel = "android"
        major_login.extra_info = "KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY="
        major_login.android_engine_init_flag = 110009
        major_login.if_push = 1
        major_login.is_vpn = 1
        major_login.origin_platform_type = "4"
        major_login.primary_platform_type = "4"
        
        proto_bytes = major_login.SerializeToString()
        key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
        iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return cipher.encrypt(pad(proto_bytes, AES.block_size))
    except Exception:
        return None

def major_login_safe(access_token: str, open_id: str, region: str, client_ip: str, proxy_url: Optional[str] = None) -> Optional[bytes]:
    """Perform safe major login"""
    payload = build_safe_major_login_payload(open_id, access_token, region, client_ip)
    if not payload:
        return None
    
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
    try:
        proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
        response = requests.post(
            cfg['major_login_url'], 
            headers=headers, 
            data=payload, 
            verify=False, 
            timeout=10, 
            proxies=proxies
        )
        if response.status_code == 200 and len(response.content) > 0:
            return response.content
    except Exception:
        pass
    return None

def parse_safe_major_login_response(response_bytes: bytes) -> Optional[Dict]:
    """Parse MajorLogin response"""
    try:
        res = MajoRLoGinrEs_pb2.MajorLoginRes()
        res.ParseFromString(response_bytes)
        return {
            'token': res.token,
            'key': res.key.hex() if hasattr(res, 'key') and res.key else None,
            'iv': res.iv.hex() if hasattr(res, 'iv') and res.iv else None,
            'region': res.region if hasattr(res, 'region') else None,
            'url': res.url if hasattr(res, 'url') else None
        }
    except Exception:
        return None

def build_get_login_data_payload(jwt_token: str, access_token: str, region: str, client_ip: str) -> Optional[bytes]:
    """Build GetLoginData payload"""
    if not AES_AVAILABLE:
        return None
    try:
        token_payload_base64 = jwt_token.split('.')[1]
        token_payload_base64 += '=' * ((4 - len(token_payload_base64) % 4) % 4)
        decoded_payload = base64.urlsafe_b64decode(token_payload_base64).decode('utf-8')
        payload_dict = json.loads(decoded_payload)
        external_id = payload_dict['external_id']
        signature_md5 = payload_dict['signature_md5']
        
        major_login = MajoRLoGinrEq_pb2.MajorLogin()
        major_login.event_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        major_login.game_name = "free fire"
        major_login.platform_id = 1
        major_login.client_version = "1.126.2"
        major_login.system_software = "Android OS 9 / API-28 (PQ3B.190801.10101846/G9650ZHU2ARC6)"
        major_login.system_hardware = "Handheld"
        major_login.telecom_operator = "Verizon"
        major_login.network_type = "WIFI"
        major_login.screen_width = 1920
        major_login.screen_height = 1080
        major_login.screen_dpi = "280"
        major_login.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
        major_login.memory = 3003
        major_login.gpu_renderer = "Adreno (TM) 640"
        major_login.gpu_version = "OpenGL ES 3.1 v1.46"
        major_login.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
        major_login.client_ip = client_ip
        major_login.language = "zh-tw" if region.upper() == "TW" else "en"
        major_login.open_id = external_id
        major_login.open_id_type = "4"
        major_login.device_type = "Handheld"
        major_login.memory_available.version = 55
        major_login.memory_available.hidden_value = 81
        major_login.access_token = access_token
        major_login.platform_sdk_id = 1
        major_login.network_operator_a = "Verizon"
        major_login.network_type_a = "WIFI"
        major_login.client_using_version = signature_md5
        major_login.external_storage_total = 36235
        major_login.external_storage_available = 31335
        major_login.internal_storage_total = 2519
        major_login.internal_storage_available = 703
        major_login.game_disk_storage_available = 25010
        major_login.game_disk_storage_total = 26628
        major_login.external_sdcard_avail_storage = 32992
        major_login.external_sdcard_total_storage = 36235
        major_login.login_by = 3
        major_login.library_path = "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
        major_login.reg_avatar = 1
        major_login.library_token = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
        major_login.channel_type = 3
        major_login.cpu_type = 2
        major_login.cpu_architecture = "64"
        major_login.client_version_code = "2019116753"
        major_login.graphics_api = "OpenGLES2"
        major_login.supported_astc_bitset = 16383
        major_login.login_open_id_type = 4
        major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWAUOUgsvA1snWlBaO1kFYg=="
        major_login.loading_time = 13564
        major_login.release_channel = "android"
        major_login.extra_info = "KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY="
        major_login.android_engine_init_flag = 110009
        major_login.if_push = 1
        major_login.is_vpn = 1
        major_login.origin_platform_type = "4"
        major_login.primary_platform_type = "4"
        
        proto_bytes = major_login.SerializeToString()
        key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
        iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return cipher.encrypt(pad(proto_bytes, AES.block_size))
    except Exception:
        return None

def get_login_data_safe(jwt_token: str, access_token: str, base_url: str, region: str, client_ip: str, proxy_url: Optional[str] = None) -> bool:
    """Perform GetLoginData request"""
    payload = build_get_login_data_payload(jwt_token, access_token, region, client_ip)
    if not payload:
        return False
    
    cfg = ACTIVATION_CONFIGS.get(region.upper())
    if not cfg:
        return False
        
    url = f"{base_url}/GetLoginData"
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'X-Unity-Version': '2018.4.11f1',
        'X-GA': 'v1 1',
        'ReleaseVersion': 'OB54',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; G011A Build/PI)',
        'Connection': 'close',
        'X-Forwarded-For': client_ip,
        'X-Real-IP': client_ip,
    }
    if region.upper() == "TW":
        headers['Accept-Language'] = 'zh-TW,zh;q=0.9,en;q=0.8'
    try:
        proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
        response = requests.post(
            url, 
            headers=headers, 
            data=payload, 
            verify=False, 
            timeout=10, 
            proxies=proxies
        )
        return response.status_code == 200
    except Exception:
        return False

def activate_account(uid: str, password: str, region: str, proxy_url: Optional[str] = None) -> bool:
    """Activate account using region-specific configuration"""
    cfg = ACTIVATION_CONFIGS.get(region.upper())
    if not cfg:
        return False
        
    client_ip = generate_rotated_ip(region)
    
    # Step 1: Guest token
    guest_headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; SM-G960F Build/PIE)",
        "Content-Type": "application/x-www-form-urlencoded",
        "Connection": "close",
        "X-Forwarded-For": client_ip,
        "X-Real-IP": client_ip,
    }
    if region.upper() == "TW":
        guest_headers["Accept-Language"] = "zh-TW,zh;q=0.9,en;q=0.8"
        
    guest_data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"
    }
    try:
        proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
        resp = requests.post(
            cfg['guest_url'], 
            headers=guest_headers, 
            data=guest_data, 
            verify=False, 
            timeout=10, 
            proxies=proxies
        )
        if resp.status_code != 200:
            return False
        gjson = resp.json()
        access_token = gjson.get('access_token')
        open_id = gjson.get('open_id')
        if not access_token or not open_id:
            return False
            
        # Step 2: Major Login
        major_response = major_login_safe(access_token, open_id, region, client_ip, proxy_url)
        if not major_response:
            return False
            
        # Step 3: Parse response
        login_data = parse_safe_major_login_response(major_response)
        if not login_data or not login_data.get('token'):
            return False
            
        # Step 4: Get Login Data (Final activation step)
        return get_login_data_safe(
            login_data['token'], 
            access_token, 
            login_data['url'] or cfg['get_login_data_url'], 
            region, 
            client_ip, 
            proxy_url
        )
    except Exception:
        return False

# =============================================================================
# ASYNC GUEST GENERATION ENGINE
# =============================================================================
def _encrypt_major_login_proto(open_id: str, access_token: str, region: str, client_ip: str) -> Optional[bytes]:
    """Encrypt major login protobuf"""
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
        
        serialized = ml.SerializeToString()
        key_b = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
        iv_b = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
        cipher = AES.new(key_b, AES.MODE_CBC, iv_b)
        return cipher.encrypt(pad(serialized, AES.block_size))
    except Exception:
        return None

async def _perform_major_login_async_api(session, uid: str, password: str, access_token: str, open_id: str, region: str, is_ghost: bool, client_ip: str, proxy_url: Optional[str] = None) -> Dict:
    """Async major login"""
    cfg = ACTIVATION_CONFIGS.get(region.upper())
    if not cfg:
        return {"account_id": "N/A", "jwt_token": ""}
        
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
        headers["User-Agent"] = "Dalvik/2.1.0 (Linux; U; Android 9; TW; Taiwan)"
        
    final_payload = _encrypt_major_login_proto(open_id, access_token, region, client_ip)
    if final_payload is None:
        return {"account_id": "N/A", "jwt_token": ""}
        
    try:
        async with session.post(
            cfg['major_login_url'], 
            data=final_payload, 
            headers=headers, 
            ssl=False,
            proxy=proxy_url
        ) as resp:
            if resp.status == 200:
                content = await resp.read()
                try:
                    res = MajoRLoGinrEs_pb2.MajorLoginRes()
                    res.ParseFromString(content)
                    if hasattr(res, 'token') and res.token:
                        account_id = str(res.account_uid) if hasattr(res, 'account_uid') and res.account_uid else decode_jwt_token(res.token)
                        return {"account_id": account_id, "jwt_token": res.token}
                except Exception:
                    pass
                text = content.decode('utf-8', errors='ignore')
                jwt_start = text.find("eyJ")
                if jwt_start != -1:
                    jwt_token = text[jwt_start:]
                    second_dot = jwt_token.find(".", jwt_token.find(".") + 1)
                    if second_dot != -1:
                        jwt_token = jwt_token[:second_dot + 44]
                        account_id = decode_jwt_token(jwt_token)
                        return {"account_id": account_id, "jwt_token": jwt_token}
    except Exception:
        pass
    return {"account_id": "N/A", "jwt_token": ""}

async def _major_register_and_login_async_api(session, uid: str, password: str, access_token: str, open_id: str, name: str, region: str, is_ghost: bool, client_ip: str, proxy_url: Optional[str] = None) -> Optional[Dict]:
    """Async major register and login"""
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
        headers_reg = {
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
            headers_reg["Accept-Language"] = "zh-TW,zh;q=0.9,en;q=0.8"
            
        async with session.post(
            "https://loginbp.ggpolarbear.com/MajorRegister", 
            data=encrypted_payload, 
            headers=headers_reg, 
            ssl=False,
            proxy=proxy_url
        ) as resp:
            if resp.status != 200:
                return None
                
        login_result = await _perform_major_login_async_api(
            session, uid, password, access_token, open_id, region, is_ghost, client_ip, proxy_url
        )
        if login_result is None:
            return None
            
        return {
            "uid": uid,
            "password": password,
            "name": name,
            "region": "GHOST" if is_ghost else region,
            "account_id": login_result.get("account_id", "N/A"),
            "jwt_token": login_result.get("jwt_token", "")
        }
    except Exception:
        return None

# =============================================================================
# GENERATE ACCOUNT WITH AUTO ACTIVATION
# =============================================================================
async def create_acc_for_api(session, region: str, name_prefix: str, is_ghost: bool, semaphore, auto_activate: bool = True) -> Optional[Dict]:
    """Generate account with auto activation"""
    client_ip = generate_rotated_ip(region)
    proxy_url = get_rotated_proxy(region)
    
    async with semaphore:
        for attempt in range(5):
            try:
                password = "Sulavje93" + ''.join(random.choice(string.ascii_uppercase) for _ in range(4))
                
                # STEP 1: Register
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
                
                headers_reg = {
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
                    headers_reg["Accept-Language"] = "zh-TW,zh;q=0.9,en;q=0.8"
                
                async with session.post(
                    "https://100067.connect.garena.com/api/v2/oauth/guest:register", 
                    data=payload_reg, 
                    headers=headers_reg, 
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
                
                # STEP 2: Token
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
                
                # STEP 3: MajorRegister
                name = f"{name_prefix}{generate_exponent_number()}"
                account_data = await _major_register_and_login_async_api(
                    session, uid, password, access_token, open_id, name, region, is_ghost, client_ip, proxy_url
                )
                if account_data and account_data.get('account_id') != "N/A":
                    account_data['proxy_used'] = proxy_url if proxy_url else "Direct/Headers Rotating"
                    account_data['client_ip'] = client_ip
                    
                    # STEP 4: Auto Activate if enabled
                    if auto_activate and not is_ghost:
                        try:
                            # Use ThreadPoolExecutor for sync activation
                            with ThreadPoolExecutor(max_workers=1) as executor:
                                future = executor.submit(activate_account, uid, password, region, proxy_url)
                                activated = future.result(timeout=15)
                            account_data['activated'] = activated
                        except Exception:
                            account_data['activated'] = False
                    else:
                        account_data['activated'] = False
                    
                    return account_data
            except Exception:
                continue
        return None

# =============================================================================
# EXPORT FOR VERCEL
# =============================================================================
__all__ = [
    'ACTIVATION_CONFIGS',
    'REGION_IP_RANGES',
    'generate_rotated_ip',
    'get_rotated_proxy',
    'create_acc_for_api',
    'decode_jwt_token',
    'generate_exponent_number',
    'IS_VERCEL',
    'IS_SERVERLESS'
]