import hashlib
import getpass

def anonymize(text):
    # Hash the input text using SHA-256
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def main():
    print("Enter your details:")
    name = input("Name: ")
    age = input("Age: ")
    email = input("Email: ")

    # Anonymize sensitive fields
    anon_name = anonymize(name)
    anon_email = anonymize(email)

    # Store anonymized data
    with open("user_data.txt", "a") as f:
        f.write(f"Name: {anon_name}\n")
        f.write(f"Age: {age}\n")
        f.write(f"Email: {anon_email}\n")
        f.write("-" * 20 + "\n")

    print("Your data has been securely stored and anonymized.")

if __name__ == "__main__":
    main()