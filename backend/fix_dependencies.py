import subprocess
import sys
import os

def fix_project_dependencies():
    """
    This script attempts to resolve dependency conflicts and install
    all required packages from the requirements.txt file.
    """
    requirements_file = "requirements.txt"
    if not os.path.exists(requirements_file):
        print(f"Error: The file '{requirements_file}' was not found in the current directory.")
        print("Please ensure you are running this script from your project's 'backend' directory.")
        return

    print("Attempting to install all packages from requirements.txt...")
    print("This may also resolve any dependency conflicts.")

    try:
        # Use pip's install command with the requirements file.
        # The --upgrade flag ensures that existing packages are updated
        # to a version that satisfies all constraints.
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "-r", requirements_file])
        print("\nAll dependencies from requirements.txt have been successfully installed or updated.")
        print("Your project should now be able to run without 'ModuleNotFoundError's.")
    except subprocess.CalledProcessError as e:
        print(f"\nAn error occurred while installing dependencies: {e}")
        print("This may be due to complex version conflicts that pip cannot automatically resolve.")
        print("Please review the error message above for more details.")
        print("As a next step, you might need to manually inspect your requirements.txt")
        print("and the package versions to find a compatible set.")
        print("Alternatively, you can try creating a new virtual environment and running this script again.")

if __name__ == "__main__":
    fix_project_dependencies()
