import requests
from bs4 import BeautifulSoup
import pandas as pd

# show all rows when you print a pandas dataframe
pd.set_option('display.max_rows', None)


def skill_extract_text(args):
    """Extracts and prints all text from the webpage at the given URL."""
    try:
        url = args[0]
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        print('Extracted text:')
        print(soup.get_text())
    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")

def skill_extract_tables(args):
    """Extracts tables from the webpage at the given URL and prints them."""
    try:
        url = args[0]
        response = requests.get(url)
        response.raise_for_status()
        dfs = pd.read_html(response.text)  # This uses BeautifulSoup under the hood
        print(f"Found {len(dfs)} tables.")
        for i, df in enumerate(dfs):
            print(f"Table {i + 1}:")
            print(df)
    except ValueError:
        print("No tables found on the page.")
    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")

def skill_extract_xml(args):
    """Extracts and prints XML structure from the webpage at the given URL."""
    try:
        url = args[0]
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'xml')  # Parse content as XML
        print('Extracted XML:')
        print(soup.prettify())
    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")