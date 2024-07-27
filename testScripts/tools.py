import math

def split(arr, numPerSplit):
    """Input: arr: array to split into parts
            numperSplut: number of elements per split wanted
        Output: array with split arrays"""
    i=0
    returnArr=[]
    while(i<len(arr)):
        temp=[]
        for j in range(0, numPerSplit):
            try:
                temp.append(arr[i])
                i+=1
            except IndexError:
                break
        returnArr.append(temp)
    return returnArr
