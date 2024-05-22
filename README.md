# FinanCal
Acquiring Spending Data for California Counties

## Features
- Scrapes California Spending Data for Informational purposes from https://counties.bythenumbers.sco.ca.gov and puts them into nested json files.

## Data
There is a lot of data to process, so sample data of the output is provided.

## How to Use
1. Make sure to have python and edge installed on your machine. If using a different web browser/driver, make sure to modify the code accordingly.

[Python Installation](https://www.python.org/downloads/)

[Edge Installation](https://www.microsoft.com/en-us/edge/download?form=MM1475)

2. cd into the project directory (wherever you saved it on your machine + "cd FinanCal")

3. Create a virtual environment with "python -m venv venv"
   
5. Activate environment (should be "venv\Scripts\activate" on windows OR "source venv/bin/activate" on Mac assuming the environment is named venv)
   
7. Install the requirements with "pip install -r requirements.txt".

8. Adjust the config.py file in the util folder for the depth if information wanted. Not recommended to go too high on "depth" variables. They will net much more information, but it will take a long time and computing resources past a depth of about 2.

9. Run the program with "python main.py".
   
10. It will generate a json file with nested information.


## Disclaimer
Please note that web scraping may be subject to legal restrictions depending on the website's terms of service. It is recommended to review and comply with the website's policies before using this scraper. 

## License
This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/). Feel free to use, modify, and distribute this tool according to the terms of the license.

For any questions or feedback, please contact [flatwhitecoffey@gmail.com](mailto:flatwhitecoffey@gmail.com). Thank you for using ContactCongress!
