def getIndex(l: list, x: int):
    """
    """
    low = 0
    high = len(l)
    while low < high:
        mid = (low+high)//2
        if x < l[mid]:
            high = mid
        else:
            low = mid+1
    return low
