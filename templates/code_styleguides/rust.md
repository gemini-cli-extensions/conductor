### **Rust Development Guide: The Sovereign & Toyota Way**

เอกสารนี้คือมาตรฐานสูงสุดและเป็นข้อบังคับสำหรับการพัฒนาโปรเจกต์ด้วยภาษา Rust ทั้งหมด โดยผสานหลักการ **Sovereign AI (Batuta Stack)**, **Toyota Way (Jidoka, Five Whys)**, และแนวปฏิบัติที่ดีที่สุดของ Rust เข้าไว้ด้วยกัน

#### **ส่วนที่ 1: ปรัชญาและหลักการพื้นฐาน (Core Philosophy)**

1.  **Sovereign AI (ความเป็นอิสระทางปัญญาประดิษฐ์):**
    *   **นโยบาย 80/20:** **บังคับใช้** สัดส่วน **80% Batuta Stack** และ **ไม่เกิน 20% External Dependencies**
    *   **ลดความเสี่ยง Supply Chain:** การพึ่งพาเครื่องมือภายในช่วยให้เราควบคุมคุณภาพ, ความปลอดภัย, และประสิทธิภาพได้อย่างเต็มที่
    *   **ขั้นตอนก่อนเพิ่ม Dependency ใหม่:**
        1.  **ตรวจสอบ Batuta Stack ก่อนเสมอ:** `ls /home/noah/src/ | grep -E "^(aprender|trueno|...)"`
        2.  **ต่อยอดหากใกล้เคียง:** ถ้า Batuta Stack มีฟังก์ชันใกล้เคียง 70%+ ให้ต่อยอดแทนการเพิ่ม dependency ใหม่
        3.  **บันทึกเหตุผล:** หากจำเป็นต้องใช้ dependency ภายนอก ให้บันทึกเหตุผลที่ไม่สามารถใช้ Batuta Stack ได้ใน Pull Request อย่างชัดเจน

2.  **The Toyota Way (วิถีแห่งโตโยต้า):**
    *   **Jidoka (Automation with a Human Touch - คุณภาพในตัว):** สร้างระบบคุณภาพอัตโนมัติที่สามารถหยุดกระบวนการได้ทันทีเมื่อพบปัญหา (Andon Cord) เราใช้ Pre-commit/Pre-push hooks และ CI/CD เป็นเครื่องมือหลักในการทำ Jidoka
    *   **Five Whys (ถามว่า "ทำไม" 5 ครั้ง):** เป็น **วิธีการ Debugging ที่ยอมรับเพียงวิธีเดียว** (`pmat five-whys`) เพื่อค้นหารากเหง้าของปัญหา (Root Cause) แทนการแก้ที่ปลายเหตุ
    *   **Genchi Genbutsu (ไปดูให้เห็นกับตา):** การตัดสินใจต้องอยู่บนพื้นฐานของ "ข้อเท็จจริง" และ "ข้อมูล" ที่เก็บรวบรวมจากเครื่องมือวัดผลของเรา (เช่น `pmat rust-project-score`, `pmat context`) ไม่ใช่ความรู้สึก
    *   **Kaizen (การปรับปรุงอย่างต่อเนื่อง):** ทุกครั้งที่พบ Root Cause จาก Five Whys เราต้องปรับปรุงกระบวนการเพื่อป้องกันไม่ให้เกิดซ้ำ

3.  **Idiomatic & Performant Rust:**
    *   **Safety First:** ใช้ระบบ Ownership และ Borrowing อย่างเต็มประสิทธิภาพ หลีกเลี่ยง `unsafe` โดยเด็ดขาด
    *   **Zero-Cost Abstractions:** ออกแบบโค้ดให้มีประสิทธิภาพสูงสุดโดยไม่สูญเสียความสามารถในการอ่าน
    *   **Clarity & Readability:** เขียนโค้ดที่สื่อความหมายได้ด้วยตัวเอง

#### **ส่วนที่ 2: มาตรฐานการพัฒนาและเครื่องมือ (Development Standards & Tooling)**

1.  **การจัดการ Dependencies (Batuta Stack First):**
    *   **เครื่องมือหลัก:** ใช้ไลบรารีจาก **Batuta Stack** เป็นอันดับแรก (เช่น `aprender`, `trueno`, `presentar-core`)
    *   **เครื่องมือพื้นฐานที่อนุญาต:** `rand`, `rayon` ถือเป็นส่วนพื้นฐานที่ยอมรับได้
    *   **การตรวจสอบ:** ใช้ `cargo-deny` เพื่อบังคับใช้นโยบายเกี่ยวกับ licenses และที่มาของ dependencies
    *   **เครื่องมือ Coverage:** **ห้ามใช้ `cargo-tarpaulin` โดยเด็ดขาด** ให้ใช้ **`cargo llvm-cov`** เท่านั้น

