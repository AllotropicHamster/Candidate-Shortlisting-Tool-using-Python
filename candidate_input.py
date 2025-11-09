import pandas as pd
import os

def get_candidate_input():
    name = input("Enter candidate name: ")
    skills = input("Enter skills (comma separated): ").lower()
    experience = int(input("Enter years of experience: "))
    qualification = input("Enter qualification: ").lower()
    
    # Create a dictionary with the input data
    candidate_data = {
        'name': [name],
        'skills': [skills],
        'experience': [experience],
        'qualification': [qualification]
    }
    
    # Convert to DataFrame
    df = pd.DataFrame(candidate_data)
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Save to CSV
    csv_path = os.path.join('data', 'candidates.csv')
    
    # If file exists, append without header, else create new with header
    if os.path.exists(csv_path):
        df.to_csv(csv_path, mode='a', header=False, index=False)
    else:
        df.to_csv(csv_path, index=False)
    
    print(f"Candidate data saved to {csv_path}")

if __name__ == "__main__":
    get_candidate_input()
