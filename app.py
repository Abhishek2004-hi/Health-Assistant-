# app.py
# This is the simple terminal version
# Run this to use in command line

from health_helper import (
    analyze_symptoms,
    get_diet_advice,
    get_exercise_advice,
    check_medicine_info,
    emergency_check
)

def print_header():
    """Print the app header"""
    print("\n" + "="*50)
    print("   🏥 Personal Health Assistant")
    print("="*50)
    print("⚠️  This is NOT a replacement for real doctors!")
    print("="*50 + "\n")

def print_menu():
    """Print the main menu"""
    print("\n📋 What do you need help with?")
    print("1. Analyze my symptoms")
    print("2. Get diet advice")
    print("3. Get exercise advice")
    print("4. Medicine information")
    print("5. Emergency check")
    print("6. Exit")
    print("-"*30)

def main():
    """Main function - runs the app"""
    print_header()
    
    while True:  # Keep running until user exits
        print_menu()
        
        # Get user choice
        choice = input("Enter your choice (1-6): ")
        
        # Option 1: Analyze Symptoms
        if choice == "1":
            print("\n🔍 Symptom Analyzer")
            print("-"*30)
            symptoms = input("Describe your symptoms: ")
            print("\n⏳ Analyzing your symptoms...")
            result = analyze_symptoms(symptoms)
            print("\n💊 Health Advice:")
            print("-"*30)
            print(result)
        
        # Option 2: Diet Advice
        elif choice == "2":
            print("\n🥗 Diet Advisor")
            print("-"*30)
            condition = input("Enter your health condition: ")
            print("\n⏳ Getting diet advice...")
            result = get_diet_advice(condition)
            print("\n🥗 Diet Advice:")
            print("-"*30)
            print(result)
        
        # Option 3: Exercise Advice
        elif choice == "3":
            print("\n🏃 Exercise Advisor")
            print("-"*30)
            condition = input("Enter your health condition: ")
            print("\n⏳ Getting exercise advice...")
            result = get_exercise_advice(condition)
            print("\n🏋️ Exercise Advice:")
            print("-"*30)
            print(result)
        
        # Option 4: Medicine Info
        elif choice == "4":
            print("\n💊 Medicine Information")
            print("-"*30)
            medicine = input("Enter medicine name: ")
            print("\n⏳ Getting medicine information...")
            result = check_medicine_info(medicine)
            print("\n💊 Medicine Info:")
            print("-"*30)
            print(result)
        
        # Option 5: Emergency Check
        elif choice == "5":
            print("\n🚨 Emergency Checker")
            print("-"*30)
            symptoms = input("Describe your symptoms: ")
            print("\n⏳ Checking emergency level...")
            result = emergency_check(symptoms)
            print("\n🚨 Emergency Status:")
            print("-"*30)
            print(result)
        
        # Option 6: Exit
        elif choice == "6":
            print("\n👋 Stay healthy! Goodbye!")
            break
        
        else:
            print("❌ Invalid choice! Please enter 1-6")

# Run the app
if __name__ == "__main__":
    main()