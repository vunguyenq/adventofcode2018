input =  [(122, 79 , 57), (217, 196, 39), (101, 153, 71)]

for (x,y,S) in input:
    res = ((((x+10) * y + S) * (x+10)) % 1000) // 100 - 5
    print(res)