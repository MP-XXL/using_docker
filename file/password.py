import os

password = os.getenv("PASSWORD") #or ("PASSWORD", "1234") using default env value

if password == "drone":
    print("*"*11)
    print("Correct password!")

else:
    print("#"*5)
    print("Incorrect password")

print(password)
