#outputs a new tuple (arr, units), where arr only has the players from one position
def main(inp, name, index = 3, unused = 0):
    arr = inp[0]
    position = ''
    for i in range(len(arr)):
        if arr[i][0] == name:
            position = arr[i][index]
            break
    
    arr2 = []
    for i in range(len(arr)):
        if arr[i][index] == position:
            arr2.append(arr[i])

    return (arr2, inp[1])
