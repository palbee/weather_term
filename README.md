# weather_term

This is some noodling to retrieve weather data and then plot it in the terminal.

Install via: `poetry install`
## Configuration
In order to use this code some configuration is needed. The configuration is stored in `~/.weather_term.json`, and contains the following:
```json
{
  "OFFICE": "<your forecast office>",
  "GRID_X": "<the grid x for your lat/long>",
  "GRID_Y": "<the grid x for your lat/long>",
  "LAT": "<your latitude in decimal degrees to four places places>",
  "LON": "<your longitude in decimals degrees to four decimal places>",
  "OPENWEATHER_API": "<you open weather map api key>"
}
```


Please refer to the [Weather.gov API](https://www.weather.gov/documentation/services-web-api) for 
details on OFFICE, GRID_X, and GRID_Y. They may be retrieved via:

```shell
curl https://api.weather.gov/points/<lat>,<lon>
```

You can register for an OpenWeather API key at https://openweathermap.org

### Notes
The `fetch_data_weather_gov` script does not require an API key.

Currently the scripts require the [Kitty](https://sw.kovidgoyal.net/kitty/) terminal emulator.


### Screenshots
 ![Weather term running in a window.](screenshots/weather_term.png?raw=true "Weather Term")