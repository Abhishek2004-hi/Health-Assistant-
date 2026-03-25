# voice_input.py
# Converts your voice to text
# Then sends to AI for analysis

import speech_recognition as sr

def listen_to_voice():
    """
    Listen to microphone and convert to text
    
    Think of it like:
    - Open ears (microphone)
    - Listen (record audio)  
    - Understand (convert to text)
    """
    # Create recognizer object
    recognizer = sr.Recognizer()
    
    try:
        # Use microphone as source
        with sr.Microphone() as source:
            print("🎤 Listening... Speak now!")
            
            # Adjust for background noise
            recognizer.adjust_for_ambient_noise(source)
            
            # Listen for speech
            audio = recognizer.listen(
                source,
                timeout=5  # wait 5 seconds
            )
            
            print("Processing speech...")
            
            # Convert speech to text
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
            
    except sr.WaitTimeoutError:
        return "No speech detected"
    except sr.UnknownValueError:
        return "Could not understand audio"
    except Exception as e:
        return f"Error: {str(e)}"

def voice_health_check():
    """
    Full voice health check flow
    """
    from health_helper import analyze_symptoms
    
    print("Say your symptoms...")
    symptoms = listen_to_voice()
    
    if symptoms and "Error" not in symptoms:
        print(f"\nSymptoms heard: {symptoms}")
        print("Getting health advice...")
        advice = analyze_symptoms(symptoms)
        print(f"\nAdvice:\n{advice}")
        return symptoms, advice
    else:
        return None, symptoms