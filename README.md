# Web Scraper Project

This is a Python project that performs web scraping on USP’s JúpiterWeb academic system to extract detailed information about:
* Teaching units
* Undergraduate courses
* Mandatory and optional subjects

After data extraction, the system allows interactive queries through a terminal interface.

## Authors

* Matheus Pereira Dias
* Daniel Contente Romanzini

## Features

The system enables:
1) Listing all courses grouped by unit;
2) Consulting a specific course (name, duration, subject list);
3) Viewing detailed data for all available courses;
4) Looking up a subject by code, including which courses offer it;
5) Finding subjects shared across multiple courses.

## Technologies Used
* Python 3
* Selenium + WebDriver (for browser automation and interaction)
* BeautifulSoup4 (for parsing HTML content)
* rich (for enhanced console output)

## Notes
* The scraping process may take a few minutes depending on the number of units selected.
* The USP website can occasionally be slow or unstable.
* Make sure Google Chrome is installed and that the correct version of ChromeDriver is available on your system path.

## Installation

### Clone the repository:

```
git clone https://github.com/matheuspd/Web-Scraper-Project.git
cd Web-Scraper-Project
```

### (Optional) Create a virtual environment:

```
python -m venv venv
source venv/bin/activate  # Linux/macOS
```

### Install the dependencies:

```
pip install -r requirements.txt
```

## How to use:

### Run the main program:

```
python3 main.py
```

### The program will ask a maximum number of units to process, enter a number higher than 0.

During execution, the program will automatically launch a browser using Selenium WebDriver, navigate through the USP system, and use BeautifulSoup to extract and process HTML content.

### After processing, you will see an interactive menu like this (in portuguese):

```
Enter the number corresponding to the query you want to perform:
1. List courses by unit
2. Show details for a specific course
3. Show details for all courses
4. Show information about a subject and which courses it belongs to
5. Show subjects that appear in more than one course
0. Exit
```

Enter the numbers of the options to obtain the desired answers and 0 when you want to exit the program.
