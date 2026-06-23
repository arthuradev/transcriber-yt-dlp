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
