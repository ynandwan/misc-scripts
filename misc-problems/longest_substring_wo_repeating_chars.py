"""
Given a string s, find the length of the longest substring without repeating characters.

 

Example 1:

Input: s = "abcabcbb"
Output: 3
Explanation: The answer is "abc", with the length of 3.
Example 2:

Input: s = "bbbbb"
Output: 1
Explanation: The answer is "b", with the length of 1.
Example 3:

Input: s = "pwwkew"
Output: 3
Explanation: The answer is "wke", with the length of 3.
Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.
 

Constraints:

0 <= s.length <= 5 * 104
s consists of English letters, digits, symbols and spaces.

"""

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        gstr = ''
        l = 0
        for i,char in enumerate(s):
            #print(i)
            if i == 0:
                l = 1
                g = set([char])
                gstr = char
                #print("first char:",l,gstr,g)
            else:
                if char not in g:
                    g.add(char)
                    gstr = '{}{}'.format(gstr,char)
                    l = max(l,len(gstr))
                    #print("char not in g:", l,gstr,g)
                else:
                    lg = len(gstr)
                    for j in range(lg):
                        if gstr[lg - j -1] == char:
                            gstr_new = '{}{}'.format(gstr[lg-j:],char)
                            break
                    #
                    #print("found char",l,gstr,gstr_new,g, j )
                    for k in range(j+1,lg):
                        g.remove(gstr[lg-k-1])
                    #
                    #print(l,gstr,g)
                    gstr = gstr_new
                    l = max(l, len(gstr))
        return l
