"""
Author: Duncan McColl, duncmc831@gmail.com

H5pandas provides pandas like indexing syntax for a pandas object stored
in a .hdf file. It also provides a persistent store for subsets of
row or column ids that can be used to index the matrix.

Everything you need to know can be found by:
> from h5pandas import H5pandas
> help(h5pandas)
"""
import pandas as pd


class H5pandas(object):
    """
    H5pandas is a simple proxy class that does two things:

        Allows accessing a HDF5 pandas matrix with pandas indexing
        syntax, i.e. pandas.DataFrame[] and pandas.DataFrame.loc[].

        Lets a user store lists of column names and/or row names and use
        them with the provided indexing.

    H5pandas requires that you have an hdf file with dataframes stored:
        pandas.DataFrame.to_hdf(
        "path/to/h.hdf5",
        "key_for_my_dataframe",
        format="table"
        )

    Here's some example code describing all functionality in 40 lines.

        # pd_access points to the dataframe in your hdf file.
        pd_access = H5pandas("path/to/h.hdf5", "key_for_my_dataframe")

        # Access columns using the familiar syntax of pandas.
        # Below, abc_cols is your pandas dataframe with columns
        # ["a","b","c"] and all rows.
        abc_cols = pd_access[["a","b","c"]]

        # Access rows using the familiar syntax of pandas.
        # Below, abc_rows is a pandas dataframe with rows ["a","b","c"]
        # and all columns.
        abc_rows = pd_access.loc[["a","b","c"]]

        # You have a persistent store for defined slices.
        pd_access.save_slice(["a", "b", "c"], "saved slice")

        # Access the stored slice directly through the indexer.
        print pd_access["saved slice"].equals(abc_cols) # True

        # You can use that same slice to access those rows, as long as
        # they are valid row indices in the dataframe.
        print pd_access.loc["saved slice"].equals(abc_rows) # True

        # Of course, .loc[] can access both rows and columns.
        # So we can do stuff like:
        abc_rows_and_cols = pd_access.loc["saved slice", "saved slice"]
        print abc_rows_and_cols.equals(abc_rows["a","b","c"]) # True

        # The saved slices are stored in the hdf file, so you can
        # share that file with a colleague and they will have access
        # to all your saved sets of row and column names.

        # Take a peak at the stored slices.
        saved_slices = pd_access.get_saved_slices()
        print saved_slices #  ["memorable name"]

        # And see what ids are stored in the slice
        print pd_access.get_slice(saved_slices[0]) # ["a", "b", "c"]

        # Or read the whole dataframe into memory.
        df = pd_access.get()
    """
    def __init__(self, hdf5_file, group_key):
        """
        :param hdf5_file: string "path/to/hdf_file.hdf"
        :param group_key: string "key_you_saved_the_dataframe_with"
        :return: H5pandas Object.
        """
        self.hdf5_file = hdf5_file
        self.HDFStore = pd.HDFStore(hdf5_file)
        self.group_key = group_key
        self.loc = _LocIndexer(self)

    def get(self):
        """Return the entire pandas dataframe."""
        return self.HDFStore.select(self.group_key)

    def __getitem__(self, item):
        """Mimic pandas.DataFrame indexing."""
        item_is_single_colid = False
        if isinstance(item, str):
            if item in self.get_saved_slices():
                item = self.get_slice(item)
            else:
                # The string is not recognized as a group key.
                item_is_single_colid = True
                # Access the single column.
                data = self.HDFStore.select(
                    self.group_key,
                    columns=item
                )


        data = self.HDFStore.select(self.group_key, columns=item)
        if item_is_single_colid:
            # Return a pandas.Series in accordance with their interface.
            data = data[item]

        return data

    def get_slice(self, slice_key):
        """Return a saved slice given the slice id."""
        return self.HDFStore.get("slices/" + slice_key).tolist()

    def save_slice(self, key_array, slice_key):
        """Save an array of indexing keys for later use."""
        self.HDFStore.put(
            "slices/" + slice_key,
            value=pd.Series(key_array)
        )

    def get_saved_slices(self):
        """Return a list of all saved slices."""
        saved = [x[8:] for x in self.HDFStore.keys() if "/slices/" in x]
        return saved


class _LocIndexer(object):
    """Provides pandas.DataFrame.iloc[] syntax to H5pandas."""
    def __init__(self, H5DataFrame):
        self.H5DataFrame = H5DataFrame

    def __getitem__(self, item):
        """Mimic pandas.DataFrame.iloc[] syntax."""

        item_is_index_string = False
        if isinstance(item, list):
            row_slice = item
            col_slice = None
        else:
            if isinstance(item, str):
                try:
                    col_slice = None
                    row_slice = self.H5DataFrame.get_slice(item)
                except (KeyError, TypeError):
                    row_slice = item
                    item_is_index_string = True
            else:
                try:
                    row_slice = self.H5DataFrame.get_slice(item[0])
                except (KeyError, TypeError):
                    row_slice = item[0]
                    pass

                try:
                    col_slice = self.H5DataFrame.get_slice(item[1])
                except (KeyError, TypeError, IndexError) as e:
                    if isinstance(e, IndexError):
                        col_slice = None
                    else:
                        col_slice = item[1]

        data = self.H5DataFrame.HDFStore.select(
            self.H5DataFrame.group_key,
            where='index=row_slice',
            columns=col_slice
        )

        if item_is_index_string:
            # Mimic pandas by returning a pandas.Series.
            data = data.loc[item]

        return data

