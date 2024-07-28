# Step 1: Reading the file
def read_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

feedback_file_path = 'Feedback.txt'
feedback_entries = read_file(feedback_file_path)
total_feedback = len(feedback_entries)
print(f"Total feedback entries: {total_feedback}")

# Step 2: Extracting Keywords
keywords = ["good", "bad", "excellent", "poor"]

def extract_keywords(feedback):
    keyword_counts = {key: 0 for key in keywords}
    for entry in feedback:
        for keyword in keywords:
            if keyword in entry.lower():
                keyword_counts[keyword] += 1
    return keyword_counts

keyword_counts = extract_keywords(feedback_entries)

# Step 3: Generating a Summary Report
def generate_summary(total, keyword_counts):
    summary = f"Total number of feedback entries: {total}\n"
    summary += "Keyword occurrences:\n"
    for keyword, count in keyword_counts.items():
        summary += f"{keyword}: {count}\n"
    return summary

summary_report = generate_summary(total_feedback, keyword_counts)
print(summary_report)

# Step 4: Saving the Report
def save_report(report, file_path):
    with open(file_path, 'w') as file:
        file.write(report)

report_file_path = r"C:\Users\User\Python Course SMIT\CustomerFeedbackProcessing\summary_report.txt"

# Save the report
save_report(summary_report, report_file_path)
print(f"Report saved successfully at {report_file_path}")
