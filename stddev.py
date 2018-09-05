#returns the mean/median, and the standard deviation. forScout returns it without units
def main(inp, name, index=1, useMean=True, forScout=False):
    arr = inp[0]
    units = inp[1]
    x = 0.0
    c = len(arr)
    for i in arr:
        v = float(i[index])
        if v < 0:
            continue
        x += v 
    
    middle = int(c / 2)
    
    median = arr[middle][index] if x % 2 == 1 else (arr[middle][index] + arr[middle][index]) / 2
    #the mean, or the median
    m = x / c if useMean else median
    x = 0.0
    #now for the standard deviation
    for i in arr:
        v = float(i[index])
        if v < 0:
            continue
        v = v - m
        x += v*v
    
    import math
    dev = math.sqrt(x/c)
    m = round(m, 3)
    dev = round(dev, 4)
    name = "mean: " if useMean else "median: "
    if forScout:
        return name + str(m) + ", standard deviation: " + str(dev)
    #with units 
    return name + str(m) + units[index] + ", standard deviation: " + str(dev) + units[index]
    
