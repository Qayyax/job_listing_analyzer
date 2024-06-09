import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from fpdf import FPDF


data = pd.read_csv('jobs.csv')

# EDA
data_head = data.head()
data_info = data.info()
data_description = data.describe(include='all')

print(data_head)
print(data_info)
print(data_description)


# Counts for companies and locations
company_counts = data['company'].value_counts()
location_counts = data['location'].value_counts()

# Skills frequency
# Splitting the skills string into a list and flattening it
skills_series = data['skills'].dropna().apply(lambda x: x.split(','))
flattened_skills = [
    skill.strip() for sublist in skills_series for skill in sublist
]
skills_counts = Counter(flattened_skills)

print(company_counts.head(10))
print(location_counts.head(10))
print(skills_counts.most_common(10))

# Word cloud for skills
skills_text = ' '.join(flattened_skills)
wordcloud = WordCloud(
    width=800, height=400, background_color='white'
).generate(skills_text)


class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Job Market Analysis Report', 0, 1, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(2)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_table(self, data, col_widths, col_headers):
        self.set_font('Arial', 'B', 12)
        for i, header in enumerate(col_headers):
            self.cell(col_widths[i], 10, header, 1, 0, 'C')
        self.ln()
        self.set_font('Arial', '', 12)
        for row in data:
            for i, datum in enumerate(row):
                self.cell(col_widths[i], 10, str(datum), 1, 0, 'C')
            self.ln()

    def add_plot(self, image_path):
        self.image(image_path, w=180)


pdf = PDF()

pdf.add_page()

# Introduction
pdf.set_font('Arial', 'B', 16)
pdf.cell(0, 10, 'Introduction', 0, 1, 'L')
pdf.set_font('Arial', '', 12)
pdf.multi_cell(
    0,
    10,
    "This report provides an analysis of job postings data including basic "
    "statistics of companies and locations, as well as a visualization of "
    "skills distribution among the postings.",
)

# Basic Statistics
pdf.chapter_title('Basic Statistics - Companies')
pdf.add_table(
    company_counts.head(10).reset_index().values,
    [90, 90], ['Company', 'Number of Postings']
)

pdf.chapter_title('Basic Statistics - Locations')
pdf.add_table(
    location_counts.head(10).reset_index().values,
    [90, 90], ['Location', 'Number of Postings']
)

pdf.chapter_title('Basic Statistics - Skills')
pdf.add_table([
    list(item) for item in skills_counts.most_common(10)], [90, 90],
    ['Skill', 'Frequency']
)

# List of plots images name
plot_paths = [
    'location_postings.png', 'company_postings.png',
    'skills_wordcloud.png'
]
plt.figure(figsize=(12, 8))
location_counts.head(10).plot(kind='bar', color='skyblue')
plt.title('Number of Job Postings per Location')
plt.xlabel('Location')
plt.ylabel('Number of Postings')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(plot_paths[0])
plt.close()

plt.figure(figsize=(12, 8))
company_counts.head(10).plot(kind='bar', color='lightgreen')
plt.title('Number of Job Postings per Company')
plt.xlabel('Company')
plt.ylabel('Number of Postings')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(plot_paths[1])
plt.close()

wordcloud.to_file(plot_paths[2])

# Visualizations
pdf.chapter_title('Visualizations')
for path in plot_paths:
    pdf.add_plot(path)

# Output the PDF to a file
pdf.output('Job_Market_Analysis_Report.pdf')

print()
print("+" * 20)
print("Job Analysis has been exported as Job_Market_Analysis_Report.pdf")
print()
