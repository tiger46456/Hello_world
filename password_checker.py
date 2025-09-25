import getpass
import sys
from utils import calculate_strength_score, provide_feedback, check_pwned_password
from colorama import init, Fore

init(autoreset=True)

def get_strength_color(score):
    if score <= 4:
        return Fore.RED
    elif score <= 7:
        return Fore.YELLOW
    else:
        return Fore.GREEN

def main():
    print("Personal Password Strength Checker")
    print("Type 'exit' or 'quit' to close.")
    print("---------------------------------")

    while True:
        try:
            password = getpass.getpass("Enter your password: ")

            if password.lower() in ["exit", "quit"]:
                print("Exiting...")
                break

            if not password:
                print(Fore.RED + "Password cannot be empty.")
                continue

            pwned_info = check_pwned_password(password)
            score = calculate_strength_score(password, pwned_info)
            feedback = provide_feedback(password)

            color = get_strength_color(score)

            print("\n--- Password Analysis ---")
            print(f"Strength Score: {color}{score}/10")

            print("\n--- Strength Feedback ---")
            for line in feedback:
                if line:
                    print(f"- {line}")

            print("\n--- Breach Check ---")
            print(f"- {pwned_info}")
            print("---------------------------\n")

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

if __name__ == "__main__":
    main()
