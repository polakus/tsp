try:
    # 1/0
    a = [1]
    print(a[1])
except ZeroDivisionError:
    print("error")