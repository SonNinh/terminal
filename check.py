f = open('text', 'r')
text = f.read()
f.close()

while True:
    args = input("input: ")
    ls = args.split()

    print(text[-int(ls[0])-3:-int(ls[0])+1] + ':' + text[-int(ls[1])-3:-int(ls[1])+1])