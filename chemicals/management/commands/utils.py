import os
import fnmatch
from habanero import Crossref
from datetime import date

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
        
        self.__title = manuscript_metadata['message']['title'][0]
        
        self.__publication_name = manuscript_metadata['message']['container-title'][0]
        
        self.__publication_date = self.__get_publication_date_from_date_parts(manuscript_metadata['message']['published']['date-parts'][0])

    def get___doi(self):
        return self.__doi
    
    def get___title(self):
        return self.__title
    
    def get___publication_name(self):
        return self.__publication_name
    
    def get___publication_date(self):
        return self.__publication_date

    def __get_manuscript_metadata(self):
        cr = Crossref()

        manuscript_metadata = cr.works(ids=self.__doi)

        return manuscript_metadata

    def __get_publication_date_from_date_parts(self, date_parts: list):
        year, month, day = (date_parts + [1, 1, 1])[:3]
        return date(year, month, day)