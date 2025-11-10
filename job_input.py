import pandas as pd
import os

def get_job_input():
    job_name = input("Enter job name: ")
    required_skills = input("Enter required skills (comma separated): ").lower()
    required_experience = int(input("Enter required years of experience: "))
    required_qualification = input("Enter required qualification: ").lower()
    
    job_data = {
        'job_name': [job_name],
        'required_skills': [required_skills],
        'required_experience': [required_experience],
        'required_qualification': [required_qualification]
    }
    
    df = pd.DataFrame(job_data)
    
    os.makedirs('data', exist_ok=True)
    
    csv_path = os.path.join('data', 'jobs.csv')
    
    if os.path.exists(csv_path):
        df.to_csv(csv_path, mode='a', header=False, index=False)
    else:
        df.to_csv(csv_path, index=False)
    
    print(f"Job data saved to {csv_path}")

if __name__ == "__main__":
    get_job_input()
