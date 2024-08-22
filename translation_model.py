# models/translation_model.py

from transformers import MarianMTModel, MarianTokenizer

def load_translation_model(source_lang="en", target_lang="es"):
    """
    Loads the translation model and tokenizer for the specified language pair.
    
    :param source_lang: Source language code (default is "en").
    :param target_lang: Target language code.
    :return: tokenizer, model
    """
    model_name = f"Helsinki-NLP/opus-mt-{source_lang}-{target_lang}"
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    return tokenizer, model
