import random

x = int(input("Enter a number for the last range: "))

def guess(x):
  random_number = random.randint(1,x)
  guess = 0
  while guess != random_number:
    guess = int(input(f"Guess a Number between 1 to {x} "))

    if guess < random_number:
      print("Sorry, Guess again. Too Low")

    elif guess > random_number:
      print("Sorry, Guess again. Too High")

  print(f"Yes, Congrats. You Have guessed the number {random_number} corectlty")

guess(x)
