import tkinter as tk
from tkinter import ttk, messagebox
from candidate_input import get_candidate_input
from job_input import get_job_input
from job_matcher import comparr

# ------------------ GUI SETUP ------------------
root = tk.Tk()
root.title("Candidate Shortlisting Tool")

# Make window resizable and start large
root.geometry("1000x700")
root.minsize(800, 500)
root.state("zoomed")  # Opens in fullscreen/maximized mode

# Gradient Background
gradient_frame = tk.Canvas(root, width=800, height=600)
gradient_frame.pack(fill="both", expand=True)

# Create gradient background
for i in range(0, 600):
    color = f"#%02x%02x%02x" % (180 - i//5, 200 - i//10, 255 - i//15)
    gradient_frame.create_line(0, i, 800, i, fill=color)

# Transparent frame over gradient
main_frame = tk.Frame(gradient_frame, bg="#f7f9fc", bd=2, relief="ridge")
main_frame.place(relx=0.5, rely=0.5, anchor="center", width=720, height=500)

# Tabs
notebook = ttk.Notebook(main_frame)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

frame1 = ttk.Frame(notebook)
frame2 = ttk.Frame(notebook)
frame3 = ttk.Frame(notebook)
notebook.add(frame1, text="Candidate Entry")
notebook.add(frame2, text="Recruiter Entry")
notebook.add(frame3, text="Check Matches")

# ------------------ Candidate Entry ------------------
ttk.Label(frame1, text="Candidate Name").grid(row=0, column=0, pady=10, padx=10)
entry_name = ttk.Entry(frame1, width=40)
entry_name.grid(row=0, column=1, pady=10)

ttk.Label(frame1, text="Skills (comma separated)").grid(row=1, column=0, pady=10, padx=10)
entry_skills = ttk.Entry(frame1, width=40)
entry_skills.grid(row=1, column=1, pady=10)

ttk.Label(frame1, text="Experience (years)").grid(row=2, column=0, pady=10, padx=10)
entry_exp = ttk.Entry(frame1, width=40)
entry_exp.grid(row=2, column=1, pady=10)

ttk.Label(frame1, text="Qualification").grid(row=3, column=0, pady=10, padx=10)
entry_qual = ttk.Entry(frame1, width=40)
entry_qual.grid(row=3, column=1, pady=10)

def save_candidate():
    import pandas as pd, os
    name = entry_name.get()
    skills = entry_skills.get()
    exp = entry_exp.get()
    qual = entry_qual.get()
    if not all([name, skills, exp, qual]):
        messagebox.showwarning("⚠️ Missing Info", "Please fill all candidate fields!")
        return
    try:
        exp = int(exp)
    except ValueError:
        messagebox.showerror("❌ Invalid Input", "Experience must be a number.")
        return

    data = {
        'name': [name],
        'skills': [skills.lower()],
        'experience': [exp],
        'qualification': [qual.lower()]
    }
    os.makedirs('data', exist_ok=True)
    csv_path = os.path.join('data', 'candidates.csv')
    df = pd.DataFrame(data)
    if os.path.exists(csv_path):
        df.to_csv(csv_path, mode='a', header=False, index=False)
    else:
        df.to_csv(csv_path, index=False)
    messagebox.showinfo("✅ Saved", f"Candidate {name} added successfully!")

ttk.Button(frame1, text="Save Candidate", command=save_candidate).grid(row=4, column=0, columnspan=2, pady=15)

# ------------------ Recruiter Entry ------------------
ttk.Label(frame2, text="Job Name").grid(row=0, column=0, pady=10, padx=10)
entry_job_name = ttk.Entry(frame2, width=40)
entry_job_name.grid(row=0, column=1, pady=10)

ttk.Label(frame2, text="Required Skills (comma separated)").grid(row=1, column=0, pady=10, padx=10)
entry_req_skills = ttk.Entry(frame2, width=40)
entry_req_skills.grid(row=1, column=1, pady=10)

ttk.Label(frame2, text="Required Experience (years)").grid(row=2, column=0, pady=10, padx=10)
entry_req_exp = ttk.Entry(frame2, width=40)
entry_req_exp.grid(row=2, column=1, pady=10)

ttk.Label(frame2, text="Required Qualification").grid(row=3, column=0, pady=10, padx=10)
entry_req_qual = ttk.Entry(frame2, width=40)
entry_req_qual.grid(row=3, column=1, pady=10)

def save_job():
    import pandas as pd, os
    job = entry_job_name.get()
    skills = entry_req_skills.get()
    exp = entry_req_exp.get()
    qual = entry_req_qual.get()
    if not all([job, skills, exp, qual]):
        messagebox.showwarning("⚠️ Missing Info", "Please fill all job fields!")
        return
    try:
        exp = int(exp)
    except ValueError:
        messagebox.showerror("❌ Invalid Input", "Experience must be a number.")
        return

    data = {
        'job_name': [job],
        'required_skills': [skills.lower()],
        'required_experience': [exp],
        'required_qualification': [qual.lower()]
    }
    os.makedirs('data', exist_ok=True)
    csv_path = os.path.join('data', 'jobs.csv')
    df = pd.DataFrame(data)
    if os.path.exists(csv_path):
        df.to_csv(csv_path, mode='a', header=False, index=False)
    else:
        df.to_csv(csv_path, index=False)
    messagebox.showinfo("✅ Saved", f"Job {job} added successfully!")

ttk.Button(frame2, text="Save Job", command=save_job).grid(row=4, column=0, columnspan=2, pady=15)

# ------------------ Check Matches ------------------
style = ttk.Style()
style.configure("Treeview", rowheight=25)
style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
style.map("Treeview", background=[("selected", "#4a90e2")])

ttk.Label(frame3, text="Candidate Name").grid(row=0, column=0, pady=10, padx=10)
entry_check_name = ttk.Entry(frame3, width=40)
entry_check_name.grid(row=0, column=1, pady=10)

def check_matches():
    candidate_name = entry_check_name.get()
    if not candidate_name:
        messagebox.showwarning("⚠️ Missing Name", "Please enter candidate name!")
        return

    matches = comparr(candidate_name)

    for i in tree.get_children():
        tree.delete(i)  # Clear old results

    if not matches:
        messagebox.showinfo("No Matches", f"No suitable jobs found for {candidate_name}.")
        return

    for m in matches:
        tree.insert("", "end", values=(m['job_name'], f"{m['match_percentage']}%"))

ttk.Button(frame3, text="Find Job Matches", command=check_matches).grid(row=1, column=0, columnspan=2, pady=15)

# Scrollable Table
# ---------------- Scrollable Table (final working version) ----------------
tree_container = ttk.Frame(frame3)
tree_container.grid(row=2, column=0, columnspan=2, pady=10, sticky="nsew")

# Configure frame to expand with window
frame3.grid_rowconfigure(2, weight=1)
frame3.grid_columnconfigure(0, weight=1)

columns = ("Job Name", "Match Percentage")

# Create Treeview
tree = ttk.Treeview(tree_container, columns=columns, show="headings", height=10)
tree.heading("Job Name", text="Job Name")
tree.heading("Match Percentage", text="Match Percentage")
tree.column("Job Name", anchor="center", width=350)
tree.column("Match Percentage", anchor="center", width=150)

# Add Scrollbar
scrollbar = ttk.Scrollbar(tree_container, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

# Pack both tree and scrollbar properly
tree.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
# ------------------ Footer ------------------
footer = tk.Label(root, text="Developed by Ojas, Vishnu, Arkav, Shivang and Sushil",
                  font=("Segoe UI", 10, "italic"), bg="#c8d9ff")
footer.pack(side="bottom", fill="x", pady=3)

# ------------------ Run App ------------------
root.mainloop()