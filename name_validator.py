class NameValidator:
    """
    Ensures player names are unique and not empty.
    If a name is taken or empty, we prompt again.
    """
    @staticmethod
    def validate_name(name, existing_names):
        while name in existing_names or not name.strip():
            if not name.strip():
                print("Name cannot be empty. Try again.")
            else:
                print(f"The name '{name}' is already taken.")
            name = input("Enter a different name: ").strip()
        existing_names.add(name)
        return name
