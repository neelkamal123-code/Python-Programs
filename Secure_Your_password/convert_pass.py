import string
import random

random.seed(0)

combination = list(string.ascii_letters + string.digits + string.punctuation)
random.shuffle(combination)
uppercaseal = string.ascii_uppercase
lowercaseal = string.ascii_lowercase
digits = string.digits

SECUREUPPER = tuple((i,random.choice(combination)) for i in uppercaseal)
SECURELOWER = tuple((i,random.choice(combination)) for i in lowercaseal)
SECUREDIGITS = tuple((i,random.choice(combination)) for i in digits)

SECURE = SECUREUPPER + SECURELOWER + SECUREDIGITS

def SECURE_Password(password):
    for a,b in SECURE:
        password = password.replace(a,b)
    return password

# Driver code
if __name__ == "__main__":

    password = input("Enter Your Password:\n")

    secure_pass = SECURE_Password(password)
    print(f"SECURED PASSWORD:\n{secure_pass}")
    with open("Password.txt","a") as f:
        f.write(f'''Original_password:{password},SECURED_VERSION:{secure_pass}\n''')