#outputs a new tuple (arr, units), where arr only has the players from one position
def main(inp, name, index = 3, unused = 0):
    validPositions = ["C", "1B", "2B", "3B", "SS", "LF", "CF", "RF", "OF"]
    arr = inp[0]
    if len(name) < 3:
        if not name in validPositions:
            raise ValueError()
        position = name
    else: 
        for i in range(len(arr)):
            if arr[i][0] == name:
                position = arr[i][index]
                break
    arr2 = []
    if not position == "OF":
        for i in range(len(arr)):
            if arr[i][index] == position:
                arr2.append(arr[i])
    else:
        for i in range(len(arr)):
            if arr[i][index] in ["LF", "CF", "RF"]:
                arr2.append(arr[i])
    if len(arr2) == 0:
        raise ValueError()
    return (arr2, inp[1])
