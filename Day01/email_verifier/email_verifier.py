# ===== TASK 2: Email Validator =====
# Create a custom InvalidEmailError exception
# The function should validate email format and raise InvalidEmailError if:
# - Email doesn't contain exactly one '@' symbol
# - Email doesn't contain at least one '.' after the '@'
# If input is empty, raise ValueError with message "Error: email cannot be empty"
# Keep asking until a valid email is entered

print("=== Task 2: Email Validator ===")
print("Email must contain '@' and a domain with '.'\n")

class InvalidEmailError(Exception):

    def __init__(self, error_msg):
        Exception.__init__(self, error_msg)
        self.error_msg = error_msg

def validate_email(prompt):
    #
    # Write your code here.
    # Define InvalidEmailError class
    # Validate email format
    # Handle exceptions and keep prompting
    #
    validating = True
    while validating:
        try:
            user_input = input(prompt)
            if user_input == "":
                raise ValueError
            elif user_input.count("@") == 0 or user_input.count("@") > 1 or user_input.index(".") < user_input.index("@"):
                raise InvalidEmailError(Exception)#remember error message when not using try - except
            else:
                return user_input
        except ValueError:
            print("Error! Email cannot be empty!")
        except InvalidEmailError:
            print("Email entered does not meet a valid email requirements!")
        except Exception:
            print("Oops! Something went wrong.")

email = validate_email("Enter your email: ")
print(f"Email accepted: {email}")
print()
