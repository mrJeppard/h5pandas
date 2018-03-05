"""
Example usage of H5pandas class.
"""
from h5pandas import H5pandas
import pandas as pd

# Make some data and toss it in a dataframe.
data = [range(5), range(5), range(5), range(5), range(5)]
names = ["a", "b", "c", "d", "e"]
df = pd.DataFrame(data, columns=names, index=names)
print df

# Save it to hdf in "table" format
hdf_file = "example.hdf"
df_key = "example"
df.to_hdf(hdf_file, df_key, format="table")

# Point to it with the H5pandas class. This doesn't read anything in
# memory.
pd_access = H5pandas(hdf_file, df_key)

# Read in columns using familiar syntax of pandas.
# Below, abc_cols is your pandas dataframe with columns
# ["a","b","c"] and all rows.
abc_cols = pd_access[["a", "b", "c"]]
print abc_cols

# Read in rows using the familiar syntax of pandas.
# Below, abc_rows is a pandas dataframe with rows ["a","b","c"]
# and all columns.
abc_rows = pd_access.loc[["a", "b", "c"]]
print abc_rows

# Define a slice in the persistent store.
pd_access.save_slice(["a", "b", "c"], "slice")
pd_access.get_slice("slice")

# Access the stored slice directly through the indexer.
print pd_access["slice"].equals(abc_cols)  # True

# You can use that same slice to access those rows, as long as
# they are valid row indices in the dataframe.
print pd_access.loc["slice"].equals(abc_rows)  # True

# Of course, .loc[] can access both rows and columns.
# So we can do stuff like:
abc_rows_and_cols = pd_access.loc["saved slice", "saved slice"]
print abc_rows_and_cols.equals(abc_rows["a","b","c"])  # True

# The saved slices are stored in the hdf file, so you can
# share that file with a colleague and they will have access
# to all your saved sets of row and column names.

# Take a peak at the stored slices.
saved_slices = pd_access.get_saved_slices()
print saved_slices  # ["memorable name"]

# And see what ids are stored in the slice
print pd_access.get_slice(saved_slices[0])  # ["a", "b", "c"]

# Or read the whole dataframe into memory if you'd like.
df = pd_access.get()

# Enjoy!
