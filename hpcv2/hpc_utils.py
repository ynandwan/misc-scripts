
import os

def replace_spl(s):
    replace_chars = [' ', '/', '_','-']
    for this_char in replace_chars:
        s = s.replace(this_char,'.')
    return s

def parse_filename(s):
    bname = os.path.basename(s)   
    bname = '.'.join(bname.split('.')[:-1])
    return replace_spl(bname)


