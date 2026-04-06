

SUBORDINATING_CONJUNCTIONS = {
    # Contrast / Concession
    "although": "แสดงความขัดแย้งหรือสิ่งที่ตรงข้ามกับความคาดหมาย",
    "though": "แสดงความขัดแย้ง",
    "even though": "แสดงความขัดแย้งอย่างชัดเจน",
    "whereas": "แสดงความแตกต่างหรือการเปรียบเทียบ",
    "while": "แสดงการเปรียบเทียบความแตกต่าง",

    # Reason / Cause
    "because": "แสดงเหตุผล",
    "since": "แสดงเหตุผลหรือเวลา",
    "as": "แสดงเหตุผลหรือเวลา",

    # Condition
    "if": "แสดงเงื่อนไข",
    "unless": "แสดงเงื่อนไขเชิงปฏิเสธ",
    "provided": "แสดงเงื่อนไข",
    "provided that": "แสดงเงื่อนไข",
    "as long as": "แสดงเงื่อนไข",

    # Time
    "when": "แสดงเวลา",
    "whenever": "แสดงเวลา",
    "before": "แสดงเวลาที่เกิดก่อน",
    "after": "แสดงเวลาที่เกิดหลัง",
    "until": "แสดงเวลาจนถึงจุดหนึ่ง",
    "once": "แสดงเวลาหลังจากเหตุการณ์หนึ่งเกิดขึ้น",

    # Purpose / Result
    "so that": "แสดงจุดประสงค์หรือผลลัพธ์",
    "in order that": "แสดงจุดประสงค์",

    # Manner
    "how": "แสดงวิธีการหรือรูปแบบที่บางสิ่งเกิดขึ้น",
}


COORDINATING_CONJUNCTIONS = {
    "and": "เชื่อมข้อมูลหรือเหตุการณ์เพิ่มเติม",
    "but": "แสดงความขัดแย้ง",
    "or": "แสดงทางเลือก",
    "nor": "เชื่อมประโยคปฏิเสธ",
    "for": "แสดงเหตุผล",
    "so": "แสดงผลลัพธ์",
    "yet": "แสดงความขัดแย้ง",
    
}

CORRELATIVE_PAIRS = {
    "either": "or",
    "neither": "nor",
    "both": "and",
    "not only": "but also"
}


RELATIVE_PRONOUNS = {
    "who": "ใช้แทนคน ทำหน้าที่เป็นประธานหรือกรรม",
    "whom": "ใช้แทนคน ทำหน้าที่เป็นกรรม",
    "which": "ใช้แทนสิ่งของหรือสัตว์",
    "that": "ใช้แทนคนหรือสิ่งของ (ใช้เฉพาะ defining relative clause)",
    "whose": "ใช้แทนคน สัตว์ หรือสิ่งของ แสดงความเป็นเจ้าของ",
}


RELATIVE_ADVERBS = {
    "where": "ใช้แทนสถานที่",
    "when": "ใช้แทนเวลา",
    "why": "ใช้แทนสาเหตุ",
}

PASSIVE_TYPE_EXPLANATIONS = {
    "be-passive": (
        "ในประโยคนี้ใช้โครงสร้าง passive มาตรฐาน "
        "เพื่อเน้นสิ่งที่ถูกกระทำมากกว่าผู้กระทำ"
    ),
    "get-passive": (
        "ในประโยคนี้ใช้ get-passive ซึ่งให้ความรู้สึกว่าเหตุการณ์ "
        "เกิดขึ้นกับประธานและอาจสื่อถึงผลกระทบหรือประสบการณ์"
    ),
    "reduced-passive": (
        "ในประโยคนี้เป็น reduced passive clause "
        "ทำหน้าที่ขยายคำนาม และย่อมาจากโครงสร้างที่มี 'was/were'"
    ),
}


INVERSION_TRIGGERS = {
    "negative": {
        "never", "rarely", "seldom", "hardly",
        "scarcely", "barely", "no", "not",
        "little"
    },
    "conditional": {
        "had", "were", "should"
    },
    "restrictive": {
        "only"
    }
}

TIMELINE_ORDER = [
    "Past Perfect Continuous",
    "Past Perfect",
    "Past Continuous",
    "Past Simple",
    "Present Perfect Continuous",
    "Present Perfect",
    "Present Continuous",
    "Present Simple",
    "Future (going to)",
    "Future Continuous",
    "Future Perfect Continuous",
    "Future Perfect",
    "Future Simple",
    "Modal",
]

TENSE_EFFECTS = {
    "Past Perfect Continuous": "ใช้บอกเหตุการณ์ที่ดำเนินต่อเนื่องก่อนจุดหนึ่งในอดีต",
    "Past Perfect": "ใช้บอกเหตุการณ์ที่เสร็จสิ้นก่อนเหตุการณ์อื่นในอดีต",
    "Past Continuous": "ใช้บอกเหตุการณ์ที่กำลังเกิดขึ้นในช่วงเวลาหนึ่งในอดีต",
    "Past Simple": "ใช้บอกเหตุการณ์ที่เกิดขึ้นและจบลงในอดีต",
    "Present Perfect Continuous": "ใช้บอกเหตุการณ์ที่เริ่มในอดีตและยังคงดำเนินต่อถึงปัจจุบัน",
    "Present Perfect": "ใช้บอกเหตุการณ์ในอดีตที่ส่งผลถึงปัจจุบัน",
    "Present Continuous": "ใช้บอกเหตุการณ์ที่กำลังเกิดขึ้นในขณะนี้",
    "Present Simple": "ใช้บอกข้อเท็จจริง นิสัย หรือสภาพทั่วไป",
    "Future (going to)": "ใช้บอกเหตุการณ์ในอนาคตที่วางแผนไว้แล้ว",
    "Future Continuous": "ใช้บอกเหตุการณ์ที่กำลังเกิดขึ้นในอนาคต",
    "Future Perfect Continuous": "ใช้บอกเหตุการณ์ที่จะดำเนินต่อเนื่องถึงจุดหนึ่งในอนาคต",
    "Future Perfect": "ใช้บอกเหตุการณ์ที่จะเสร็จสิ้นก่อนเวลาหนึ่งในอนาคต",
    "Future Simple": "ใช้บอกเหตุการณ์ที่จะเกิดขึ้นในอนาคต",
    "Modal": "ใช้แสดงความสามารถ ความเป็นไปได้ ความจำเป็น หรือข้อบังคับ",
}

TENSE_STRUCTURES = {
    "Past Perfect Continuous": "Subject + had been + V-ing",
    "Past Perfect": "Subject + had + V3",
    "Past Continuous": "Subject + was/were + V-ing",
    "Past Simple": "Subject + V2",
    "Present Perfect Continuous": "Subject + has/have been + V-ing",
    "Present Perfect": "Subject + has/have + V3",
    "Present Continuous": "Subject + am/is/are + V-ing",
    "Present Simple": "Subject + V1(s/es)",
    "Future (going to)": "Subject + am/is/are going to + V1",
    "Future Continuous": "Subject + will be + V-ing",
    "Future Perfect Continuous": "Subject + will have been + V-ing",
    "Future Perfect": "Subject + will have + V3",
    "Future Simple": "Subject + will + V1",
    "Modal": "Subject + modal verb + V1",
}