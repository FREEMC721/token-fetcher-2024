# Create and write to requirements.txt
with open("requirements.txt", "w") as req_file:
    # List of required packages
    packages = [
        "requests==2.31.0",  # Versioned dependency for requests
        "colorama==0.4.6"    # Versioned dependency for colorama
    ]
    
    # Write each package to the file
    for package in packages:
        req_file.write(package + "\n")

print("requirements.txt created successfully.")
