#returns the scout scale (20-80, 50 is average +- 10 for each standard deviation) rating for a player's ability 
def main(inp, name, index=1, useMean=False, reverseDev=False):
    arr = inp[0]
    units = inp[1]
    x = len(arr)
    stddev=__import__('stddev')
    for i in range(len(arr)):
        if arr[i][0] == name:
            s = stddev.main(inp, name, index, useMean, True).split(' ')
            #d is the number of std deviations from the mean, times 10 for baseball's 20-80 scale
            d = (float(arr[i][index]) - float(s[1][0:-1]))/float(s[4]) * 10
            d = int(d)
            if reverseDev:#for numbers where smaller is better
                d *= -1
            r = d % 5
            d += 50
            if r == 0:
                return(name + ": " + str(d) + ' (' + str(arr[i][index]) + units[index] + ')')
            if r < 3:
                d -= r
                return(name + ": " + str(d) + ' (' + str(arr[i][index]) + units[index] + ')')
            
            d += 5 - r
            return(name + ": " + str(d) + ' (' + str(arr[i][index]) + units[index] + ')')
    return name + ": none (no data)"
