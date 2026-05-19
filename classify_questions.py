import json
import re

with open('raw_questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

# Rules mapping keywords to (Part HTML filename, Chapter Number)
rules = [
    # Statistics
    (r'(meta-analysis|study design|bias|randomization|odds ratio|relative risk|smr|correlation|student t test|alpha error|cluster randomized)', 'stat.html', 'Stat'),
    # Vaccinology
    (r'(vaccine|immunization|aefi|polio|pneumococcal|ipv|vzig)', 'vac.html', 'Vac'),
    # Social Pediatrics
    (r'(asha|hbyc|hbnc|poshan abhiyan|swastha nari|rksk|rashtriya kishore)', 'sp.html', 'SP'),
    
    # Part 10: Neonatal (Do this early as it's very specific)
    (r'(neonate|neonatal|newborn|premature|preterm|rop|kmc|kangaroo mother|apnea of prematurity|fetal|intrauterine)', 'part10.html', '118'),
    
    # Part 6: Fluid/Electrolytes
    (r'(fluid|sodium|hypernatremia|hyponatremia|potassium|acidosis|alkalosis|dehydration)', 'part6.html', '63'),
    
    # Part 7: Emergency
    (r'(shock|septic shock|ards|burn|cpr|bls|pals|organophosphate|poisoning)', 'part7.html', '73'),
    
    # Part 8: Genetics
    (r'(genetics|down\'s syndrome|down syndrome|turner|gene|chromosome|phenotype)', 'part8.html', '82'),
    
    # Part 5: Nutrition
    (r'(nutrition|feeding|breast milk|vitamin|malnutrition|undernutrition|complementary feeding)', 'part5.html', '49'),
    
    # Part 24: Endocrine
    (r'(thyroid|diabetes|dka|pituitary|adrenal|pheochromocytoma)', 'part24.html', '581'),
    
    # Part 15: Infectious
    (r'(infection|sepsis|meningitis|rabies|dengue|malaria|fever|tuberculosis|typhoid|fungal infection)', 'part15.html', '196'),
    
    # Part 19: Blood
    (r'(anemia|thalassemia|bleeding|coagulation|hemophilia|purpura|aiha|transfusion)', 'part19.html', '480'),
    
    # Part 18: Cardiovascular
    (r'(heart|chf|congestive|cyanotic spell|arrhythmia|cardiomyopathy|rheumatic fever)', 'part18.html', '446'),
    
    # Part 17: Respiratory
    (r'(respiratory|pneumonia|asthma|stridor|croup|pulmonary)', 'part17.html', '412'),
    
    # Part 21: Nephrology
    (r'(nephrotic|nephritic|glomerulonephritis|hus|kidney|renal|enuresis|tubular)', 'part21.html', '534'),
    
    # Part 25: Nervous
    (r'(seizure|epilepsy|brain|cerebral|encephalitis|coma|stroke|sspe|guillain|babinski)', 'part25.html', '605'),
    
    # Part 14: Rheumatic
    (r'(rheumatic|sle|kawasaki|lupus)', 'part14.html', '171'),
    
    # Part 20: Cancer
    (r'(cancer|tumor|leukemia|lymphoma|hodgkin)', 'part20.html', '512'),
    
    # Part 27: Eye
    (r'(eye|optic|retinopathy|cataract|vision)', 'part27.html', '643'),
    
    # Part 28: Ear
    (r'(ear|bera|hearing|deafness)', 'part28.html', '652'),
    
    # Part 29: Skin
    (r'(skin|scabies|dermatitis)', 'part29.html', '660'),
    
    # Part 3: Behavioral
    (r'(anorexia|bulimia|eating disorder|behavior|mood disorder)', 'part3.html', '26'),
    
    # Part 2: Growth & Dev
    (r'(growth|development|milestone)', 'part2.html', '15'),
    
    # Part 11: Adolescent
    (r'(adolescent|puberty|headsss)', 'part11.html', '140'),
    
    # Part 1: Field of Pediatrics
    (r'(ethics|palliative|adoption|abuse|injury|maltreatment|accident)', 'part1.html', '1'),
    
    # Part 16: Digestive
    (r'(diarrhea|liver|hepatic|hepatitis|wilson|celiac|crohn|gi|fecal|endoscopy)', 'part16.html', '360'),
    
    # Part 32: Environmental
    (r'(altitude|mountain sickness)', 'part32.html', '730'),
]

classified_questions = []

for q in questions:
    text = q['raw_text'].lower()
    
    assigned_part = 'misc.html'
    assigned_chap = 'Misc'
    
    for pattern, part, chap in rules:
        if re.search(pattern, text):
            assigned_part = part
            assigned_chap = chap
            break
            
    q['target_html'] = assigned_part
    q['chapter'] = assigned_chap
    classified_questions.append(q)

with open('classified_questions.json', 'w', encoding='utf-8') as f:
    json.dump(classified_questions, f, indent=4, ensure_ascii=False)

print(f"Classified {len(classified_questions)} questions.")
