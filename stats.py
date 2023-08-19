def readfile():
    try:
        with open("steps.txt", "r") as f:
            for line in f:
                steps = int(line)
                return steps
    except:
        pass
    return 0


def writefile(num):
    with open("steps.txt", "w") as f:
        f.write(str(num) + "\n")
