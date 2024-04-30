ml = "sAo4.%Rm0HxSXcga"
mi = "1<;96538?:04=2740>"
o = ""

for j in range(len(mi)):
    o += chr(ml.index(mi[j]) + 48)

result = decodeURIComponent(o)
print(result)
