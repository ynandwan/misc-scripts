"""
Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

 

Example 1:

Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
Example 2:

Input: nums = [3,2,4], target = 6
Output: [1,2]
Example 3:

Input: nums = [3,3], target = 6
Output: [0,1]
 

Constraints:

2 <= nums.length <= 104
-109 <= nums[i] <= 109
-109 <= target <= 109
Only one valid answer exists.
"""

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        num2ind = {}
        for i,num in enumerate(nums):
            if num not in num2ind:
                num2ind[num] = []
            #
            num2ind[num].append(i)
        #
        for i, num in enumerate(nums):
            if (target - num) in num2ind:
                if (target - num) == num:
                    if len(num2ind[num]) >= 2:
                        return (num2ind[num][0], num2ind[num][1])
                else:    
                    return([i,num2ind[target-num][0]])
        """
        for i in range(len(nums)):
            for j in range(i+1, len(nums)):
                if nums[i] + nums[j] == target:
                    return [i,j]
        """
        
        
