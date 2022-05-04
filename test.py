class Terrain:
    pass

def list_filter(arr, condition):
    return list(filter(condition, arr))

arr = [1,2,3,4]
cond = lambda x: x<3

print(list_filter(arr, cond))

print(str(type(Terrain())))

n = int(input())
posters = 0
corners = []
for _ in range(n):
    _, height = list(map(int, input().split()))
    corners = list(filter(lambda x: x<=height, corners))
    if height not in corners:
        posters += 1
        corners.append(height)
print(posters)