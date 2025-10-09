class EmpytInputError(Exception):
    pass

def hello(prompt):
    while True:
        user_input = input(prompt).capitalize()
        try:
            if user_input == "":
                raise EmpytInputError
            else:
                print(f"Hello, {user_input}")
                print("Stay jiggy!")
                return f"Goodbye {user_input}"
        except EmpytInputError:
            print("User did not enter a valid input!")
        except Exception:
            print("Oops! Something went wrong!")


command = print(hello("Enter your name : "))
