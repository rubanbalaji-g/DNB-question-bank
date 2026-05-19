import os
import glob
import subprocess
import json
import re

pdf_dir = "/home/ruban/Documents/DNB question paper"
pdf_files = glob.glob(os.path.join(pdf_dir, "*.pdf"))

questions = []

unwanted_phrases = [
    r'Subjective : Yes',
    r'Calculator : None',
    r'Response Time : N.A',
    r'Think Time : N.A',
    r'Minimum Instruction Time : [0-9]*',
    r'Correct Marks : [0-9]*'
]

def split_question(q_text, exam_tag):
    # Split questions that have a), b), c) or i), ii) 
    # Usually it's "a) text b) text". Sometimes there's a prefix sentence before a).
    # e.g. "Discuss X: a) Y [5] b) Z [5]" -> "Discuss X: a) Y [5]" and "Discuss X: b) Z [5]"
    
    # Check if there are a) and b)
    if 'a)' in q_text and 'b)' in q_text:
        # Split using regex to catch "a)", "b)", "c)", "d)"
        parts = re.split(r'([a-d]\))', q_text)
        
        prefix = parts[0].strip()
        
        split_qs = []
        for i in range(1, len(parts), 2):
            part_letter = parts[i]
            part_text = parts[i+1].strip() if i+1 < len(parts) else ""
            
            # Extract marks from this part if present
            marks_match = re.search(r'\[([^\]]+)\]$', part_text)
            marks_str = ""
            if marks_match:
                marks_str = marks_match.group(1)
                part_text = part_text[:marks_match.start()].strip()
            
            # Combine prefix and part
            combined_text = part_text
            if prefix:
                combined_text = f"{prefix} {part_letter} {part_text}"
            else:
                combined_text = f"{part_letter} {part_text}"
                
            formatted = f"{combined_text} ({exam_tag})"
            if marks_str:
                formatted += f" {marks_str}"
                
            split_qs.append({
                "raw_text": combined_text,
                "formatted_text": formatted
            })
        return split_qs
    else:
        # No subparts
        marks_match = re.search(r'\[([^\]]+)\]$', q_text)
        marks_str = ""
        if marks_match:
            marks_str = marks_match.group(1)
            q_text = q_text[:marks_match.start()].strip()
        
        formatted = f"{q_text} ({exam_tag})"
        if marks_str:
            formatted += f" {marks_str}"
        return [{
            "raw_text": q_text,
            "formatted_text": formatted
        }]


for pdf in pdf_files:
    filename = os.path.basename(pdf)
    
    parts = filename.replace('.pdf', '').split()
    exam = parts[0].upper()
    session_month = parts[1].upper()
    year_short = parts[2]
    paper = parts[3].upper()
    
    year_full = "20" + year_short
    exam_tag = f"{exam} {year_full}/{paper[1]}"
    
    try:
        result = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True)
        text = result.stdout
        
        text = text.replace('\x0c', '')
        
        q_blocks = text.split('Question Number :')
        
        for block in q_blocks[1:]:
            lines = block.strip().split('\n')
            
            q_lines = []
            for line in lines[1:]:
                line = line.strip()
                if not line: continue
                if line.startswith('Question Id :') or line.startswith('Display Marks:'): continue
                
                # Remove unwanted phrases
                for phrase in unwanted_phrases:
                    line = re.sub(phrase, '', line)
                
                line = line.strip()
                if line:
                    q_lines.append(line)
            
            q_text = " ".join(q_lines)
            
            # Remove leading "1. "
            q_text = re.sub(r'^\d+\.\s*', '', q_text).strip()
            
            if not q_text:
                continue
                
            sub_questions = split_question(q_text, exam_tag)
            
            for sq in sub_questions:
                questions.append({
                    "filename": filename,
                    "exam": exam,
                    "year": year_full,
                    "paper": paper,
                    "raw_text": sq['raw_text'],
                    "formatted_text": sq['formatted_text']
                })
            
    except Exception as e:
        print(f"Error parsing {filename}: {e}")

with open('raw_questions.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, indent=4, ensure_ascii=False)

print(f"Extracted {len(questions)} questions.")
