import os

user_input = input("Enter file name : ")

with open(user_input, "+a") as file:
    file.write("HOLA DOCKER!")

print(user_input)

password = os.getenv("PASSWORD") #or ("PASSWORD", "1234") using default env value

if password == "drone":
    print("*"*11)
    print("Correct password!")

else:
    print("#"*5)
    print("Incorrect password")

print(password)
