# Weather Integration

## Provider
WeatherAPI is the initial provider.

## Behavior
- Disabled by default.
- First run can enable it.
- User enters city/query and API key locally.
- Display city, temperature, condition, and local time.
- If unavailable, show discreet warning.
- Cache weather for a configurable number of minutes.

## Safety
- Do not commit API keys.
- Do not hardcode São Bernardo do Campo.
- Weather is cosmetic and must not block core app usage.

## Implementation (Phase 5)
- `core.weather.WeatherSnapshot` / `WeatherError` — pure domain types.
- `ports.weather.WeatherPort` — `fetch(query, units) -> WeatherSnapshot`.
- `adapters.weatherapi.WeatherApiAdapter` — calls `current.json`; HTTP transport
  is injectable; the API key is read from `WEATHERAPI_KEY` (env), never logged,
  and redacted from error detail.
- `application.weather.WeatherService` — TTL cache (`cache_minutes`) and graceful
  degradation: any `WeatherError` becomes `None`.
- `ui.weather` — `format_weather` / `render_weather_line` (discreet "unavailable"
  warning when `None`); the shell renders the line at the top of the header.
- Wiring lives in `__main__._build_weather_line_provider`: weather shows only when
  `enabled` and `show_on_startup`; with no key it shows the discreet warning.
