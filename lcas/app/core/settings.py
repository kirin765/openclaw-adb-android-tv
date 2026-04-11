from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000
    redis_url: str = "redis://localhost:6379/0"
    rules_path: str = "config/rules.yaml"
    openclaw_bridge_url: str = "http://localhost:3000/openclaw/task"
    api_token: str = "change-me"
    web_base_url: str = "http://192.168.0.172:8000"
    default_android_tv_id: str = "livingroom-tv"
    default_android_tv_ip: str = "192.168.0.161"
    adb_path: str = "adb"
    allow_shell_executor: bool = False
    storage_dir: str = "storage"
    learned_rules_path: str = "storage/learned_rules.yaml"
    default_timezone: str = "Asia/Seoul"
    yonhap_rss_url: str = "https://www.yna.co.kr/rss/news.xml"
    weather_latitude: float = 37.5665
    weather_longitude: float = 126.9780
    weather_label: str = "Seoul"
    weather_units: str = "metric"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
