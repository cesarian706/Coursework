import cs50
# get valid height from user
print("Height: ", end= "")
while True:
    h = cs50.get_int()
    if h > 0 or h < 23:
        break
# print pattern for height
for i in range(h):
    for s in range((h-1) - i):
        print(" ", end= "")
    for p in range(i + 2):
        print("#", end="")
    print()
