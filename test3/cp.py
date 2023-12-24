def calculate(date_str):
    if len(date_str) == 1:
        return int(date_str)
    else:
        newsum = 0
        for i in date_str:
            digit_sum = int(i)
            newsum = newsum + digit_sum
        return calculate(str(newsum))

def funn():
    bday = input("Enter the date [dd/mm/yyyy] :")
    bdigit =''
    for i in bday:
        if i.isdigit():
            bdigit += i 
    result = calculate(bdigit)
    
    return str(result)

if __name__ == "__main__":
    final= funn()
    print(final)
 