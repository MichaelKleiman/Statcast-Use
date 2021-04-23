#from an array of tuples to an array of 2 item arrays

#the relevant stat must always be in index 1. 
def deTuple(arr, index):
    for i in range(len(arr)):
        arr[i]=[arr[i][0], arr[i][index]]

#quicksorts in place the array by the stat. Probably makes a negligable runtime difference compared to other sorts, but it seemed appropriate. I kind of just wanted to do it this way.
def quicksort(arr, startIndex, endIndex):
    #not the most efficient base case, but it works
    if endIndex - startIndex < 1:
        return
    
    #the middle element should work well for every stat
    pI = int((endIndex - startIndex) / 2) + startIndex
    p = arr[pI]
    arr[pI] = arr[startIndex]
    pI = startIndex

    for i in range(startIndex + 1, endIndex + 1):
        if arr[i][1] > p[1]:
            arr[pI] = arr[i]
            arr[i] = arr[pI + 1]
            pI += 1

    arr[pI] = p
    quicksort(arr, startIndex, pI - 1)
    quicksort(arr, pI + 1, endIndex)

def cleanName(n):
    cn = n.upper()
    cns = cn.split('.')
    cn = ''
    for i in range(len(cns)):
       cn += cns[i] 
    return cn
#returns the percentile of the player regarding this stat
def main(inp, name, index = 1, reverse = False):
    arr = inp[0]
    units = inp[1]
    x = len(arr)
    if units[1] != 'ft/s':
        deTuple(arr, index)
        quicksort(arr, 0, x - 1)
    #if some players are missing data for this stat, they are removed from the percentile calculation 
    for i in range(x):
        if arr[i][1] < 0:
            x = i
            break
    cn = cleanName(name)
    for i in range(x):
        if cleanName(arr[i][0]) == cn:
            p = 100 - (100 * i / x)
            p = round(p, 1)
            if reverse:
                p = 100.0 - p
                return(arr[i][0] + ': ' + str(p) + '%'+ ' (' + str(arr[i][1])+ units[index] +', #' + str(len(arr)) +' of ' + str(i)+')')
            return(arr[i][0] + ': ' + str(p) + '%'+ ' (' + str(arr[i][1])+ units[index] +', #' + str(i) +' of ' + str(len(arr))+')')
    return name + ", none (no data)"
