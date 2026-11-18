import datetime
import os
import fitz


def read_file(filepath):
    if os.path.exists(filepath):
        with open(filepath) as f:
            return f.read()
    return None


repo = os.environ.get("GITHUB_REPOSITORY", "unknown/repo")
run_id = os.environ.get("GITHUB_RUN_ID", "unknown")
run_number = os.environ.get("GITHUB_RUN_NUMBER", "unknown")
workflow = os.environ.get("GITHUB_WORKFLOW", "unknown")
commit_sha = os.environ.get("GITHUB_SHA", "unknown")

date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

outputs = {
    "Supervised": read_file("super_output.txt"),
    "Unsupervised": read_file("unsuper_output.txt"),
}


report = f"""
Coursework Status Report

Repository:
https://github.com/{repo}

Workflow:
{workflow}

Run Number:
{run_number}

Run ID:
{run_id}

Commit SHA:
{commit_sha}

Generated:
{date_time}

========================================

"""

for stage, output in outputs.items():
    if output is None:
        report += f"\n{stage}: NOT RUN\n"
    elif "Ready to commit and push" in output:
        report += f"\n{stage}: PASS\n"
    else:
        report += f"\n{stage}: ISSUES FOUND\n"


report += "\n\n========================================\n"
report += "Detailed Output\n"
report += "========================================\n"

for stage, output in outputs.items():
    report += f"\n\n--- {stage} ---\n\n"

    if output:
        report += output[:10000]
    else:
        report += "No output available."


doc = fitz.open()

page = doc.new_page()
page.insert_text(
    (50, 50),
    report,
    fontsize=10,
)

doc.save("ci_report.pdf")
doc.close()
