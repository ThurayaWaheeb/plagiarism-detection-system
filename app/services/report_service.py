from datetime import datetime

def generate_plagiarism_report(filename, similarity, top_projects):

    similarity = round(similarity, 2)

    date = datetime.now().strftime("%Y-%m-%d")

    report = f"""
تقرير كشف الانتحال
================================

اسم الملف: {filename}
تاريخ الفحص: {date}

نسبة التشابه الكلية: {similarity} %

--------------------------------
المشاريع الأكثر تشابهًا
--------------------------------
"""

    for proj in top_projects:
        report += f"\n{proj['project_title']} — نسبة التشابه: {proj['similarity']}%"

    report += f"""


================================
PLAGIARISM REPORT
================================

File Name: {filename}
Checked At: {date}

Overall Similarity: {similarity} %

--------------------------------
Top Matching Projects
--------------------------------
"""

    for proj in top_projects:
        report += f"\n{proj['project_title']} — Similarity: {proj['similarity']}%"

    return {
        "report_text": report,
        "overall_similarity": similarity,
        "projects": top_projects
    }