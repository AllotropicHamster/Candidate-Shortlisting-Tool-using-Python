import pandas as pd
import os

def calculate_skill_match(candidate_skills, job_skills):
    candidate_skills_list = [skill.strip() for skill in candidate_skills.split(',')]
    job_skills_list = [skill.strip() for skill in job_skills.split(',')]
    
    # Count matching skills
    matching_skills = sum(1 for skill in candidate_skills_list if skill in job_skills_list)
    total_required_skills = len(job_skills_list)
    
    # Calculate percentage match for skills
    return (matching_skills / total_required_skills) * 100 if total_required_skills > 0 else 0

def comparr(candidate_name):
    # Read CSV files
    candidates_path = os.path.join('data', 'candidates.csv')
    jobs_path = os.path.join('data', 'jobs.csv')
    
    try:
        candidates_df = pd.read_csv(candidates_path)
        jobs_df = pd.read_csv(jobs_path)
    except FileNotFoundError:
        print("Error: Make sure both candidates.csv and jobs.csv exist in the data folder")
        return []
    
    # Find the candidate
    candidate = candidates_df[candidates_df['name'].str.lower() == candidate_name.lower()]
    if candidate.empty:
        print(f"No candidate found with name: {candidate_name}")
        return []
    
    # Get candidate details
    candidate_skills = candidate['skills'].iloc[0]
    candidate_experience = candidate['experience'].iloc[0]
    candidate_qualification = candidate['qualification'].iloc[0]
    
    matches = []
    
    # Compare with each job
    for _, job in jobs_df.iterrows():
        # Calculate skill match percentage
        skill_match = calculate_skill_match(candidate_skills, job['required_skills'])
        
        # Check experience
        exp_match = candidate_experience >= job['required_experience']
        
        # Check qualification
        qual_match = candidate_qualification.lower() == job['required_qualification'].lower()
        
        # Calculate overall match percentage
        # Giving weights: Skills (50%), Experience (30%), Qualification (20%)
        overall_match = (
            skill_match * 0.5 +
            (100 if exp_match else 0) * 0.3 +
            (100 if qual_match else 0) * 0.2
        )
        
        matches.append({
            'job_name': job['job_name'],
            'match_percentage': round(overall_match, 2)
        })
    
    # Sort matches by percentage in descending order
    matches.sort(key=lambda x: x['match_percentage'], reverse=True)
    return matches

if __name__ == "__main__":
    candidate_name = input("Enter candidate name to match: ")
    matches = comparr(candidate_name)
    
    if matches:
        print("\nJob Matches:")
        for match in matches:
            print(f"Job: {match['job_name']}, Match: {match['match_percentage']}%")
