with open("words.txt",'w') as w:
    w.write('this is a test\n')

with open("words.txt") as r:
    print(r.read())
