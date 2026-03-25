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

def analyze_in_language(symptoms, language):
    from health_helper import analyze_symptoms
    english_advice = analyze_symptoms(symptoms)
    if language != "English":
        return translate_text(english_advice, language)
    return english_advice