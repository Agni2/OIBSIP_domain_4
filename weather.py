import requests
import json

def fetch_weather_data(api_key, place):
    base = "http://api.openweathermap.org/data/2.5/weather"
    
    if any(c.isdigit() for c in place):
        if ',' not in place:
            print("Tip: For ZIP codes, add a country code like '90210,us' or '1010,at'")
            return None
        params = {"zip": place, "appid": api_key, "units": "metric"}
    else:
        params = {"q": place, "appid": api_key, "units": "metric"}
    
    try:
        resp = requests.get(base, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        
        if data.get("cod") != 200:
            print(f"API issue: {data.get('message', 'No details')}")
            return None
        
        return data
    except requests.exceptions.RequestException as err:
        print(f"Connection error: {err}")
    except json.JSONDecodeError:
        print("Oops — couldn't parse the response properly")
    
    return None

def print_weather(info):
    if not info:
        return
    
    name = info["name"]
    country = info["sys"]["country"]
    temp = info["main"]["temp"]
    feels = info["main"]["feels_like"]
    hum = info["main"]["humidity"]
    desc = info["weather"][0]["description"].title()
    wind = info["wind"]["speed"]
    
    print("\n" + "="*45)
    print(f" Weather Update: {name}, {country} ".center(45, "-"))
    print("="*45)
    print(f"Temp: {temp}°C | Feels like: {feels}°C")
    print(f"Condition: {desc}")
    print(f"Humidity: {hum}%")
    print(f"Wind: {wind} m/s")
    print("="*45)

def main():
    API_KEY = "0f36fa11f1e644aaed1b4b2a61137d00"  
    
    print("=== Global Weather Checker ===")
    print("You can enter:")
    print("- City (e.g. 'Nairobi')")
    print("- City,country (e.g. 'Toronto,ca')")
    print("- ZIP,country (e.g. '75001,fr')\n")
    
    while True:
        query = input("Location (or 'q' to quit): ").strip()
        
        if query.lower() == 'q':
            print("Thanks for using this platform!")
            break
        
        if not query:
            print("That seemed empty — try again.")
            continue
        
        data = fetch_weather_data(API_KEY, query)
        print_weather(data)

if __name__ == "__main__":
    main()
