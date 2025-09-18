import requests
from bs4 import BeautifulSoup
import csv

def scrape_motor_data(start_ranges, output_file):
    try:
        # Open the CSV file for writing
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Parameter", "Value"])

            # Loop through the specified ranges
            for start, end in start_ranges:
                for id_num in range(start, end + 1):
                    url = f"https://www.bodine-electric.com/products/dc-parallel-shaft-gearmotors/42a-fx-series-dc-parallel-shaft-scr-rated-90v-180v-gearmotors/{id_num}/"

                    try:
                        # Send a GET request to the URL
                        response = requests.get(url)
                        response.raise_for_status()  # Raise an error for bad status codes

                        # Parse the HTML content using BeautifulSoup
                        soup = BeautifulSoup(response.text, 'html.parser')

                        # Locate the table
                        table = soup.find('table')
                        if not table:
                            print(f"Table not found for ID {id_num}")
                            continue

                        # Extract table rows
                        rows = table.find_all('tr')
                        for row in rows:
                            cols = [col.text.strip() for col in row.find_all(['th', 'td'])]
                            if len(cols) == 2:  # Only keep rows with two columns (parameter and value)
                                writer.writerow([id_num] + cols)

                        # Locate the price
                        price = soup.select_one("span.price")
                        price_text = price.text.strip() if price else "Price not found"

                        # Write the price
                        writer.writerow([id_num, "Price", price_text])

                        print(f"Data successfully scraped for ID {id_num}")

                    except Exception as e:
                        print(f"An error occurred for ID {id_num}: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Ranges of IDs to scrape
start_ranges = [(1501, 1510), (5140, 5149)]

# Output CSV file name
output_file = "motor_data.csv"

# Call the function
scrape_motor_data(start_ranges, output_file)
