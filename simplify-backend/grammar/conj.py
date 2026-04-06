from .lexicons import (
    SUBORDINATING_CONJUNCTIONS, 
    COORDINATING_CONJUNCTIONS, 
    CORRELATIVE_PAIRS
)

def explain_conjunction(doc):
    results = []
    processed_indices = set()

    for token in doc:
        if token.i in processed_indices:
            continue

        # correlative
        if token.dep_ == "preconj" or token.text.lower() in CORRELATIVE_PAIRS:
           
            main_conj = next(
                (t for t in token.head.children 
                 if t.pos_ == "CCONJ" and t.i != token.i), 
                None
            )
            
            if main_conj:
                pair_text = f"{token.text.lower()} ... {main_conj.text.lower()}"
               
                meaning = COORDINATING_CONJUNCTIONS.get(main_conj.text.lower(), "แสดงความสัมพันธ์")

                explanation = {
                    "what_it_is": "Correlative conjunction คือคำสันธานคู่ที่ทำงานร่วมกันเพื่อเน้นย้ำความสัมพันธ์",
                    "effect_on_meaning": f"ใช้เพื่อ{meaning} โดยให้น้ำหนักแก่ทั้งสองส่วนเท่ากัน",
                    "usage_note": "โครงสร้างหลังคำทั้งสองต้องขนานกัน (Parallel Structure) เช่น Noun คู่ Noun หรือ Verb คู่ Verb",
                    "what_it_does_here": f"ในประโยคนี้ใช้คู่ '{pair_text}' เพื่อ{meaning}"
                }

                results.append({
                    "category": "Conjunction",
                    "topic": "Correlative conjunction",
                    "trigger": pair_text,
                    "explanation": explanation
                })
                
                processed_indices.add(token.i)
                processed_indices.add(main_conj.i)
                continue

        # sconj
        if token.pos_ == "SCONJ" and token.dep_ == "mark":
            meaning = SUBORDINATING_CONJUNCTIONS.get(token.text.lower(), "เชื่อมประโยคย่อย")
            clause = " ".join(t.text for t in token.head.subtree)
            
            results.append({
                "category": "Conjunction",
                "topic": "Subordinating conjunction",
                "trigger": token.text,
                "clause_or_span": clause,
                "explanation": {
                    "what_it_is": "Subordinating conjunction ใช้เชื่อมประโยคย่อยเข้ากับประโยคหลัก",
                    "effect_on_meaning": f"ใช้เพื่อ{meaning}",
                    "usage_note": "ประโยคย่อยที่ตามหลังคำนี้ไม่สามารถสื่อความหมายสมบูรณ์ได้ด้วยตัวเอง",
                    "what_it_does_here": f"ในประโยคนี้ '{token.text.lower()}' ทำหน้าที่{meaning}"
                }
            })
            processed_indices.add(token.i)

        # cconj
        elif token.pos_ == "CCONJ":
            meaning = COORDINATING_CONJUNCTIONS.get(token.text.lower(), "เชื่อมส่วนที่มีความสำคัญเท่ากัน")
            
            results.append({
                "category": "Conjunction",
                "topic": "Coordinating conjunction",
                "trigger": token.text,
                "explanation": {
                    "what_it_is": "Coordinating conjunction คือคำสันธานที่เชื่อมคำ กลุ่มคำ หรือประโยคที่มีระดับเดียวกัน",
                    "effect_on_meaning": f"ใช้เพื่อ{meaning}",
                    "usage_note": "หากเชื่อม Independent Clause สองประโยค ควรมีเครื่องหมาย comma (,) วางไว้ข้างหน้า",
                    "what_it_does_here": f"ในประโยคนี้ '{token.text.lower()}' {meaning}"
                }
            })
            processed_indices.add(token.i)

    return results