"""
functions to read and write step count
"""
STEP_FILE = "steps.txt"


def readfile():
    """reads step file"""
    try:
        with open(STEP_FILE, "r", encoding="utf8") as f:
            for line in f:
                steps = int(line)
                return steps
    except:
        pass
    return 0


def writefile(num):
    """writes step file"""
    with open(STEP_FILE, "w", encoding="utf8") as f:
        f.write(str(num) + "\n")
