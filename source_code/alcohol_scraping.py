import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re


def scrape_alcohol_abuse_data(url):
    """Scrape alcohol abuse statistics from the given URL."""
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        print(f"Error fetching page: {response.status_code}")
        return pd.DataFrame()

    soup = BeautifulSoup(response.text, "html.parser")
    data = []

    for section in soup.find_all(['h3', 'p']):
        text = section.text.strip()
        if section.name == 'h3' and 'Alcohol Abuse Statistics' in text:
            state_name = text.replace(' Alcohol Abuse Statistics', '').strip()
            stats_list = section.find_next_sibling('ul')

            if stats_list:
                stats = [item.text.strip() for item in stats_list.find_all('li')]

                binge_rate = median_drinks = top_25_drinks = None
                median_binge_freq = top25_binge_freq = annual_deaths = None

                for stat in stats:
                    if 'binge drink at least once per month' in stat:
                        binge_rate_match = re.search(r'([\d.]+)%', stat)
                        binge_rate = float(binge_rate_match.group(1)) if binge_rate_match else None

                    elif 'The median number of drinks per binge is' in stat:
                        parts = stat.split(';')
                        if len(parts) == 2:
                            median_drinks_match = re.search(r'The median number of drinks per binge is ([\d.]+)',
                                                            parts[0])
                            median_drinks = float(median_drinks_match.group(1)) if median_drinks_match else None
                            top_25_drinks_match = re.search(
                                r'the 25% most active drinkers consume a median ([\d.]+) drinks per binge', parts[1],
                                re.IGNORECASE)
                            top_25_drinks = float(top_25_drinks_match.group(1)) if top_25_drinks_match else None

                    elif 'binge a median' in stat:
                        parts = stat.split(';')
                        if len(parts) == 2:
                            median_binge_freq_match = re.search(r'binge a median ([\d.]+) times', parts[0])
                            median_binge_freq = float(
                                median_binge_freq_match.group(1)) if median_binge_freq_match else None
                            top25_binge_freq_match = re.search(r'the 25% most active drinkers binge ([\d.]+) times',
                                                               parts[1], re.IGNORECASE)
                            top25_binge_freq = float(
                                top25_binge_freq_match.group(1)) if top25_binge_freq_match else None

                    elif 'annual deaths' in stat:
                        annual_deaths_match = re.search(r'([\d,]+)', stat)
                        annual_deaths = int(
                            annual_deaths_match.group(1).replace(',', '')) if annual_deaths_match else None

                data.append({
                    'State': state_name,
                    'Binge Drinking (%)': binge_rate,
                    'Median Drinks per Binge': median_drinks,
                    'Top 25% Median Drinks per Binge': top_25_drinks,
                    'Median Binges Monthly': median_binge_freq,
                    'Top 25% Monthly Binges': top25_binge_freq,
                    'Annual Deaths (Excessive Alcohol)': annual_deaths
                })

    df = pd.DataFrame(data)

    # Manually append missing data
    df.loc[df['State'] == 'Georgia', 'Median Binges Monthly'] = 1.6
    df.loc[df['State'] == 'New Jersey', 'Top 25% Monthly Binges'] = 3.5

    return df


def save_data(df, filename, delimiter=','):
    """Save DataFrame to CSV or TSV."""
    raw_data_dir = os.path.join("..", "data", "raw")
    os.makedirs(raw_data_dir, exist_ok=True)
    output_file = os.path.join(raw_data_dir, filename)
    df.to_csv(output_file, sep=delimiter, index=False)
    print(f"✅ Data saved successfully at: {output_file}")


def main():
    url = "https://drugabusestatistics.org/alcohol-abuse-statistics/"
    df = scrape_alcohol_abuse_data(url)
    if not df.empty:
        save_data(df, "state_alcohol_abuse.csv", delimiter=',')
        save_data(df, "state_alcohol_abuse.tsv", delimiter='\t')


if __name__ == "__main__":
    main()