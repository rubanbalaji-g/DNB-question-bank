import glob
import re

for file_path in glob.glob('*.html'):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # We want to replace patterns like "<td>a) " or " a) " with "<td>" or " "
    # Regex: Lookbehind for <td> or space, match a-d or i-iii, match ") ", replace with nothing (just keep the space/<td>)
    
    # Actually, we can just replace "a) ", "b) ", "c) ", "d) ", "i) ", "ii) ", "iii) ", "iv) "
    # It's safest to just do a simple string replace for <td>a) -> <td>, etc.
    # And " a) " -> " ", etc.
    
    # Let's use regex for a clean replace
    # (?<=<td>)\s*([a-h]|i{1,3}|iv|v)\)\s*
    content = re.sub(r'(?<=<td>)\s*([a-h]|i{1,3}|iv|v)\)\s*', '', content)
    
    # Also inside the text: " a) " -> " "
    content = re.sub(r'\s+([a-h]|i{1,3}|iv|v)\)\s*', ' ', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
