import json
import os
import re

with open('raw_questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

# Group questions by Exam and Session/Year
# E.g., 'DCH DEC 2025'
grouped_sessions = {}
for q in questions:
    filename = q['filename']
    parts = filename.replace('.pdf', '').split()
    exam = parts[0].upper()
    session = parts[1].upper()
    year = q['year']
    
    key = f"{exam} {session} {year}"
    file_slug = f"{exam.lower()}_{session.lower()}_{year}.html"
    
    if key not in grouped_sessions:
        grouped_sessions[key] = {
            'title': key,
            'file': file_slug,
            'questions': []
        }
    grouped_sessions[key]['questions'].append(q)

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><link rel="icon" type="image/png" href="favicon.png"><link rel="icon" type="image/png" href="favicon.png">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | DNB Pediatrics Question Bank</title>
    
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="assets/css/style.css">
    <script src="assets/js/main.js" defer></script>
</head>
<body>

    <div class="container mx-auto px-4 py-8">
        <header class="text-center mb-10">
            <h1 class="title">{title}</h1>
            <p class="subtitle"><a href="index.html" class="back-link">&larr; Back to Main Index</a></p>
        </header>

        <main class="glass-panel">
            <div class="controls-bar">
                <button id="theme-toggle" class="theme-toggle">🌙 Dark Mode</button>
                <div class="search-container">
                    <input type="text" id="search-input" class="search-input" placeholder="Search questions...">
                </div>
            </div>
            <div class="table-container">
            <table id="questionsTable">
                <thead>
                    <tr>
                        <th class="w-9-12" onclick="sortTable(0)">
                            Question
                        </th>
                        <th class="w-2-12" onclick="sortTable(1)">
                            Paper
                        </th>
                        <th class="w-1-12" onclick="sortTable(2)">
                            Year
                        </th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
            </div>
        </main>
        
        <footer class="text-center mt-10 text-gray-500 text-sm">
            <p>YoRu | Updated till Jan 2025</p>
        </footer>
    </div>
    
    <button id="fab" class="fab" title="Back to top">↑</button>
</body>
</html>
"""

# Create the HTML files
index_links = []
for key, data in grouped_sessions.items():
    rows = []
    # Sort by paper inside the session
    data['questions'].sort(key=lambda x: x['paper'])
    for q in data['questions']:
        row = f"<tr><td>{q['formatted_text']}</td><td>{q['paper']}</td><td>{q['year']}</td></tr>"
        rows.append(row)
    
    html_content = html_template.format(title=data['title'], rows="\n                    ".join(rows))
    
    with open(data['file'], 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    index_links.append((data['title'], data['file']))

# Now update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

# We want to add a new section for Latest Question Papers just before the "Volume 1" section
# "Volume 1" starts with: <!-- Volume 1 -->

links_html = ""
for title, file in sorted(index_links, reverse=True):
    links_html += f'<a href="{file}" class="card-link">{title}</a>\n                    '

new_section = f"""<!-- Latest Papers -->
            <div>
                <div class="section-blue" style="border-color: #f59e0b; color: #f59e0b;"><h2 class="section-title" style="border-color: #f59e0b; color: #f59e0b;">Latest Question Papers (Yearwise)</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {links_html.strip()}
                </div></div>
            </div>
            
            <div class="mt-10"></div>
            """

if "<!-- Latest Papers -->" not in index_content:
    index_content = index_content.replace('<!-- Volume 1 -->', new_section + '\n            <!-- Volume 1 -->')
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(index_content)

print("Yearwise files created and index.html updated.")
