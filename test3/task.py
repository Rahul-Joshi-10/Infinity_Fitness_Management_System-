
def funn(birthday):
    if len(birthday) == 1:
            return int(birthday)
    else:
        var2 = 0
        for i in birthday:
            var = int(i)
            var2 += var
        var3 = funn(str(var2))
        return str(var3)

if __name__ == "__main__":
    
    birthday = ''
    bday = input("Enter the your birthday [dd/mm/yyyy] :")
    for i in bday:
        if i.isdigit():
            birthday += i

    finall = funn(birthday)
    print(finall)
    
    
    




    




