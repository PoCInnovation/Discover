# PoC Project 2023
# Discover

import wikipediaapi as wiki
import pandas as pd
from nltk.tokenize import word_tokenize

def get_page_from_input():
    """Returns the page from the input"""
    name = input("Enter title of wikipedia page: ")
    page = wrapper.page(name)

    if  (
            "Category:All article disambiguation pages" in page.categories or
            "Category:All disambiguation pages" in page.categories or
            "Category:Disambiguation pages" in page.categories
        ):
        print("Your input is a little vague... please choose from the following:")
        for example in page.links:
            if "Talk:" in example:
                continue
            if "Python" in example:
                print(example)
        print()
        return get_page_from_input()

    if page.exists() is True:
        print(f"Found page {name} at {page.fullurl}")
        return page

    print(f"Page {name} does not exist")
    print()
    get_page_from_input()

def index_of(li, val, start):
    try:
        return li.index(val, start)
    except ValueError:
        return -1

class Subject():
    """Main class for subjects"""
    def __init__(self, page : wiki.WikipediaPage):
        self.page = page

    def from_keyword_to_end_of_sentence(self, index, summary):
        """Returns the end of the sentence of the keyword"""
        keywords_indexes = [index_of(summary, x, index) for x in ".;:"]
        end = min(filter(lambda x: x != -1, keywords_indexes))

        return summary[(index + 1):(end)]

    def fetch_is_keyword(self):
        """Extracts pages which are linked
        following keywords such as 'is'"""
        keywords = ["is", "are", "was", "were"]
        sentences = []
        summary = word_tokenize(self.page.summary)
        print(summary)

        for index, word in enumerate(summary):
            if word in keywords:
                sentences.append(
                    self.from_keyword_to_end_of_sentence(index, summary)
                )

        for sentence in sentences:
            sentence_str = ' '.join(sentence).upper()
            print(f"{sentence_str}: ")
            for link in self.page.links:
                if sentence_str.find(link.upper()) != -1:
                    print(f"\t{link}")

        # for sentence in sentences:
        #     for link in self.page.links:
        #         if link.title in sentence:
        #             print(link)

wrapper = wiki.Wikipedia('en')

subject = Subject(get_page_from_input())
subject.fetch_is_keyword()
