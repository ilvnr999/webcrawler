pre = 30 

save = 30
y = 0
while save < 3000:
    save = (save + pre * 12) * 1.07
    y += 1

print(f'save:{save}, year:{y}')
