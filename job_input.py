import pandas as pd
import os

def get_job_input():
    job_name = input("Enter job name: ")
    required_skills = input("Enter required skills (comma separated): ").lower()
    required_experience = int(input("Enter required years of experience: "))
    required_qualification = input("Enter required qualification: ").lower()
    
    # Create a dictionary with the input data
    job_data = {
        'job_name': [job_name],
        'required_skills': [required_skills],
        'required_experience': [required_experience],
        'required_qualification': [required_qualification]
    }
    
    # Convert to DataFrame
    df = pd.DataFrame(job_data)
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Save to CSV
    csv_path = os.path.join('data', 'jobs.csv')
    
    # If file exists, append without header, else create new with header
    if os.path.exists(csv_path):
        df.to_csv(csv_path, mode='a', header=False, index=False)
    else:
        df.to_csv(csv_path, index=False)
    
    print(f"Job data saved to {csv_path}")

if __name__ == "__main__":
    get_job_input()
