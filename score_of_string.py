s='hello'
length=len(s)
caps = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
small = 'abcdefghijklmnopqrstuvwxyz'
caps_ASCII_value ={'A': 65, 'B': 66, 'C': 67, 'D': 68, 'E': 69, 'F': 70,
            'G': 71, 'H': 72, 'I': 73, 'J': 74, 'K': 75, 'L': 76, 
            'M': 77, 'N': 78, 'O': 79, 'P': 80, 'Q': 81, 'R': 82, 
            'S': 83, 'T': 84, 'U': 85, 'V': 86, 'W': 87, 'X': 88,
            'Y': 89, 'Z': 90}
small_ASCII_value ={'a': 97, 'b': 98, 'c': 99, 'd': 100, 'e': 101, 'f': 102,
                    'g': 103, 'h': 104, 'i': 105, 'j': 106, 'k': 107, 'l': 108, 'm': 109, 
                    'n': 110, 'o': 111, 'p': 112, 'q': 113, 'r': 114, 's': 115, 't': 116,
                    'u': 117, 'v': 118, 'w': 119, 'x': 120, 'y': 121, 'z': 122}
score=0
if (s[0] in caps):
    for i in range(length-1):
        finding1=s[i]
        finding2=s[i+1]
        score= score+abs(small_ASCII_value[finding1]-small_ASCII_value[finding2])
        string_score=(score)
    print(string_score)
elif (s[0] in small):
    for i in range(length-1):
        finding1=s[i]
        finding2=s[i+1]
        score= score+abs(small_ASCII_value[finding1]-small_ASCII_value[finding2])
        string_score=(score)
    print(string_score)


    