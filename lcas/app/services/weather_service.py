from __future__ import annotations

import httpx

from app.models.schemas import WeatherResponse


class WeatherService:
    def __init__(self, latitude: float, longitude: float, label: str, units: str = "metric"):
        self.latitude = latitude
        self.longitude = longitude
        self.label = label
        self.units = units

    async def get_current(self) -> WeatherResponse:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "current": "temperature_2m,weather_code,wind_speed_10m,relative_humidity_2m",
            "timezone": "auto",
        }
        if self.units == "imperial":
            params["temperature_unit"] = "fahrenheit"
            params["wind_speed_unit"] = "mph"
        else:
            params["wind_speed_unit"] = "ms"
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

        current = data.get("current", {})
        return WeatherResponse(
            label=self.label,
            temperature_c=current.get("temperature_2m"),
            description=self._description_for_code(current.get("weather_code")),
            wind_speed=current.get("wind_speed_10m"),
            humidity=current.get("relative_humidity_2m"),
            observation_time=current.get("time"),
        )

    def _description_for_code(self, code: int | None) -> str:
        mapping = {
            0: "맑음",
            1: "대체로 맑음",
            2: "부분적으로 흐림",
            3: "흐림",
            45: "안개",
            48: "안개",
            51: "이슬비",
            61: "비",
            63: "비",
            65: "강한 비",
            71: "눈",
            80: "소나기",
            95: "뇌우",
        }
        return mapping.get(code, "알 수 없음")
