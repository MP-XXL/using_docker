class InvalidScore(Exception):
    pass

def grader(grade):
     score = grade
     try:
         if score < 0 or score > 100:
             raise InvalidScore
     except Exception:
         print("Invalid score entered by user!")
     except ValueError:
         print("User entered a vlaue that is not a number!")

     match score:
         case score if score >=70 and score <= 100:
             print("Your grade is A")
         case score if score >=60 and score <= 69:
             print("Your grade is B")
         case score if score >=50 and score <= 59:
             print("Your grade is C")
         case score if score >=40 and score <= 49:
             print("Your grade is D")
         case score if score >=30 and score <= 39:
             print("Your grade is E")
         case score if score >=0 and score <= 29:
             print("Your grade is F")

user_input = int(input("Enter score : "))

grader(user_input)





