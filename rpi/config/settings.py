from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    serial_port: str = "/dev/ttyUSB0"
    serial_baud: int = 115200
    database_url: str = "postgresql+asyncpg://zima:password@localhost:5432/zimalab"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    usb_cam_device: str = "0"

    kasa_host: str = ""
    kasa_username: str = ""
    kasa_password: str = ""
    kasa_poll_interval: int = 10  # seconds

    influx_url: str = "http://localhost:8086"
    influx_token: str = ""
    influx_org: str = "zimalab"
    influx_bucket: str = "power"


settings = Settings()
