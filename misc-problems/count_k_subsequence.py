# Enter your code here. Read input from STDIN. Print output to STDOUT
"""
#Question from hacker rank 
Jigar got a sequence of n positive integers as his birthday present! He likes consecutive subsequences whose sum is divisible by k. He asks you to write a program to count them for him.

Input Format
The first line contains T, the number of testcases.
T testcases follow. Each testcase consists of 2 lines.
The first line contains n and k separated by a single space.
And the second line contains n space separated integers.

Output Format
For each test case, output the number of consecutive subsequenences whose sum is divisible by k in a newline. 
"""

import sys

def count_k_subseq(k,nums):
    cumsum = [0]*len(nums)
    cumsum[0] = nums[0]
    for i in range(1,len(nums)):
        cumsum[i] = cumsum[i-1] + nums[i]
    #
    remainder_count = [0]*k
    for i in cumsum:
        remainder_count[i%k] += 1
    #
    count = remainder_count[0]
    for i in remainder_count:
        count += i*(i-1)//2
    return count


T = int(sys.stdin.readline().strip())
for _ in range(T):
    n,k = sys.stdin.readline().strip().split()
    n = int(n)
    k = int(k)
    nums = sys.stdin.readline().strip().split()
    nums = [int(x) for x in nums]
    #print(len(nums), n)
    #assert len(nums) == n
    print(count_k_subseq(k,nums))



