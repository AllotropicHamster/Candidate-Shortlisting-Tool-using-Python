# Candidate-Shortlisting-Tool-using-Python

> 🎯 A handy Python tool to help you quickly shortlist job candidates — because hiring should be smart, not slow.

## 📌 What is this?

This project is a **Candidate Shortlisting Tool** built in Python. You input candidate details and job requirements, and the tool helps match and score candidates — making your hiring workflow smoother, faster and more data-driven.

## 🧩 Why use it?

- 🚀 Speeds up the initial screening of candidates  
- 📊 Quantifies match between job requirements & candidate profile  
- 🎨 Has a simple GUI (so it's easy and simple to use)  
- ✅ Helps bring consistency and objectivity to early-stage shortlisting  

## 🛠 How it works (at a high level)

1. You provide **job requirement** details (skills, experience, keywords, etc).  
2. You enter **candidate** profiles (skills, past roles, education, etc).  
3. The tool computes a match score (or similar metric) using the core logic.  
4. The GUI presents the results so you can pick the best fits.  

## 📂 Project structure

```text
.
├── data/               # sample job- and candidate-data (CSV/JSON etc)
├── candidate_input.py  # script to input candidate data
├── job_input.py        # script to input job requirement data
├── job_matcher.py      # core matching logic
├── gui_main.py         # graphical interface to use the tool
└── README.md           # (that’s this file!)
