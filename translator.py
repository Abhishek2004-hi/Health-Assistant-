import requests

LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Marathi": "mr",
    "Tamil": "ta",
    "Telugu": "te",
    "Bengali": "bn",
    "Spanish": "es",
    "French": "fr"
}

def translate_text(text, target_language):
    try:
        lang_code = LANGUAGES.get(target_language, "en")
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "auto",
            "tl": lang_code,
            "dt": "t",
            "q": text
        }
        response = requests.get(url, params=params)
        result = response.json()
        return result[0][0][0]
    except Exception as e:
        return f"Translation Error: {str(e)}"

from health_helper import ask_groq, analyze_symptoms

def analyze_in_language(symptoms, language, age=25, gender="unknown"):
    """
    Analyze symptoms and return result in selected language
    """
    # Get english analysis first
    english_advice = analyze_symptoms(symptoms, age, gender)
    
    # If language is English, return directly
    if language.lower() == "english":
        return english_advice
    
    # Translate to selected language
    translated = ask_groq(f"""
    Translate the following medical advice to {language}.
    Keep all medical terms accurate.
    
    Text to translate:
    {english_advice}
    """)
    
    return translated