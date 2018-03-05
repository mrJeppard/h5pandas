"""
Integration style tests for the H5 pandas class.

todo: need to test accessing a single string from iloc
    check out the use of fixtures hear and see if you can clean up
    test input.
"""
from h5pandas import H5pandas
import pandas as pd

# Make a dataframe to test with.
df = pd.DataFrame(
    [range(5), range(5), range(5), range(5), range(5)],
    columns=["a", "b", "c", "d", "e"],
    index=["a", "b", "c", "d", "e"]
)

# Save the dataframe to hdf in "table" format 
hdf_file = "test.hdf5"
df_key = "example"
df.to_hdf(hdf_file, df_key, format="table")

# The instance we'll be testing
h5df = H5pandas(hdf_file, df_key)

# Put a slice in the test.hdf5 file.
slice = ["a", "b", "c"]
slice_key = "key"
h5df.save_slice(slice, slice_key)


def test_single_row_access():
    actual = h5df.loc["a"]
    expected = df.loc["a"]
    assert expected.equals(actual)


def test_single_col_access():
    """Column indexer handles a single string."""
    actual = h5df["a"]
    expected = df["a"]
    assert expected.equals(actual)


def test_col_access():
    """Test we can access the columns with the list API."""
    actual = h5df[slice]
    expected = df[slice]
    assert expected.equals(actual)


def test_row_access():
    actual = h5df.loc[["a", "b", "c"]]
    expected = df.loc[["a", "b", "c"]]
    assert expected.equals(actual)


def test_slice_retrieval():
    """Insert and retrieve a slice."""
    true_slice = ["a", "b", "c"]
    slice_key = "key "
    h5df.save_slice(true_slice, slice_key)
    returned_slice = h5df.get_slice(slice_key)
    expected = pd.Series(true_slice)
    actual = pd.Series(returned_slice)
    assert expected.equals(actual)


def test_saved_slice_col_access():
    expected = df[["a", "b", "c"]]
    actual = h5df["key"]
    assert expected.equals(actual)


def test_saved_slice_row_access():
    expected = h5df.loc["key"]
    actual = df.loc[["a", "b", "c"]]
    assert expected.equals(actual)


def test_saved_slice_row_and_col_access():
    abc_rows_and_cols = h5df.loc["key", "key"]
    actual = abc_rows_and_cols
    expected = df.loc[["a", "b", "c"], ["a", "b", "c"]]
    assert expected.equals(actual)

def test_stored_slice_retrival_is_list():
    actual = h5df.get_saved_slices()
    expected = "key"
    assert actual == expected

def test_stored_slice_retrival_is_list():
    saved_slices = h5df.get_saved_slices()
    test_passes = isinstance(saved_slices, list)
    assert test_passes

def test_values_of_stored_slice():
    actual = pd.Series(h5df.get_slice("key"))
    expected = pd.Series(slice)
    assert expected.equals(actual)

def test_get_all():
    actual = h5df.get()
    expected = df
    assert expected.equals(actual)
