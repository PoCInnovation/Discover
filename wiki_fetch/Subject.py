# PoC Project 2023
# Discover

import wikipediaapi as wiki
from nltk.tokenize import word_tokenize


def index_of(li, val, start):
    try:
        return li.index(val, start)
    except ValueError:
        return -1


def from_keyword_to_end_of_sentence(index, summary):
    """Returns the end of the sentence of the keyword"""
    keywords_indexes = [index_of(summary, x, index) for x in ".;:"]
    end = min(filter(lambda x: x != -1, keywords_indexes))

    return summary[(index + 1):end]


class Subject():
    """Main class for subjects"""

    def __init__(self, page: wiki.WikipediaPage):
        self.page = page
        self.subjects = set()

    def fetch_other_subjects_from_eponymous_category(self):
        category_title = "Category:" + self.page.title
        if category_title not in self.page.categories:
            return
        eponymous_category = self.page.categories[category_title]
        for member in eponymous_category.categorymembers:
            self.subjects.add(member)

    def fetch_is_keyword(self):
        """Extracts pages which are linked
        following keywords such as 'is'"""
        keywords = ["is", "are", "was", "were"]
        sentences = []
        summary = word_tokenize(self.page.text)

        for index, word in enumerate(summary):
            if word in keywords:
                sentences.append(
                    from_keyword_to_end_of_sentence(index, summary)
                )

        for sentence in sentences:
            sentence_str = ' '.join(sentence).upper()
            for link in self.page.links:
                if sentence_str.find(link.upper()) != -1:
                    self.subjects.add(link)
