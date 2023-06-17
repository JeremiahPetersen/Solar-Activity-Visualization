import sunpy.map
import matplotlib.pyplot as plt
import requests
from datetime import datetime
from sunpy.net import Fido, attrs as a
import astropy.units as u
import matplotlib.colors as colors

# Define date range for data retrieval
start_date = datetime(2023, 6, 10)
end_date = datetime(2023, 6, 17)

def fetch_plot_sdo_data(start_date, end_date):
    try:
        query = Fido.search(
            a.Time(start_date, end_date),
            a.Instrument("AIA"),
            a.Wavelength(193 * u.angstrom),
            a.Sample(24 * u.hour),
        )
        files = Fido.fetch(query)
    except Exception as e:
        print(f"Error fetching SDO/AIA data: {e}")
        return

    for idx, file in enumerate(files):
        try:
            solar_map = sunpy.map.Map(file)
            plt.figure(f"SDO/AIA Data: {idx+1}")
            ax = plt.subplot(projection=solar_map)
            solar_map.plot(ax, norm=colors.LogNorm())
            ax.set_title(f"{solar_map.date} - {solar_map.instrument}")
            plt.colorbar()
            plt.show()
        except Exception as e:
            print(f"Error plotting SDO/AIA data: {e}")

def fetch_plot_donki_data(start_date, end_date, data_type, x_label, y_label, y_key):
    try:
        donki_url = f"https://api.nasa.gov/DONKI/{data_type}?start_date={start_date.strftime('%Y-%m-%d')}&end_date={end_date.strftime('%Y-%m-%d')}&api_key=DEMO_KEY"
        response = requests.get(donki_url)
        data = response.json()
    except Exception as e:
        print(f"Error fetching {data_type} data: {e}")
        return

    if not data:
        print(f"No {data_type} data available for the given date range.")
        return

    # Convert string dates to datetime objects and check if the 'start_time' key exists
    dates_and_values = [(datetime.strptime(datum["start_time"][:10], "%Y-%m-%d"), datum[y_key]) for datum in data if "start_time" in datum and y_key in datum]

    # Sort the dates before plotting
    dates_and_values.sort()

    dates = [item[0] for item in dates_and_values]
    y_values = [item[1] for item in dates_and_values]

    plt.figure(f"{data_type} Data")
    plt.scatter(dates, y_values)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(data_type)
    plt.show()

fetch_plot_sdo_data(start_date, end_date)
fetch_plot_donki_data(start_date, end_date, "FLR", "Date", "Flare Class", "class_type")
fetch_plot_donki_data(start_date, end_date, "CME", "Date", "Speed (km/s)", "speed")
