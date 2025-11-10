import tkinter as tk
from tkinter import ttk, messagebox
from candidate_input import get_candidate_input
from job_input import get_job_input
from job_matcher import comparr

root = tk.Tk()
root.title("Candidate Shortlisting Tool")

root.geometry("1000x700")
root.minsize(800, 500)
root.state("zoomed")  

gradient_frame = tk.Canvas(root)
gradient_frame.pack(fill="both", expand=True)

def update_gradient(event=None):
    if event:
        width = event.width
        height = event.height
    else:
        width = gradient_frame.winfo_width()
        height = gradient_frame.winfo_height()
    
    if width <= 1 or height <= 1:
        return
        
    gradient_frame.delete("all")
    
    try:
        step = max(1, height // 100)
        for i in range(0, height, 1):
            color = f"#%02x%02x%02x" % (
                max(0, min(255, 180 - i//step)),
                max(0, min(255, 200 - i//step)),
                max(0, min(255, 255 - i//step))
            )
            gradient_frame.create_line(0, i, width, i, fill=color)
        
        title_font = ("Segoe UI", 36, "bold")
        gradient_frame.create_text(width//2, height//8, 
                                 text="Candidate Shortlisting Tool",
                                 font=title_font,
                                 fill="#1a365d")
    except Exception as e:
        print(f"Error in gradient update: {e}")

gradient_frame.bind("<Configure>", update_gradient)

root.update_idletasks()
update_gradient()

main_frame = tk.Frame(gradient_frame, bg="#f7f9fc", bd=2, relief="ridge")
main_frame.place(relx=0.5, rely=0.6, anchor="center", relwidth=0.7, relheight=0.7)

notebook = ttk.Notebook(main_frame)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

frame1 = ttk.Frame(notebook)
frame2 = ttk.Frame(notebook)
frame3 = ttk.Frame(notebook)
notebook.add(frame1, text="Candidate Entry")
notebook.add(frame2, text="Recruiter Entry")
notebook.add(frame3, text="Check Matches")

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

    csv_path = os.path.join('data', 'candidates.csv')
    
    if os.path.exists(csv_path):
        existing_df = pd.read_csv(csv_path)
        if not existing_df.empty and name.lower() in existing_df['name'].str.lower().values:
            messagebox.showerror("❌ Duplicate Entry", f"Candidate '{name}' already exists!")
            return

    data = {
        'name': [name],
        'skills': [skills.lower()],
        'experience': [exp],
        'qualification': [qual.lower()]
    }
    os.makedirs('data', exist_ok=True)
    df = pd.DataFrame(data)
    if os.path.exists(csv_path):
        df.to_csv(csv_path, mode='a', header=False, index=False)
    else:
        df.to_csv(csv_path, index=False)
    messagebox.showinfo("✅ Saved", f"Candidate {name} added successfully!")

ttk.Button(frame1, text="Save Candidate", command=save_candidate).grid(row=4, column=0, columnspan=2, pady=15)

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

    csv_path = os.path.join('data', 'jobs.csv')
    
    if os.path.exists(csv_path):
        existing_df = pd.read_csv(csv_path)
        if not existing_df.empty and job.lower() in existing_df['job_name'].str.lower().values:
            messagebox.showerror("❌ Duplicate Entry", f"Job '{job}' already exists!")
            return

    data = {
        'job_name': [job],
        'required_skills': [skills.lower()],
        'required_experience': [exp],
        'required_qualification': [qual.lower()]
    }
    os.makedirs('data', exist_ok=True)
    df = pd.DataFrame(data)
    if os.path.exists(csv_path):
        df.to_csv(csv_path, mode='a', header=False, index=False)
    else:
        df.to_csv(csv_path, index=False)
    messagebox.showinfo("✅ Saved", f"Job {job} added successfully!")

ttk.Button(frame2, text="Save Job", command=save_job).grid(row=4, column=0, columnspan=2, pady=15)

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
        tree.delete(i)  

    if not matches:
        messagebox.showinfo("No Matches", f"No suitable jobs found for {candidate_name}.")
        return

    for m in matches:
        tree.insert("", "end", values=(m['job_name'], f"{m['match_percentage']}%"))

ttk.Button(frame3, text="Find Job Matches", command=check_matches).grid(row=1, column=0, columnspan=2, pady=15)

tree_container = ttk.Frame(frame3)
tree_container.grid(row=2, column=0, columnspan=2, pady=10, sticky="nsew")


frame3.grid_rowconfigure(2, weight=1)
frame3.grid_columnconfigure(0, weight=1)

columns = ("Job Name", "Match Percentage")

tree = ttk.Treeview(tree_container, columns=columns, show="headings", height=10)
tree.heading("Job Name", text="Job Name")
tree.heading("Match Percentage", text="Match Percentage")
tree.column("Job Name", anchor="center", width=350)
tree.column("Match Percentage", anchor="center", width=150)

scrollbar = ttk.Scrollbar(tree_container, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

tree.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
footer = tk.Label(root, text="Developed by Ojas, Vishnu, Arkav, Shivang and Sushil",
                  font=("Segoe UI", 10, "italic"), bg="#c8d9ff")
footer.pack(side="bottom", fill="x", pady=3)

root.mainloop()