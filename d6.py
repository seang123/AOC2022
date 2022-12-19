import time

ss = time.perf_counter()
with open('d6_data.txt', 'r') as f:
    content = f.read()
    for i in range(14, len(content)-1):
        if len(set(content[i-14:i])) == 14:
            print(i)
            break
print(f'{(time.perf_counter() - ss):.3f}')