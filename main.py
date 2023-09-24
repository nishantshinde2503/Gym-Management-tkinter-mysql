import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

# Initialize the Tkinter window
window = tk.Tk()
window.title("Gym Management System")
window.geometry("1000x600")  # Increase window size

# Function to register a new member
def register_member():
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    membership_duration = membership_duration_var.get()
    
    # Connect to the MySQL database
    db = mysql.connector.connect(
        host="localhost",
        user="root",  # Updated username
        password="Rosary@3844",  # Updated password
        database="GymManagement"
    )
    cursor = db.cursor()

    # Insert member data into the Members table
    insert_query = "INSERT INTO Members (first_name, last_name, email, phone, join_date, membership_duration) VALUES (%s, %s, %s, %s, %s, %s)"
    join_date = datetime.now().strftime("%Y-%m-%d")
    data = (first_name, last_name, email, phone, join_date, membership_duration)
    
    cursor.execute(insert_query, data)
    db.commit()
    
    # Get the inserted member ID
    member_id = cursor.lastrowid
    
    # Close the database connection
    db.close()
    
    # Clear input fields after registration
    first_name_entry.delete(0, tk.END)
    last_name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    
    # Show member ID to the user
    messagebox.showinfo("Registration", f"Member registered successfully!\nMember ID: {member_id}")

# Function to log entry/exit time
def log_entry_exit():
    member_id = member_id_entry.get()
    
    # Connect to the MySQL database
    db = mysql.connector.connect(
        host="localhost",
        user="root",  # Updated username
        password="Rosary@3844",  # Updated password
        database="GymManagement"
    )
    cursor = db.cursor()

    # Check if this is the first time the member is logging in
    first_login_query = "SELECT entry_time FROM EntryExit WHERE member_id = %s ORDER BY entry_time ASC LIMIT 1"
    cursor.execute(first_login_query, (member_id,))
    first_login = cursor.fetchone()
    
    if first_login:
        first_login_date = first_login[0]
        membership_duration_query = "SELECT membership_duration FROM Members WHERE member_id = %s"
        cursor.execute(membership_duration_query, (member_id,))
        membership_duration = cursor.fetchone()[0]
        
        # Calculate the remaining days of membership
        current_date = datetime.now()
        remaining_days = (first_login_date + timedelta(days=membership_duration)) - current_date
        messagebox.showinfo("Membership Status", f"Membership ID: {member_id}\nRemaining Days: {remaining_days.days}")
    else:
        messagebox.showerror("Error", "Member not found or not logged in for the first time!")

    # Close the database connection
    db.close()

# Function to display member details
def display_member_details():
    member_id = member_id_display_entry.get()
    
    # Connect to the MySQL database
    db = mysql.connector.connect(
        host="localhost",
        user="root",  # Updated username
        password="Rosary@3844",  # Updated password
        database="GymManagement"
    )
    cursor = db.cursor()

    # Retrieve member details from the Members table
    select_query = "SELECT * FROM Members WHERE member_id = %s"
    cursor.execute(select_query, (member_id,))
    member = cursor.fetchone()
    
    # Close the database connection
    db.close()
    
    if member:
        details_text.config(state=tk.NORMAL)
        details_text.delete(1.0, tk.END)
        details_text.insert(tk.END, f"Member ID: {member[0]}\n")
        details_text.insert(tk.END, f"First Name: {member[1]}\n")
        details_text.insert(tk.END, f"Last Name: {member[2]}\n")
        details_text.insert(tk.END, f"Email: {member[3]}\n")
        details_text.insert(tk.END, f"Phone: {member[4]}\n")
        details_text.insert(tk.END, f"Join Date: {member[5]}\n")
        details_text.insert(tk.END, f"Membership Duration: {member[6]} months\n")  # Add membership duration
        details_text.config(state=tk.DISABLED)
    else:
        messagebox.showerror("Error", "Member not found!")

# Create a frame for the registration section on the right side
registration_frame = ttk.LabelFrame(window, text="New Member Registration", width=400)
registration_frame.pack(padx=10, pady=10, fill="both", expand=True, side="right")

# Labels and entry widgets for registration
ttk.Label(registration_frame, text="First Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
first_name_entry = ttk.Entry(registration_frame)
first_name_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(registration_frame, text="Last Name:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
last_name_entry = ttk.Entry(registration_frame)
last_name_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(registration_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
email_entry = ttk.Entry(registration_frame)
email_entry.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(registration_frame, text="Phone:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
phone_entry = ttk.Entry(registration_frame)
phone_entry.grid(row=3, column=1, padx=5, pady=5)

ttk.Label(registration_frame, text="Membership Duration:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
membership_duration_var = tk.IntVar()
membership_duration_var.set(1)  # Default to 1 month
membership_duration_options = [1, 3, 6, 12]  # Membership duration options in months
membership_duration_menu = ttk.OptionMenu(registration_frame, membership_duration_var, *membership_duration_options)
membership_duration_menu.grid(row=4, column=1, padx=5, pady=5)

# Register button
register_button = ttk.Button(registration_frame, text="Register", command=register_member)
register_button.grid(row=5, columnspan=2, pady=10)

# Create a frame for entry/exit logging section on the left side
logging_frame = ttk.LabelFrame(window, text="Entry/Exit Logging", width=400)
logging_frame.pack(padx=10, pady=10, fill="both", expand=True, side="left")

# Member ID entry widget for logging
ttk.Label(logging_frame, text="Member ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
member_id_entry = ttk.Entry(logging_frame, width=20)  # Increase width
member_id_entry.grid(row=0, column=1, padx=5, pady=5)

# Log button
log_button = ttk.Button(logging_frame, text="Log Entry/Exit", command=log_entry_exit)
log_button.grid(row=1, columnspan=2, pady=10)

# Create a frame for displaying member details
details_frame = ttk.LabelFrame(window, text="Member Details", width=400)
details_frame.pack(padx=10, pady=10, fill="both", expand=True)

# Member ID entry widget for displaying details
ttk.Label(details_frame, text="Member ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
member_id_display_entry = ttk.Entry(details_frame, width=20)  # Increase width
member_id_display_entry.grid(row=0, column=1, padx=5, pady=5)

# Display button
display_button = ttk.Button(details_frame, text="Display Details", command=display_member_details)
display_button.grid(row=1, columnspan=2, pady=10)

# Text widget for displaying member details with a larger font size
details_text = tk.Text(details_frame, height=10, width=40, state=tk.DISABLED, font=("Helvetica", 14))
details_text.grid(row=2, columnspan=2, padx=5, pady=5)

# Main loop
window.mainloop()
