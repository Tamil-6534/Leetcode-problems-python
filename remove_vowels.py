s="GeeksforGeeks - A Computer Science Portal for Geeks"
length=len(s)
s_list=list(s)
for i in s_list[0:]:
    if (i=='a') or (i=='A'):
        s_list.remove(i)
for i in s_list[0:]:
    if (i=='e') or (i=="E"):
        s_list.remove(i)
for i in s_list[0:]:
    if (i=='i') or (i=='I'):
        s_list.remove(i)
for i in s_list[0:]:
    if (i=='o') or (i=='O'):
        s_list.remove(i)
for i in s_list[0:]:
    if (i=='u') or (i=="U"):
        s_list.remove(i)
joined="".join(s_list)
print(joined)
