import json
import os
import re

with open('classified_questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

# Group by target HTML file
files_to_update = {}
for q in questions:
    target = q['target_html']
    if target not in files_to_update:
        files_to_update[target] = []
    files_to_update[target].append(q)

for target_file, qs in files_to_update.items():
    if not os.path.exists(target_file):
        print(f"File {target_file} does not exist, skipping.")
        continue
        
    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # We want to insert the rows at the end of the <tbody>
    rows_to_insert = []
    for q in qs:
        # Check if the row already exists to avoid duplicates if run multiple times
        # But we format it nicely
        row = f"                    <tr><td>{q['formatted_text']}</td><td>{q['chapter']}</td><td>{q['year']}</td></tr>"
        if row not in content:
            rows_to_insert.append(row)
            
    if rows_to_insert:
        insertion = "\n" + "\n".join(rows_to_insert) + "\n</tbody>"
        content = content.replace("</tbody>", insertion)
        
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Inserted {len(rows_to_insert)} rows into {target_file}.")

print("Injection complete.")
