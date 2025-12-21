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


class Summary(BaseModel):
    en: str = Field(description="English summary, no more than 200 characters")
    cn: str = Field(description="Chinese summary, no more than 150 characters")


class ExampleSentence(BaseModel):
    de: str = Field(description="German example sentence")
    en: str = Field(description="English translation")
    cn: str = Field(description="Chinese translation")


class Meaning(BaseModel):
    """ONE distinct meaning of the word. If a word has multiple meanings, create multiple Meaning objects."""
    en: str = Field(description="English translation for THIS meaning only.")
    cn: str = Field(description="Chinese translation for THIS meaning only.")
    examples: list[ExampleSentence] = Field(min_length=1, description="1-3 example sentences for THIS meaning.")


class Collocation(BaseModel):
    de: str = Field(description="German collocation phrase")
    en: str = Field(description="English meaning")
    cn: str = Field(description="Chinese meaning")


class RelatedWord(BaseModel):
    """Synonym, antonym, and relevant words of a German word."""
    de: str = Field(description="Related German word")
    en: str = Field(description="English meaning")
    cn: str = Field(description="Chinese meaning")


class WordEntry(BaseModel):
    """Explanation of a German word. Use de to denote German, en to denote English, use cn to denote Chinese. """
    de: str = Field(description="The German word")
    part_of_speech: PartOfSpeech = Field(description="Part of speech")
    gender: Optional[str] = Field(default=None, description="der/die/das for nouns")
    is_separable: Optional[bool] = Field(default=None, description="True if verb is trennbar")
    summary: Summary = Field(description="A short summary, summarizing its main meanings, main usages, and also important note.")
    meanings: list[Meaning] = Field(min_length=1, description="A German word can have multiple different meanings. Explain them in different Meaning object. The Meaning objects should be ordered by usage freqency, meaning that the first Meaning object should have the most used meaning. In each Meaning object, give translation in both English and Chinese, and give 1-3 example sentences. For each example sentence, give its meaning in both English and Chinese. ")
    collocations: list[Collocation] = Field(description="List up to 10 common collocations of the German word. For verb, consider its usage with Nominativ, Genitiv, Dativ und Akkusativ, and also reflexive usage. For each German collocation, give its meaning in both English and Chinese.")
    related_words: Optional[list[RelatedWord]] = Field(default=None, description="List its relevant words, including synonym, antonym, and relevant words. Each of synonym, antonym, and relevant words categories should have up to 3 words, and they are optional. Do not mark category, e.g., (Synonym) as part of the German word or its translation. For each German word, give its meaning in both English and Chinese.")
