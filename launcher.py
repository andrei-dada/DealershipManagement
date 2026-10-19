import sys
import subprocess



def main():
    print("====== LAUNCHER ======")
    print("1. Run Flask API server")
    print("2. Run CLI application")
    print("0. Exit")

    choice = input("Select an option: ")

    if choice == "1":
        print("Starting the Flask server...")
        subprocess.run([sys.executable, "app.py"])
    elif choice == "2":
        print("Starting the CLI application...")
        subprocess.run([sys.executable, "cli.py"])
    elif choice == "0":
        print("Closing application...")
        stop_db()
    else:
        print("Invalid option!")


def stop_db():
    print("\nStopping the MySQL database...")
    subprocess.run(["docker", "compose", "down"])


if __name__ == "__main__":
    main()