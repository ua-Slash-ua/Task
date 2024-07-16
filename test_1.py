import requests
from tabulate import tabulate


class CountryInfo:
    def __init__(self):
        self.api_url = "https://restcountries.com/v3.1/all"

    def get_country_data(self):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            countries = response.json()
            print(countries)
            country_data = []

            for country in countries:
                name = country.get("name", {}).get("common", "N/A")
                capital = country.get("capital", ["N/A"])[0] if country.get("capital") else "N/A"
                flag_url = country.get("flags", {}).get("png", "N/A")
                country_data.append([name, capital, flag_url])

            return country_data

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return []

    def display_countries_table(self):
        country_data = self.get_country_data()
        headers = ["Country Name", "Capital", "Flag URL"]
        table = tabulate(country_data, headers, tablefmt="pretty")
        print(table)


country_info = CountryInfo()
country_info.display_countries_table()
