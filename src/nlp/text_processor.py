from abc import ABC, abstractmethod
import string

class TextProcessor(ABC):
    @abstractmethod
    def transform(self, text):
        pass


class ChangeCase(TextProcessor):
    def transform(self, text, case='lower'):
        if case.lower() ==  'lower':
            return text.lower()
        elif case.lower() == 'upper':
            return text.upper()
        elif case.lower() == 'title':
            return text.title()


class RemDigit(TextProcessor):
    def transform(self, text):
        return ''.join(char if not char.isdigit() else ' ' for char in text)


class RemPunc(TextProcessor):
    def transform(self, text):
        return ''.join(char if not char in string.punctuation else ' ' for char in text)


class RemSpaces(TextProcessor):
    def transform(self, text):
        return ' '.join(text.split())


class TextPipeline:
    def __init__(self, *arg):
        self.transformers = arg

    def transform(self, text):
        for tf in self.transformers:
            text = tf.transform(text)
        return text
    def __str__(self):
        transformers = ' -> '.join([tf.__class__.__name__ for tf in self.transformers])
        return f'Pipeline: [{transformers}]'
