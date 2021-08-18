import spacy


class SpacyEntityExtractor:
    """
    Collect Spacy tags for a parsed SpacyDoc
    """

    def __init__(self, document) -> None:
        self.data = document
        self.tags = dict()

    def collect_tags(self) -> None:
        """
        Collect Spacy tags into organized dict

        :return:
        """

        for entry in self.data.document.doc.ents:
            if entry.label not in self.tags.keys():
                self.tags.update({
                    entry.label: list(entry.text)
                })
            else:
                self.tags[entry.label].append(entry.text)
