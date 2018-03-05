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
    print pd.__version__
    import tables
    print tables.__version__

    actual = h5df.loc["a"]
    expected = df.loc["a"]
    print actual
    print expected
    assert expected.equals(actual)


def test_single_col_access():
    """Column indexer handles a single string."""
    actual = h5df["a"]
    expected = df["a"]
    assert expected.equals(actual)


def test_col_access():
    """Test we can access the columns with the list API."""
    abc_cols = h5df[slice]
    assert df[slice].equals(abc_cols)


def test_row_access():
    abc_rows = h5df.loc[["a", "b", "c"]]
    assert df.loc[["a", "b", "c"]].equals(abc_rows)


def test_slice_retrieval():
    true_slice = ["a", "b", "c"]
    slice_key = "key "
    h5df.save_slice(true_slice, slice_key)
    returned_slice = h5df.get_slice(slice_key)
    assert pd.Series(true_slice).equals(pd.Series(returned_slice))


def test_saved_slice_col_access():
    assert h5df["key"].equals(df[["a", "b", "c"]])


def test_saved_slice_row_access():
    assert h5df.loc["key"].equals(df.loc[["a", "b", "c"]])


def test_saved_slice_row_and_col_access():
    abc_rows_and_cols = h5df.loc["key", "key"]
    assert abc_rows_and_cols.equals(
        df.loc[["a", "b", "c"], ["a", "b", "c"]]
    )

def test_stored_slice_retrival():
    saved_slices = h5df.get_saved_slices()
    assert isinstance(saved_slices, list) and saved_slices[0] == "key"

def test_values_of_stored_slicce():
    retrieved_slice = h5df.get_slice("key")
    assert pd.Series(slice).equals(pd.Series(retrieved_slice))

def test_get_all():
    actual = h5df.get()
    expected = df
    assert expected.equals(actual)
