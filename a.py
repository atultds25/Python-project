import json
import urllib.request

API_URL = "https://open.er-api.com/v6/latest/USD"
CACHE_FILE = "rates.json"

# Predefined rates (1 USD = x currency)
DEFAULT_RATES = {"USD": 1.0, "INR": 83.0,
                 "EUR": 0.92, "GBP": 0.79, "JPY": 150.0}


def load_rates():
    try:  # 1) real-time rates from API
        with urllib.request.urlopen(
                API_URL, timeout=5) as r:
            rates = json.load(r)["rates"]
        with open(CACHE_FILE, "w") as f:
            json.dump(rates, f)  # save a copy
        print("Using real-time exchange rates")
        return rates
    except Exception:
        try:  # 2) last saved rates
            with open(CACHE_FILE) as f:
                print("Using saved rates from file")
                return json.load(f)
        except (FileNotFoundError, ValueError):
            print("Using predefined rates")
            return DEFAULT_RATES  # 3) default


def convert(amount, src, dst, rates):
    return amount / rates[src] * rates[dst]


def main():
    rates = load_rates()
    print("Available:", ", ".join(list(rates)[:5]))
    try:
        src = input("From currency: ").upper()
        dst = input("To currency: ").upper()
        amount = float(input("Amount: "))
        result = convert(amount, src, dst, rates)
        print(f"{amount:.2f} {src} = {result:.2f} {dst}")
    except KeyError:
        print("Error: currency not supported")
    except ValueError:
        print("Error: enter a valid number")


main()