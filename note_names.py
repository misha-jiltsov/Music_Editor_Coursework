note_dict = {0:"C",1:"D",2:"E",3:"F",4:"G",5:"A",6:"B"}
for i in range(40, 70): print(i, "-", str(note_dict[(i+3)%7]) + str((i-4)//7-4))