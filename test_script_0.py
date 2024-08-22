from time import sleep
from random import randint, shuffle

mylist = ["apple", "banana", "cherry"]

sleep(randint(1, 3))
shuffle(mylist)
print(mylist)
sleep(randint(1, 3))
shuffle(mylist)
print(mylist)
sleep(randint(1, 3))
shuffle(mylist)
print(mylist)