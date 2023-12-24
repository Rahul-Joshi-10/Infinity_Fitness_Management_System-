
def funn():
    bday = input("Enter the date [dd/mm/yyyy] :")
    
    for i in bday:
        if i.isdigit():
            birthday = i

    return newfun(birthday)


def newfun(result):
        if len(result) == 1:
            return int(result)

        else:
            for i in finalresult:
                var = int(i)
                var12 += var
            var2 = newfun(str(var12))

        return str(var2)



        
if __name__ == "__main__":
    var3 = funn()
    print(var3)
    
    




    




