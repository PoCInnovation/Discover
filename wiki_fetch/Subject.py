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

    def __init__(self, page: wiki.WikipediaPage, wrapper: wiki.Wikipedia):
        self.page = page
        self.wrapper = wrapper
        self.subjects = {}

    def get_category_names(self):
        category_list = []
        for category in self.page.categories:
            category_list.append(category)
        return category_list

    def fetch_other_subjects_from_eponymous_category(self):
        category_title = "Category:" + self.page.title
        if category_title not in self.page.categories:
            return
        eponymous_category = self.page.categories[category_title]
        if eponymous_category.title not in self.subjects:
            self.subjects[eponymous_category.title] = set()
        for member in eponymous_category.categorymembers:
            self.subjects[eponymous_category.title].add(member)

    def fetch_is_keyword(self, k):
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
                    link_categories = Subject(
                        self.wrapper.page(link),
                        self.wrapper).get_category_names()
                    self_categories = self.get_category_names()
                    for index, category in enumerate(self_categories):
                        if index > k:
                            break
                        if category not in self.subjects:
                            self.subjects[category] = set()
                        if category not in link_categories:
                            self.subjects[category].add(link)
