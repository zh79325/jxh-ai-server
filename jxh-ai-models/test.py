

def formatN(n):
    if n < 0:
        return 0
    elif n > 1:
        return 1
    else:
        return n
if __name__ == '__main__':
    n=1.0001111
    print(f"{formatN(n):.5f}")
