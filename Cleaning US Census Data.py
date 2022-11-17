# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.1
#   kernelspec:
#     display_name: Python 3.11.0 64-bit
#     language: python
#     name: python3
# ---

from glob import iglob
import matplotlib.pyplot as plt
import pandas as pd

# # Cleaning US Census Data

# You just got hired as a Data Analyst at the Census Bureau, which collects census data and creates interesting visualizations and insights from it.
#
# The person who had your job before you left you all the data they had for the most recent census. It is in multiple `csv` files. They didn't use pandas, they would just look through these `csv` files manually whenever they wanted to find something. Sometimes they would copy and paste certain numbers into Excel to make charts.
#
# The thought of it makes you shiver. This is not scalable or repeatable.
#
# Your boss wants you to make some scatterplots and histograms by the end of the day. Can you get this data into `pandas` and into reasonable shape so that you can make these histograms?

# ## Inspect the Data!

# 1. The first visualization your boss wants you to make is a scatterplot that shows average income in a state vs proportion of women in that state.
#
#    Open some of the census `csv` files that came with the kit you downloaded. How are they named? What kind of information do they hold? Will they help us make this graph?

with open(r"states0.csv", "r") as state:
    [print(f"{_}") for _ in state]

# 2. It will be easier to inspect this data once we have it in a DataFrame. You can't even call `.head()` on these `csv`s! How are you supposed to read them?
#
#    Using `glob`, loop through the census files available and load them into DataFrames. Then, concatenate all of those DataFrames together into one DataFrame, called something like `us_census`.

# +
# '*' wildcard used to recognise all csv files containg 'states' as the prefix.
path = r"C:\Users\Akhil\Desktop\Codecademy\Cleaning US Census Data\states*.csv"

# Creating a generator object that will iterate over all the files in the path.
files = iglob(f"{path}")
dataframes = (pd.read_csv(f) for f in files)

us_census = pd.concat(dataframes, ignore_index=True)
# -

# 3. Look at the `.columns` and the `.dtypes` of the `us_census` DataFrame. Are those datatypes going to hinder you as you try to make histograms?

print(us_census.columns, end="\n\n")
print(us_census.dtypes)

# 4. Look at the `head()` of the DataFrame so that you can understand why some of these `dtypes` are objects instead of integers or floats.
#
#    Start to make a plan for how to convert these columns into the right types for manipulation.

us_census.head()

# ## Regex to the Rescue

# 5. Use regex to turn the `Income` column into a format that is ready for conversion into a numerical type.

# +
us_census["Income"] = us_census["Income"].str.replace(r"[$]|,", "", regex=True)
us_census["Income"] = pd.to_numeric(us_census["Income"])

us_census.head()
# -

# 6. Look at the `GenderPop` column. We are going to want to separate this into two columns, the `Men` column, and the `Women` column.
#
#    Split the column into those two new columns using `str.split` and separating out those results.

us_census[["Men", "Women"]] = us_census["GenderPop"].str.split("_", expand=True)
us_census.head()

# 7. Convert both of the columns into numerical datatypes.
#
#    There is still an `M` or an `F` character in each entry! We should remove those before we convert.

# +
us_census[["Men", "Women"]] = us_census[["Men", "Women"]].replace(
    r"M|F", "", regex=True
)

us_census[["Men", "Women"]] = us_census[["Men", "Women"]].apply(
    pd.to_numeric, errors="coerce"
)

us_census.dtypes
# -

# 8. Now you should have the columns you need to make the graph and make sure your boss does not slam a ruler angrily on your desk because you've wasted your whole day cleaning your data with no results to show!
#
#    Use matplotlib to make a scatterplot!
#
#    ```py
#    plt.scatter(the_women_column, the_income_column)
#    ```
#
#    Remember to call `plt.show()` to see the graph!

plt.scatter(us_census["Women"], us_census["Income"])
plt.title("Scatter Plot of Income vs. Number of Women per State")
plt.xlabel("Population of Women per State")
plt.ylabel("Income (in US Dollars)")
plt.show()
plt.clf()

# 9. You want to double check your work. You know from experience that these monstrous csv files probably have `nan` values in them! Print out your column with the number of women per state to see.
#
#    We can fill in those `nan`s by using pandas' `.fillna()` function.
#
#    You have the `TotalPop` per state, and you have the `Men` per state. As an estimate for the `nan` values in the `Women` column, you could use the `TotalPop` of that state minus the `Men` for that state.
#
#    Print out the `Women` column after filling the `nan` values to see if it worked!

us_census["Women"] = us_census["Women"].fillna(us_census["TotalPop"] - us_census["Men"])
print(us_census["Women"].head())

# 10. We forgot to check for duplicates! Use `.duplicated()` on your `census` DataFrame to see if we have duplicate rows in there.

no_duplicates = us_census.duplicated(subset=us_census.columns[1:])
print(no_duplicates.head(10))

# 11. Drop those duplicates using the `.drop_duplicates()` function.

census = us_census.drop_duplicates(subset=us_census.columns[1:])
census

# 12. Make the scatterplot again. Now, it should be perfect! Your job is secure, for now.

plt.scatter(us_census["Women"], us_census["Income"])
plt.title("Scatter Plot of Income vs. Number of Women per State")
plt.xlabel("Population of Women per State")
plt.ylabel("Income (in US Dollars)")
plt.show()
plt.clf()

# ## Histogram of Races

# 13. Now your boss wants you to make a bunch of histograms out of the race data that you have. Look at the `.columns` again to see what the race categories are.

print(us_census.columns)

# 14. Try to make a histogram for each one!
#
#     You will have to get the columns into the numerical format, and those percentage signs will have to go.
#
#     Don't forget to fill the `nan` values with something that makes sense! You probably dropped the duplicate rows when making your last graph, but it couldn't hurt to check for duplicates again.

# +
# ['Hispanic', 'White', 'Black', 'Native', 'Asian', 'Pacific']
race_data = us_census.columns[3:9]

us_census_unique = us_census.drop_duplicates(subset=us_census[1:])

# Remove '%' signs and convert values to numeric
for group in race_data:
    df = us_census_unique[group].replace(r"(%)", "", regex=True)
    us_census_unique[group] = df.apply(pd.to_numeric, errors="coerce")

us_census_unique["Pacific"] = us_census_unique["Pacific"].fillna(
    100
    - us_census_unique["Hispanic"]
    - us_census_unique["White"]
    - us_census_unique["Black"]
    - us_census_unique["Native"]
    - us_census_unique["Asian"]
)

for race in race_data:
    plt.hist(us_census_unique[race])
    plt.title(f"Histogram of the Percentage of {race} People per State")
    plt.xlabel("Percentage")
    plt.ylabel("Frequency")
    plt.show()
    plt.clf()

# -

# ## Get Creative

# 15. Phew. You've definitely impressed your boss on your first day of work.
#
#     But is there a way you really convey the power of pandas and Python over the drudgery of `csv` and Excel?
#
#     Try to make some more interesting graphs to show your boss, and the world! You may need to clean the data even more to do it, or the cleaning you have already done may give you the ease of manipulation you've been searching for.

for _ in race_data:
    plt.bar(x=_, height=us_census_unique[_])
    plt.title(f"Bar Graph of the Percentage of {race} People per State")
    plt.xlabel("Percentage")
    plt.ylabel("Frequency")
