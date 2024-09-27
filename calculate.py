pre = 40 

save = 0
y = 0
while save < 6000:
    save = (save + pre * 12) * 1.07
    y += 1

print(f'save:{save}, year:{y}')
