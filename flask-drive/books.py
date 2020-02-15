def solve (nArr, N, I, Q):
	# write your code here, which processes the passed variables, accepts queries and produces result.
        #print(nArr, N, I, Q)
        case = nArr[I-1:]
        print(case)
        while Q:
            temp = 0
            idx = 0
            val = int(input())
            if sum(case) <= val:
                print(max(case))
            elif val in case:
                print(val)
            elif val < min(case):
                print(-1)
            else:
                for i in case:
                    if temp < val:
                        temp += i
                        idx  += 1
                print(max(case[: idx - 1]))
            Q -= 1

T = int(input()) #Total Testcases
while(T > 0):
	temp = [int(x) for x in input().split()]
	N, I, Q = temp[0], temp[1], temp[2]
	nArr = [int(x) for x in input().split()]
	solve(nArr, N, I, Q)
	T = T - 1
