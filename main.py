from candidate_input import get_candidate_input
from job_input import get_job_input
from job_matcher import comparr
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_menu():
    print("\n=== Job Matching System ===")
    print("1. I am a Candidate (Enter Details)")
    print("2. I am a Recruiter (Enter Job Details)")
    print("3. Check Job Matches for a Candidate")
    print("4. Exit")
    print("========================")

def main():
    while True:
        clear_screen()
        print_menu()
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            clear_screen()
            print("=== Candidate Details Entry ===")
            get_candidate_input()
            input("\nPress Enter to continue...")
            
        elif choice == '2':
            clear_screen()
            print("=== Job Details Entry ===")
            get_job_input()
            input("\nPress Enter to continue...")
            
        elif choice == '3':
            clear_screen()
            print("=== Check Job Matches ===")
            candidate_name = input("Enter candidate name to check matches: ")
            matches = comparr(candidate_name)
            
            if matches:
                print("\nJob Matches for", candidate_name)
                print("------------------------")
                for match in matches:
                    print(f"Job: {match['job_name']}")
                    print(f"Match Percentage: {match['match_percentage']}%")
                    print("------------------------")
            input("\nPress Enter to continue...")
            
        elif choice == '4':
            print("\nThank you for using the Job Matching System!")
            break
            
        else:
            print("\nInvalid choice! Please try again.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()