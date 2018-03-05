"""
Integration style tests for the H5 pandas class.
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
subset = ["a", "b", "c"]
subset_key = "key"
h5df.save_slice(subset, subset_key)


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
    actual = h5df[subset]
    expected = df[subset]
    assert expected.equals(actual)


def test_row_access():
    actual = h5df.loc[subset]
    expected = df.loc[subset]
    assert expected.equals(actual)


def test_slice_retrieval():
    """Insert and retrieve a slice."""
    true_slice = subset
    slice_key = "key "
    h5df.save_slice(true_slice, slice_key)
    returned_slice = h5df.get_slice(slice_key)
    expected = pd.Series(true_slice)
    actual = pd.Series(returned_slice)
    assert expected.equals(actual)


def test_saved_slice_col_access():
    expected = df[subset]
    actual = h5df[subset_key]
    assert expected.equals(actual)


def test_saved_slice_row_access():
    expected = h5df.loc[subset_key]
    actual = df.loc[subset]
    assert expected.equals(actual)


def test_saved_slice_row_and_col_access():
    abc_rows_and_cols = h5df.loc[subset_key, subset_key]
    actual = abc_rows_and_cols
    expected = df.loc[subset, subset]
    assert expected.equals(actual)

def test_stored_slice_retrival_is_list():
    actual = h5df.get_saved_slices()
    expected = subset_key
    assert actual == expected

def test_stored_slice_retrival_is_list():
    saved_slices = h5df.get_saved_slices()
    test_passes = isinstance(saved_slices, list)
    assert test_passes

def test_values_of_stored_slice():
    actual = pd.Series(h5df.get_slice(subset_key))
    expected = pd.Series(subset)
    assert expected.equals(actual)

def test_get_all():
    actual = h5df.get()
    expected = df
    assert expected.equals(actual)
