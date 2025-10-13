swapped_values=[]
def swap_case(s):
    for j in s:
        if (j.islower()):
            swapped_values.append(j.upper())
        elif(j.isupper()):
            swapped_values.append(j.lower())
        else:
            swapped_values.append(j)

if __name__ == '__main__':
    s ="hello"
    swap_case(s)
    join=''.join(swapped_values)
    print(join)

