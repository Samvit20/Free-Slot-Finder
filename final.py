from PIL import Image
import json
import numpy as np
import lib
import os
slot_type = np.zeros((14, 13))
final_list = []
coords = [0, 0]
tt = Image.open("newtimetable.png")
dim = tt.size

def updateCoordinates():
    global coords
    if coords[1] < 12:
        coords = [coords[0], coords[1]+1]
    else:
        coords = [coords[0]+1, 0]

cols = [(0, 255, 0), (255, 255, 0)]
start = []
i = 0
while i < dim[0]:
    j = 0
    while j < dim[1]:
        rgb = tt.getpixel((i, j))
        if rgb == (255, 255, 0) or rgb == (0, 255, 0):
            start = [i, j]
            i = dim[0]
            break
        j = j + 1
    i = i + 1
j = start[1]
i = start[0]

try:
    for m in range(14):
        for a in range(13):
            if tt.getpixel((i, j)) == (0, 255, 0):
                slot_type[coords[0], coords[1]] = 1
            updateCoordinates()
            if a == 12:
                break
            i = i + 1
            while tt.getpixel((i, j)) != (0, 0, 0):
                i = i + 1
            while tt.getpixel((i, j)) not in cols:
                i = i + 1
        if m == 13:
            break
        i = start[0]
        j = j + 1
        while tt.getpixel((i, j)) != (0, 0, 0):
            j = j + 1
        while tt.getpixel((i, j)) not in cols:
            j = j + 1

except IndexError:
    if coords[0] < 10 or coords[1] != 0:
        print("NOT ABLE TO READ FILE: Please upload proper image of time table.")
        exit()

for x in range(14 - coords[0]):
    tr = np.zeros(13)
    i = 13
    while i >= 1:
        slot_type[i] = slot_type[i-1]
        i = i - 1
    slot_type[0] = tr
slot_type = np.rot90(slot_type, 2, (0, 1))

a = 0
while a < 13:
    m = 0
    while m < 13:
        final_list.append(int(slot_type[a, m] + slot_type[a+1, m]))
        m = m + 1
    final_list.append('\n')
    a = a + 2

os.remove("newtimetable.png")

print("Schedule is: \n")
c = 0
for i in final_list:
    if i == 0:
        # print(c+1)
        print("Free")
    elif(i == 1):
        print("Busy")
    else:
        print("\n")
x = input("\nGive any input to continue: ")
exit()
