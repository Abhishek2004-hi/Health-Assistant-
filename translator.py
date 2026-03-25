# translator.py
# Translates health advice to any language

from googletrans import Translator

# Create translator object
translator = Translator()

# Supported languages dictionary
LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Marathi": "mr",
    "Tamil": "ta",
    "Telugu": "te",
    "Bengali": "bn",
    "Gujarati": "gu",
    "Spanish": "es",
    "French": "fr",
    "Arabic": "ar"
}

def translate_text(text, target_language):
    """
    Translate text to target language
    
    Example:
    text = "Take rest and drink water"
    target = "Hindi"
    returns = "आराम करें और पानी पिएं"
    """
    try:
        # Get language code
        lang_code = LANGUAGES.get(
            target_language, "en"
        )
        
        # Translate
        result = translator.translate(
            text,
            dest=lang_code
        )
        
        return result.text
        
    except Exception as e:
        return f"Translation Error: {str(e)}"

def analyze_in_language(symptoms, language):
    """
    Analyze symptoms and return advice
    in chosen language
    """
    from health_helper import analyze_symptoms
    
    # Get English advice first
    english_advice = analyze_symptoms(symptoms)
    
    # Translate to chosen language
    if language != "English":
        translated = translate_text(
            english_advice,
            language
        )
        return translated
    
    return english_advice