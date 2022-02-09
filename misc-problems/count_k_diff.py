"""
Given an array of integers nums and an integer k, return the number of unique k-diff pairs in the array.

A k-diff pair is an integer pair (nums[i], nums[j]), where the following are true:

0 <= i < j < nums.length
|nums[i] - nums[j]| == k
Notice that |val| denotes the absolute value of val.

 

Example 1:

Input: nums = [3,1,4,1,5], k = 2
Output: 2
Explanation: There are two 2-diff pairs in the array, (1, 3) and (3, 5).
Although we have two 1s in the input, we should only return the number of unique pairs.
Example 2:

Input: nums = [1,2,3,4,5], k = 1
Output: 4
Explanation: There are four 1-diff pairs in the array, (1, 2), (2, 3), (3, 4) and (4, 5).
Example 3:

Input: nums = [1,3,1,5,4], k = 0
Output: 1
Explanation: There is one 0-diff pair in the array, (1, 1).

"""

class Solution:
    def findPairs(self, nums: List[int], k: int) -> int:
        nums.sort()
        a_ptr = 0
        b_ptr = 1
        k_diff_pairs = set()
        while (a_ptr < len(nums)) and (b_ptr <len(nums)):        
            if (nums[b_ptr] - nums[a_ptr]) < k:
                b_ptr += 1
            elif (nums[b_ptr] - nums[a_ptr]) == k:
                #num_pairs += 1
                k_diff_pairs.add((nums[a_ptr],nums[b_ptr]))
                a_ptr += 1
            else:
                a_ptr += 1
            if a_ptr == b_ptr:
                b_ptr += 1
                continue 
            
        #
        #return num_pairs
        return len(k_diff_pairs)
        
