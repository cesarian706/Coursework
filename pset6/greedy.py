import cs50
#prompt user input
print("O hai! How much change is owed?")
while True:
    m = cs50.get_float()
    if m > 0:
        break
#
c = round(m * 100)
#divide by quarter value
q = c // 25
#get remainder
r = c % 25
#divide by dime value
d = r // 10
#get remainder
r = r % 10
#divide by nickel value
n = r //5
#get remainder
r = r % 5
#divide by penny value
p = r // 1
#add coins count for each value
o = q + d + n + p
#print result
print(o)