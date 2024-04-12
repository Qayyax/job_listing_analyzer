# job_listing_analyzer
---

# Project Overview

"Job Listing Analyser" is a command-line application designed to scrape job listings from a specified job website and analyze the collected data to provide insights into job market trends. The application outputs analyses such as the frequency of job titles, required skills, company names, and job locations. This tool is especially useful for job seekers, recruiters, and researchers interested in understanding the current demand in various job sectors.

## Features

- Scrape job listing data from web pages.
- Analyze job market trends based on location, company, and required skills.
- Generate CSV files with the scraped data.
- Provide visualizations and summary statistics of the analyzed data.

## Getting Started

These instructions will guide you on how to set up and run the "Job Listing Analyser" on your local machine for development and testing purposes.

## Prerequisites

Before you run the project, you need to have Python installed on your machine (Python 3.6 or later is recommended). You also need to install several Python libraries which the scripts depend on.

## Installation

Install the required Python libraries using pip:

```python
pip install pandas matplotlib beautifulsoup4 request wordcloud
```

## Project Structure

- **`main.py`**: Script to scrape job listings and save them to a CSV file.
- **`analysis.py`**: Script to analyze the scraped data and produce visualizations and summaries.

## Running the Project

Follow these steps to run the project

1. **Data Collection**:

Run `main.py` to start the scraping process. This script will ask you to input the job title you are searching for as well as your desired location, it will then scrape job listings and save them in a CSV file. 

```python
python main.py
```

2. **Data Analysis**:

After collecting the data, run `analysis.py` to analyze the data. This script reads the CSV file, performs statistical analysis, and generates visualizations, which are saved in a pdf file.

```python
python analysis.py
```

## Contributing

Feel free to fork this project and submit pull requests. You can also open issues for any bugs you find or enhancements you think would be useful.

## Authors

- Tife Olatunji - [Github profile](https://github.com/Qayyax)
