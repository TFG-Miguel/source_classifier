import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Global variable to store an already used file path
def_file: str

def write(data, mode: str = 'a', file: str = None):
    """
    Writes data to a file. If a file path is provided in the first use of this method, 
    the next uses that address the same file can omit the path, as long as another 
    path is not used in one of the previous uses.

    Args:
        data (str): The content to write.
        mode (str, optional): File mode ('a' for append, 'w' for overwrite). Default is 'a'.
        file (str, optional): The file path. If provided, updates the global def_file.

    Example:
        write("Hello, World!", 'w', "output.txt")  # Writes to "output.txt"
        
        write("Another line")  # Appends data to the same file
    """
    if file is not None:
        global def_file
        def_file = file
    with open(def_file, mode) as f:
        f.write(f"{data}\n")

def write_csv(data: list = None, file: str = None, headers: list = None, delimiter: str = ','):
    """
    Writes a list of data to a CSV file. If column headers are provided, 
    they are written first on overwrite mode.

    Args:
        data (list, optional): The data to write. Default is None.
        file (str, optional): The file path. Default is None.
        headers (list, optional): Column headers for the CSV. Default is None.
        delimiter (str, optional): Delimiter for csv files. Default is a coma.

    Raises:
        Exception: If the number of columns does not match the data length.

    Example:
          write_csv(["John", 25], "people.csv", ["Name", "Age"])  # Writes a CSV file
          
        Other uses are:
            write_csv(headers=["Name", "Age"], file="people.csv")  # Overwrite the csv file and write the headers
            
            write_csv(["John", 25])  # Appends to the "people.csv" file
    """
    if headers is not None:
        if data is not None and len(headers) != len(data):
            raise Exception("Different number of columns between columns and data")
        write(delimiter.join(headers), 'w', file)
    if data is not None:
        write(delimiter.join(data))

def load_json(file: str) -> dict:
    """
    Loads and returns a JSON file as a dictionary.

    Args:
        file (str): The path to the JSON file.

    Returns:
        dict: The loaded JSON content.

    Example:
        data = load_json("data.json")
    """
    with open(file) as f:
        return json.load(f)

def load_data(file: str):
    """
    Loads JSON data and returns a sorted list of key-value pairs.

    Args:
        file (str): The path to the JSON file.

    Returns:
        list: A sorted list of key-value tuples from the JSON data.

    Example:
        data = load_data("data.json")
    """
    data = load_json(file)
    data = list(data.items())
    data.sort(key=lambda x: x[0])
    return data

def get_mime_type(url: str) -> str:
    """
    Retrieves the MIME type of a given URL.

    Args:
        url (str): The URL to check.

    Returns:
        str: The MIME type of the URL content, or None if the request fails.

    Example:
        mime_type = get_mime_type("https://example.com/image.png")
    """
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        mime_type = response.headers.get("Content-Type", "").split(";")[0]
        return mime_type
    except requests.RequestException:
        return None

def get_text(url: str) -> str:
    """
    Fetches and extracts the text content from a webpage.

    Args:
        url (str): The URL of the webpage.

    Returns:
        str: The extracted text content, or an empty string if the request fails.

    Example:
        page_text = get_text("https://example.com")
    """
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            return soup.get_text()
        return ""
    except requests.RequestException:
        return ""

def get_domain(url: str) -> str:
    """
    Extracts and returns the domain from a given URL.

    Args:
        url (str): The full URL.

    Returns:
        str: The domain name of the URL.

    Example:
        domain = get_domain("https://sub.example.com/page")
    """
    return urlparse(url).netloc
