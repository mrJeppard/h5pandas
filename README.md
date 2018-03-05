# h5pandas
pandas like indexing syntax for a pandas dataframe stored in a .hdf
file. It also provides a persistent store for subsets of row or column
ids that can be used to index the matrix.

Needs:
 pandas==0.18.0
 pytables==3.2.2

 Should work with an anaconda env.


 H5pandas is a simple proxy class that does two things:

 1. Allows accessing a HDF5 pandas matrix with pandas indexing
 syntax, pandas.DataFrame[] and pandas.DataFrame.loc[].

 2. Lets a user store lists of column names and/or row names and use
 them for indexing.

    H5pandas requires that you have an hdf file with dataframes stored by:
    ```
        pandas.DataFrame.to_hdf(
            "path/to/h.hdf5",
            "key_for_my_dataframe",
            format="table"
        )
    ```
    Here's some example code describing all functionality in 40 lines.
    ```
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
     ```
