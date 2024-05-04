import random

def computer_guess(x):
  low = 1
  high = x
  feedback = ''
  while feedback != "c":
    if low != high:
      guess = random.randint(low, high)
    else:
      guess =  low #could be high. low = high
    feedback = input(f"Is {guess} too high(H), too low(L), or correctly (c).lower()")

    if feedback == 'h':
      high = guess -1
    elif feedback== 'l':
      low = guess + 1

  print(f"Yes, Congrats. the computer have guessed the number {guess} corectlty")


computer_guess(19)