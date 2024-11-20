import platform

def get_user_input():
    """Prompt user for input interactively."""
    print("\nSelect commit type:")
    print("F) Fix")
    print("N) New post")
    print("U) Update")
    print("X) Major change")
    try:
        if platform.system() == "Windows":
            with open("CON", "r") as console:
                print("Reading input from CON (Windows)...")
                return console.readline().strip().upper()
        else:
            with open("/dev/tty", "r") as tty:
                print("Reading input from /dev/tty (Unix)...")
                print("Your choice: ", end="", flush=True)
                return tty.readline().strip().upper()
    except Exception as e:
        print(f"Failed to get input: {e}")
        return None

if __name__ == "__main__":
    user_input = get_user_input()
    print(f"DEBUG: User input: {user_input}")
    if user_input in ["F", "N", "U", "X"]:
        print(user_input)
    else:
        print("Invalid choice")
