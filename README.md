# Where to Get Data

You'll need to download data from the National Center for Educaiton Statistics. They have a tool called [EDAT](https://nces.ed.gov/edat/) for pulling down data from longitudinal studies for your own analysis. Thisdemo uses the ELS data set. ELS is a set of data starting with 10th graders that follows them through life. At 12th grade the students were assesed again. Further assesments occured later after high school. For this demo, we care about

- Student data for the base year (data prefixed BY)
- Student data for the first follow up year, 12th grade (data prefixed with F1)

To get the appropriatte date, use EDAT, select ELS, navigate to "BY Weights and Composites" and "F1 Weights and Composites". Select "Tag All" for these selections. Select download, get csv data.

# Usage

With csv data,

```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python indexEls.py path_to.csv
```
