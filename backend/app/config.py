import os
from dotenv import load_dotenv

load_dotenv()

def get_api_key() -> str:
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("请在 .env 文件中设置 DEEPSEEK_API_KEY")
    return api_key


def get_amap_key() -> str:
    key = os.getenv("AMAP_KEY", "")
    if not key:
        raise ValueError("请在 .env 文件中设置 AMAP_KEY（高德地图 Web服务 Key）")
    return key
