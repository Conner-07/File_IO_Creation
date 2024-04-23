import csv
from operator import itemgetter

# Function to load airport data from 'Stations.csv' and create a mapping of Airport code to location
def load_airport_data(file_path):
    airport_mapping = {}
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  ###this portion skips the header
        for row in reader:
            if len(row) >= 3:
                code, city, state = row[:3]  # Only unload the first three values
                airport_mapping[code] = (city, state)
            else:
                print("Ignoring invalid row: {row}")
    return airport_mapping

# Function to compute the most popular departing and arriving cities
def compute_popular_cities(file_path, departure=True):
    city_counts = {}
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader) 
        for row in reader:
            if departure:
                city = row[1]
            else:
                city = row[2]
            if city_counts.get(city):
                city_counts[city] += 1
            else:
                city_counts[city] = 1
    return city_counts

# Function to export city data to a TSV file
def export_city_data(city_counts, airport_mapping, output_file):
    with open(output_file, 'w', newline='') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t')
        writer.writerow(['City', 'State', 'Flight Count'])
        for city, count in city_counts.items():
            writer.writerow([city] + list(airport_mapping.get(city, ('Unknown', 'Unknown'))) + [count])

# Loading data
airport_mapping = load_airport_data('/Users/connerstarkey/Downloads/Stations.csv')

departures = compute_popular_cities('/Users/connerstarkey/Downloads/CompleteData.csv', departure=True)
arrivals = compute_popular_cities('/Users/connerstarkey/Downloads/CompleteData.csv', departure=False)

num_cities = int(input("Enter the number of popular cities you would like to know about: "))

departures_sorted = sorted(departures.items(), key=itemgetter(1), reverse=True)
popular_departures = {}
for i in range(min(num_cities, len(departures_sorted))):
    popular_departures[departures_sorted[i][0]] = departures_sorted[i][1]


arrivals_sorted = sorted(arrivals.items(), key=itemgetter(1), reverse=True)
popular_arrivals = {}
for i in range(min(num_cities, len(arrivals_sorted))):
    popular_arrivals[arrivals_sorted[i][0]] = arrivals_sorted[i][1]

# Export the number of cities as separate TSV files
export_city_data(popular_departures, airport_mapping, '/Users/connerstarkey/Downloads/popular_departures.tsv')
export_city_data(popular_arrivals, airport_mapping, '/Users/connerstarkey/Downloads/popular_arrivals.tsv')

print("Files 'popular_departures.tsv' and 'popular_arrivals.tsv' have been created successfully.(Finally)")

