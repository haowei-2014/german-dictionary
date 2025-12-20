from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class PartOfSpeech(str, Enum):
    NOUN = "Nomen"
    VERB = "Verb"
    ADJECTIVE_ADVERB = "Adjektiv/Adverb"
    ADVERB = "Adverb"
    PRONOUN = "Pronomen"
    PREPOSITION = "Präposition"
    CONJUNCTION = "Konjunktion"
    ARTICLE = "Artikel"
    NUMERAL = "Numerale"
    INTERJECTION = "Interjektion"
    PARTICLE = "Partikel"


class ExampleSentence(BaseModel):
    german: str = Field(description="German example sentence")
    english: str = Field(description="English translation")
    chinese: str = Field(description="Chinese translation")


class Meaning(BaseModel):
    """ONE distinct meaning of the word. If a word has multiple meanings, create multiple Meaning objects."""
    english: str = Field(description="English translation for THIS meaning only.")
    chinese: str = Field(description="Chinese translation for THIS meaning only.")
    examples: list[ExampleSentence] = Field(min_length=1, description="1-3 example sentences for THIS meaning.")


class Collocation(BaseModel):
    german: str = Field(description="German collocation phrase")
    english: str = Field(description="English meaning")
    chinese: str = Field(description="Chinese meaning")


class RelatedWord(BaseModel):
    """Synonym, antonym, and relevant words of a German word."""
    german: str = Field(description="Related German word")
    english: str = Field(description="English meaning")
    chinese: str = Field(description="Chinese meaning")


class WordEntry(BaseModel):
    german: str = Field(description="The German word")
    part_of_speech: PartOfSpeech = Field(description="Part of speech")
    gender: Optional[str] = Field(default=None, description="der/die/das for nouns")
    is_separable: Optional[bool] = Field(default=None, description="True if verb is trennbar")
    meanings: list[Meaning] = Field(min_length=1, description="A German word can have multiple different meanings. Explain them in different Meaning object. The Meaning objects should be ordered by usage freqency, meaning that the first Meaning object should have the most used meaning. In each Meaning object, give translation in both English and Chinese, and give 1-3 example sentences. For each example sentence, give its meaning in both English and Chinese. ")
    collocations: list[Collocation] = Field(description="List up to 10 common collocations of the German word. For verb, consider its usage with Nominativ, Genitiv, Dativ und Akkusativ, and also reflexive usage. For each German collocation, give its meaning in both English and Chinese.")
    related_words: Optional[list[RelatedWord]] = Field(default=None, description="List its relevant words, including synonym, antonym, and relevant words. Each of synonym, antonym, and relevant words categories should have up to 3 words, and they are optional. Do not mark category, e.g., (Synonym) as part of the German word or its translation. For each German word, give its meaning in both English and Chinese.")
