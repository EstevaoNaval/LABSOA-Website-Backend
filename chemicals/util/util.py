import re
import os
import fnmatch
import requests
from datetime import date
from random import choices
from string import digits
from django.core.exceptions import ValidationError

def find_files(directory, extension):
    """
    Traverse a directory to find all files with a specific extension.

    Parameters:
    directory (str): The directory to search in.
    extension (str): The file extension to search for.

    Returns:
    list: A list of file paths that match the given extension.
    """
    matches = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, f"*.{extension}"):
            matches.append(os.path.join(root, filename))
    return matches

def is_numeric(string: str) -> bool:
    try:
        float(string)
        return True
    except ValueError:
        return False

class ManuscriptMetadata():
    def __init__(self, doi: str) -> None:
        self.__doi = doi
        
        manuscript_metadata = self.__get_manuscript_metadata()
        
        self.__title = manuscript_metadata['title'][0]
        
        self.__publication_name = manuscript_metadata['container-title'][0]
        
        self.__publication_date = self.__get_publication_date_from_date_parts(manuscript_metadata['published']['date-parts'][0])

    def get___doi(self):
        return self.__doi
    
    def get___title(self):
        return self.__title
    
    def get___publication_name(self):
        return self.__publication_name
    
    def get___publication_date(self):
        return self.__publication_date
    
    def __get_manuscript_metadata(self):
        CROSSREF_API_URL = f'https://api.crossref.org/works/{self.__doi}'
        
        status_code = 404
        
        while status_code != 200:
            try:
                response = requests.get(CROSSREF_API_URL)
                status_code = response.status_code
            except:
                pass
        
        data = response.json()
        return data['message']

    def __get_publication_date_from_date_parts(self, date_parts: list):
        year, month, day = (date_parts + [1, 1, 1])[:3]
        return date(year, month, day)
    

def generate_random_sequence(length=10):
    return ''.join(choices(digits, k=length))

def validate_hex_color(value):
    HEXADECIMAL_COLOR_REGEX = re.compile(r'^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$', flags=re.IGNORECASE)
    
    if not HEXADECIMAL_COLOR_REGEX.fullmatch(value):
        raise ValidationError('{} is not a hexadecimal color'.format(value))
