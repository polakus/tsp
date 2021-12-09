count = 0
for m in range(500):
    for n in range(500):
        for i in range(500):
            for j in range(500):
                if n!=j and m!=i and i!=j and m!=n and ((i+j)*(i+j+1)*(i+j+3))/7 == ((m+n)*(m+n+1)*(m+n+3))/7:
                    print(str(count))
                    count += 1
        
