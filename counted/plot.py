f=open("3_2_Minimax.txt", "r")
# f.count("Draw!")

# file  = open("3_2_Minimax.txt", "r").read()
# team  = input("Draw!")
# count = file.count(team)
#print(open("3_2_Minimax.txt", "r").read().count("Draw!"))
#f = open("3_2_Minimax.txt", "r")
total = 0
for line in f:
    if "Draw!" in line:
        total += 1
f.close()
print(total)