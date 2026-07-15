"""Supabase 配置信息"""
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv(
    "SUPABASE_URL",
    "https://yjnczqblyucwipfanvgi.supabase.co",
)
SUPABASE_KEY = os.getenv(
    "SUPABASE_KEY",
    "sb_publishable_OBCby9Ptzrihrrto1iHsAA_KuTniWkh",
)

# REST API 基础路径
SUPABASE_REST_URL = f"{SUPABASE_URL}/rest/v1"
SUPABASE_RPC_URL = f"{SUPABASE_URL}/rest/v1/rpc"

# 请求头
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
}
