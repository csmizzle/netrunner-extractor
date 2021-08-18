"""
Document parsers
"""

from typing import Optional
from pdfminer.high_level import extract_text
import re
from nltk.corpus import stopwords
import os
import spacy
from docx import Document
from spacy.lang.en import English
from tqdm import tqdm

# try to use spacy model, if not, download needed spacy model
try:
    nlp = spacy.load("en_core_web_lg")
except OSError:
    print('Downloading Spacy models needed for document.py')
    os.system('python -m spacy download en_core_web_lg')
    nlp = spacy.load('en_core_web_lg')


# document extractors
class SpacyDoc:
    """
    Class for string cleaning that can inherited to all document type specific

    """
    def __init__(self):
        self.nlp = English()

    def clean(self) -> Optional[str]:
        """
        cleaning pipeline for text
        :return: str
            cleaned text
        """

        if len(self.text) > 0:
            return re.sub(r'\n', ' ', self.text)

        return None

    def collect_tokens(self, length_threshold: int = 2) -> list:
        """
        output tokens for document
        :param length_threshold: int
            length of string to ignore in token output
        :return: list
        """

        return sorted(list(set([str(token.text).lower().strip()
                                for token in self.document.doc
                                if len(token.text.strip()) > length_threshold
                                if str(token.text).lower().strip() not in set(stopwords.words('english'))
                                ])))


class PDF(SpacyDoc):
    """
    Take text from PDF into a Spacy doc for future NLP work
    """

    def __init__(self, path: str) -> None:
        super().__init__()
        self.text = extract_text(path)
        self.clean_text = self.clean()
        self.document = self.nlp(self.clean_text)


class Docx(SpacyDoc):
    """
    Take text from Docx into a SpacyDoc for future NLP work
    """

    def __init__(self, path: str) -> None:
        super().__init__()
        self.docx = Document(path)
        self.text = self.extract_text()
        self.clean_text = self.clean()
        self.document = nlp(self.clean_text)

    def extract_text(self) -> str:
        text = ''

        print('Extracting text ...')
        for paragraph in tqdm(self.docx.paragraphs):
            text += paragraph.text

        return text
