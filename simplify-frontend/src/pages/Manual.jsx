import React from "react";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";

const Manual = () => {
  return (
    <div className="fredoka-font min-h-screen bg-white pt-16 flex">
      <Sidebar 
        isOpen={true}
        alwaysOpen={true}
        customColor="bg-gradient-to-t from-sky-200 to-white"
      />

      <div className="flex-1 flex flex-col">
        <Navbar disableHamburger={true} />

        <main className="flex-1 p-8 overflow-auto max-w-3xl mx-auto w-full ml-80">
          <h1 className="text-4xl font-bold mb-10 text-black border-b pb-4">
            User Manual
          </h1>

          {/* Introduction */}
          <section className="mb-10">
            <h2 className="text-2xl font-semibold mb-3">1. Introduction</h2>
            <p className="text-gray-700 leading-relaxed">
              เว็บแอปพลิเคชันนี้ถูกพัฒนาขึ้นเพื่อช่วยผู้เริ่มต้นเรียนภาษาอังกฤษ
              โดยสามารถปรับข้อความภาษาอังกฤษให้อ่านง่ายขึ้น (Text Simplification)
              พร้อมทั้งแสดงคำอธิบายคำศัพท์และโครงสร้างไวยากรณ์ที่เกี่ยวข้อง
              <br />เพื่อเสริมความเข้าใจอย่างเป็นระบบ
            </p>
          </section>

          {/* How to Use */}
          <section className="mb-10">
            <h2 className="text-2xl font-semibold mb-3">2. How to Use</h2>
            <ol className="list-decimal list-inside text-gray-700 space-y-2 leading-relaxed">
              <li>พิมพ์หรือวางข้อความภาษาอังกฤษลงในช่องกรอกข้อความ</li>
              <li>คลิกปุ่ม <strong>Simplify</strong></li>
              <li>ระบบจะแสดงข้อความที่ถูกปรับให้อ่านง่ายขึ้น</li>
              <li>
                คำที่มีการเปลี่ยนแปลงจะถูกไฮไลต์ และสามารถเลื่อนเมาส์เพื่อดูคำอธิบายเพิ่มเติมได้
              </li>
            </ol>
          </section>

          {/* Text Simplification */}
          <section className="mb-10">
            <h2 className="text-2xl font-semibold mb-3">
              3. Text Simplification
            </h2>
            <p className="text-gray-700 leading-relaxed">
              ระบบจะปรับคำศัพท์และโครงสร้างประโยคให้ง่ายต่อการอ่านและทำความเข้าใจ
              <br />โดยยังคงความหมายหลักของข้อความต้นฉบับไว้ให้มากที่สุด
            </p>
          </section>

          {/* Highlight */}
          <section className="mb-10">
            <h2 className="text-2xl font-semibold mb-3">
              4. Highlighted Words
            </h2>
            <p className="text-gray-700 leading-relaxed">
              คำหรือวลีที่มีการเปลี่ยนแปลงหลังจากการ Simplify
              จะถูกเน้นด้วยสีเพื่อให้ผู้ใช้สามารถสังเกตความแตกต่าง
              ระหว่างข้อความต้นฉบับและข้อความที่ปรับแล้วได้อย่างชัดเจน
              นอกจากนี้ระบบจะแสดงเส้นเน้นประโยคหลัก
              เพื่อช่วยให้ผู้เรียนเห็นโครงสร้างสำคัญของประโยคได้ง่ายขึ้น
            </p>
          </section>

          {/* Vocabulary */}
          <section className="mb-10">
            <h2 className="text-2xl font-semibold mb-3">
              5. Vocabulary Information
            </h2>
            <ul className="list-disc list-inside text-gray-700 space-y-2 leading-relaxed">
              <li>
                <strong>Definition:</strong> แสดงความหมายของคำศัพท์ทั้งภาษาไทยและภาษาอังกฤษ
              </li>
              <li>
                <strong>Synonym:</strong> คำศัพท์ที่มีความหมายใกล้เคียงกัน
              </li>
              <li>
                <strong>CEFR Level:</strong> ระดับความยากของคำศัพท์ตามมาตรฐานสากล (A1–C1)
              </li>
            </ul>
          </section>

          {/* Grammar */}
          <section className="mb-10">
            <h2 className="text-2xl font-semibold mb-3">
              6. Grammar Explanation
            </h2>
            <p className="text-gray-700 leading-relaxed">
              ระบบจะแสดงคำอธิบายเกี่ยวกับโครงสร้างไวยากรณ์ที่ปรากฏในประโยค
              <br />ทั้งในข้อความต้นฉบับและข้อความที่ผ่านการปรับแล้ว
              เพื่อช่วยให้ผู้ใช้เข้าใจหลักไวยากรณ์มากขึ้น
            </p>
          </section>

          {/* Notes */}
          <section>
            <h2 className="text-2xl font-semibold mb-3">
              7. Notes & Limitations
            </h2>
            <p className="text-gray-700 leading-relaxed">
              เครื่องมือนี้ออกแบบมาเพื่อสนับสนุนการเรียนรู้ภาษาอังกฤษระดับเริ่มต้น
              <br />จึงอาจไม่เหมาะสมกับข้อความเชิงวิชาการ
              หรือเนื้อหาทางเทคนิคที่มีความซับซ้อนสูง
            </p>
          </section>
        </main>
      </div>
    </div>
  );
};

export default Manual;