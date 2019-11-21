import sys

def is_palindrome(s):
    if len(s) == 1:
        return True
    #   
    reverse_s = s[::-1]
    return s == reverse_s


def count_palindrom_recursive(s, start=0, end=None):
    if end is None:
        end = len(s) - 1
    #
    len_substr = end - start + 1
    assert len(s) >= len_substr
    if len_substr == 0:
        return 0
    elif len_substr == 1:
        return 1
    elif len_substr == 2:
        return (2 + int(s[start] == s[end]))
    else:
        return (int(is_palindrome(s[start:(end+1)])) + count_palindrom_recursive(s, start, end-1) + count_palindrom_recursive(s, start+1, end) - count_palindrom_recursive(s, start+1, end-1))

def count_palindrom_dp(s,start=0,end=None):
    if end is None:
        end = len(s) - 1
    #
    len_substr = end - start + 1
    assert len(s) >= len_substr
    if len_substr == 0:
        return 0
    elif len_substr == 1:
        return 1
    elif len_substr == 2:
        return (2 + int(s[start] == s[end]))
    else: 
        #
        #dp_table[i][j]: contains palindrome count for s[i:j]
        #answer in dp_table[0][len_substr]
        dp_table = [[0 for _ in range(len_substr)] for _ in range(len_substr)]
        #initialize diagonal and upper off diagonal
        for i in range(len_substr):
            dp_table[i][i] = 1
            if i != len_substr-1:
                dp_table[i][i+1] = 2 + int(s[i] == s[i+1])
        #loop on len of substr
        #len  = 3 to len_substr
        for this_len in range(3,len_substr+1):
            #i: substring starting at i
            for i in range(len_substr - this_len+1):
                j = i + this_len - 1
                dp_table[i][j] = dp_table[i][j-1] + dp_table[i+1][j] - dp_table[i+1][j-1] + int(is_palindrome(s[i:(j+1)]))
        #
        return dp_table[0][-1]

if __name__ == '__main__':
    print(count_palindrom_dp(sys.argv[1]))

    
