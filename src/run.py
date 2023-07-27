from pathlib import Path
from typing import Union

from nlp.text_processor import (ChangeCase, RemDigit, RemPunc, RemSpaces,
                                    TextPipeline)


class Search:
    def __init__(self, documents_path: Union[str, Path], stop_words: str = None):

        # Crawl data
        self.data = self.crawl(documents_path)

        # Load processor
        self.pipe = TextPipeline(ChangeCase(), RemDigit(), RemPunc(), RemSpaces())

        # Load stop words
        if stop_words is None:
            stop_words = open('data/stop_words.txt').read().split('\n')
        self.stop_words = stop_words
        stop_words = set(map(self.pipe.transform, stop_words))

        # Index data
        self.index = self.index_data()


    def crawl(self, documents_path: Union[str, Path]):
        data = {}

        for doc_path in Path(documents_path).iterdir():
            if doc_path.suffix != '.txt':
                continue

            with open(doc_path) as f:
                doc_name = doc_path.stem.replace('_', ' ').title()
                data[doc_name] = f.read()
        return data

    def index_data(self, ):

        index = {}
        for doc_name, doc_content in self.data.items():
            for word in doc_content.split():
                word = self.pipe.transform(word)
                if not word:
                    continue
                if word in self.stop_words:
                    continue
                if word in index:
                    index[word].add(doc_name)
                else:
                    index[word] = {doc_name}
        return index

    def search(self, query):
        while True:
            query = self.pipe.transform(query)
            search_tokens = query.split()
            docs = []
            for token in search_tokens:
                docs.extend(self.index.get(token, []))
            return docs

if __name__ == '__main__':
    searcher  = Search('data/documents')
    while True:
        query = input('Search to find your docs (q to quit): ')
        if query.lower() == 'q':
            break

        docs = searcher.search(query)
        print(docs)