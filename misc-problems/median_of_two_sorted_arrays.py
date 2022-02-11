
"""
Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.

The overall run time complexity should be O(log (m+n)).

 

Example 1:

Input: nums1 = [1,3], nums2 = [2]
Output: 2.00000
Explanation: merged array = [1,2,3] and median is 2.
Example 2:

Input: nums1 = [1,2], nums2 = [3,4]
Output: 2.50000
Explanation: merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5.
 

Constraints:

nums1.length == m
nums2.length == n
0 <= m <= 1000
0 <= n <= 1000
1 <= m + n <= 2000
-106 <= nums1[i], nums2[i] <= 106
"""

import math
class Solution:
    
    
    def binary_search(self, num, A, i = 0, j = -1):
        #return the first index where 
        #num should be inserted in the sorted array A[i:j] 
        
        if j == -1:
            j = len(A)
        #
        if j<= i:
            print('assert fail:',num,A,i,j)
            assert j > i
            
        #print(num,A,i,j)
        if num <= A[i]:
            return i
        elif num > A[j-1]:
            return j
        else:
            n = j - i
            mid_ind = i + int(n/2)
            mid = A[mid_ind]
            if num <= mid:
                return self.binary_search(num, A, i, mid_ind)
            else:
                return self.binary_search(num, A, mid_ind+1, j)
            
        
    #k numbers are smaller than the returned number. 
    #i.e. returned number is (k+1)^th element
    def k_small(self, k:int, A: List[int],i: int=0, j: int=-1):
        if j == -1:
            j = len(A)
        #print ('k_small',k,A,i,j)
        #assert i + k < j
        return A[i+k]
     
    def find(self, k: int, A1: List[int], A2: List[int], i1 = 0, j1 = -1, i2 = 0, j2 = -1):
        #exactly k numbers are smaller than the returned number in 
        #the merged list A1[i1:j1]; A2[i2:j2]
        #i.e. it is (k+1)^th element in the merged list
        #print('find',k, A1, A2, i1,j1,i2,j2)
        if j1 == -1:
            j1 = len(A1)
        if j2 == -1:
            j2 = len(A2)
        #
        #
        l1 = j1 - i1
        l2 = j2 - i2
        #print('find l1, l2', l1, l2)
        if l2 > l1:
            return self.find(k,A2, A1, i2, j2, i1, j1)
        #
        if l2 == 0:
            return self.k_small(k,A1,i1, j1)
        
        if k == 0:
            #return the smallest number
            return min(A1[i1], A2[i2])
            
        
        if k == 1:
            if l1 == 1:
                return max(A1[i1],A2[i2])
            else:
                if A2[i2] <= A1[i1]:
                    if l2 >= 2:
                        return min(A1[i1],A2[i2+1])
                    else:
                        return A1[i1]
                else:
                    return min(A1[i1+1], A2[i2])
        
        k1 = min(l1-1,round(k/2))
        #k2 = min(l2-1,k - k1)
        
        #exactly k1 numbers are smaller than k1small in A1
        k1small = self.k_small(k1, A1, i1, j1)
        
        #
        k12 = self.binary_search(k1small, A2, i2, j2) - i2
        if k12+i2 == j2:
            y = k1small
        else:
            y = A2[i2+k12]
        
        if k1+k12 == k:
            return min(k1small, y)
        elif k1 + k12 <= k:
            #k^th smallest number lies in A1[k1:j1] and A2[k12:j2]
            return self.find(k-k1-k12,A1,A2,i1+k1,j1, i2+k12, j2)
        elif k1 + k12 > k:
            return self.find(k,A1,A2,i1, i1+k1, i2, i2+k12)
            
            
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        n1 = len(nums1)
        n2 = len(nums2)
        floor_k = math.floor((n1 + n2-1)/2)
        ceil_k = math.ceil((n1+n2-1)/2)
        
        if floor_k == ceil_k:
            return self.find(floor_k, nums1,nums2)
        else:
            return (self.find(floor_k, nums1,nums2) + self.find( ceil_k, nums1, nums2))/2.0
        