2.  **การจัดการคุณภาพอัตโนมัติ (O(1) Quality Gates & Jidoka):**
    *   **Pre-commit Hooks:** **บังคับใช้** เพื่อตรวจสอบคุณภาพโค้ดในเวลา <30ms ก่อนการ commit
        *   **`bashrs`:** Linting สำหรับ `bash` และ `Makefile`
        *   **Metric Validation:** ตรวจสอบ Thresholds จาก `.pmat-metrics.toml` (lint time, test time, binary size)
        *   **Documentation Accuracy:** ตรวจสอบความถูกต้องของ `README.md`, `CLAUDE.md` ฯลฯ ด้วย `pmat validate-readme` เพื่อป้องกัน Hallucination
    *   **Pre-push Hooks:** **บล็อกการ push** หาก book/documentation ที่เกี่ยวข้องยังไม่ได้ push เพื่อป้องกัน Code/Docs Drift
    *   **Golden Tracing (`renacer`):** **บังคับใช้** สำหรับโปรเจกต์ประเภท Transpiler หรือ Distributed Systems เพื่อจับภาพและตรวจสอบพฤติกรรมการทำงานที่คาดหวัง

3.  **การเขียนโค้ดและการจัดรูปแบบ:**
    *   **การตั้งชื่อ:** `PascalCase` สำหรับ Types, `snake_case` สำหรับ Functions/Variables, `SCREAMING_SNAKE_CASE` สำหรับ Constants
    *   **การจัดรูปแบบ:** ใช้ `rustfmt` โดยตั้งค่า `max_width = 100` ใน `rustfmt.toml`
    *   **Linter:** ใช้ `clippy` และแก้ไข warnings ทั้งหมด (`cargo clippy -- -D warnings`)

4.  **การจัดการข้อผิดพลาดและเอกสาร:**
    *   **Error Handling:** ใช้ `thiserror` สำหรับ Libraries และ `anyhow` สำหรับ Applications
    *   **Documentation:** ใช้ `///` และ `//!` พร้อมทั้งมีส่วน `# Examples`, `# Errors`, และ `# Panics` ที่ชัดเจน

5.  **การทดสอบ (Testing Excellence):**
    *   **Unit & Integration Tests:** วางใน `mod tests` และ `tests/` ตามลำดับ
    *   **Test Coverage:** ตั้งเป้าหมายที่ ≥85% line coverage โดยใช้ `cargo llvm-cov`
    *   **Property-Based Testing:** ใช้ `probar` (จาก Batuta Stack) แทน `quickcheck`
    *   **การจัดการ Test ที่ `#[ignore]`:** ต้องมีเอกสารอธิบายเหตุผลที่ชัดเจนและแผนในการกลับมาแก้ไข การลดจำนวน `#[ignore]` คือตัวชี้วัดความก้าวหน้า

6.  **การจัดการโปรเจกต์และคำสั่ง:**
    *   **Command Runner:** ใช้ `just` ผ่าน `justfile` เพื่อสร้าง Task ที่เป็นมาตรฐานและทำงานซ้ำได้
    *   **Build Scripts:** ใช้ `build.rs` สำหรับ Code Generation (เช่น `prost-build`)
    *   **Branching Strategy:** **Always walk of master. We don't do branching.** (ทำงานบน master โดยตรง ไม่มีการแตก branch)

#### **ส่วนที่ 3: กระบวนการทำงานที่บังคับใช้ (Mandatory Workflows)**

1.  **Workflow การ Debugging (The ONLY acceptable method):**
    1.  พบปัญหา (Symptom)
    2.  รัน `pmat five-whys "Symptom description"`
    3.  วิเคราะห์ Root Cause ที่ได้จากรายงาน
    4.  แก้ไขที่ Root Cause
    5.  เพิ่ม Test Case เพื่อป้องกันการเกิดซ้ำ (Kaizen)

2.  **Workflow การเพิ่ม Feature หรือแก้ไขโค้ด:**
    1.  เขียนโค้ดตามมาตรฐานในเอกสารนี้
    2.  (ถ้ามี) อัปเดตเอกสาร `pmat-book` หรือ `README.md` ที่เกี่ยวข้อง
    3.  รัน `make validate-book` หรือ `pmat validate-readme` เพื่อตรวจสอบความถูกต้อง
    4.  รัน `renacer validate` (ถ้าเป็นโปรเจกต์ที่ใช้ Golden Tracing)
    5.  `git commit`: Pre-commit hooks จะทำงานอัตโนมัติ (O(1) Quality Gates)
    6.  `git push`: Pre-push hooks จะทำงานอัตโนมัติเพื่อตรวจสอบว่า docs ถูก push แล้ว

3.  **Workflow การ Release (เช่น `cargo publish`):**
    1.  ตรวจสอบให้แน่ใจว่า `pmat-book` และ docs ทั้งหมดถูก push และ deploy สำเร็จแล้ว
    2.  รัน `make validate-book` และ `pmat rust-project-score --full`
    3.  ตรวจสอบว่าผลลัพธ์ผ่านเกณฑ์ที่กำหนด
    4.  ดำเนินการ publish