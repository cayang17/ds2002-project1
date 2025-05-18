# DS2002 ETL Project

## Project Summary:
This ETL pipeline:
- Fetches repo metadata from the GitHub REST API
- Loads a local CSV dataset on Electric Vehicle Population
- Transforms and merges the datasets
- Stores the result in a SQLite database
- Outputs summary stats and error-handled logs

## To Run:
- unzip Electric_Vehicle_Population.csv.zip and ensure Electric_Vehicle_Population.csv is in data folder
```bash
pip install -r requirements.txt
python etl_processor.py
```

## Reflection
Building this ETL pipeline taught me a lot about structuring a data science workflow end-to-end. One of the biggest challenges was working with the GitHub API. Although the documentation was clear, parsing the JSON data and converting it into a clean, flat DataFrame required careful attention to nested structures. Another challenge was deciding how to merge two very different datasets, one about GitHub repositories and another about electric vehicles, in a way that still allowed for meaningful transformation and analysis.

On the other hand, loading and cleaning the CSV data was easier than expected, especially with the help of pandas. Once I identified unnecessary columns in the Electric Vehicle dataset, dropping and adding columns was straightforward, and the .to_csv() and .to_sql() methods made file conversion and storage seamless.

One thing that surprised me was how helpful SQLite can be as a lightweight tool for storing structured data. While I’ve previously used CSVs for simple data storage, I now see the benefits of having queryable databases even for small projects.

This project gave me a clearer understanding of how ETL tools are structured in the real world. I can definitely see myself reusing or adapting this kind of utility in future data projects, especially when dealing with external APIs or needing to convert between formats and persist results. It’s a solid foundation for automating small pipelines and getting data into analysis ready form.
