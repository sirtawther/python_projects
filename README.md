## Script for Batch Deletion of Records from PostgreSQL Tables

This is a bash script that can be used to delete records from PostgreSQL tables in batches. It is useful when you want to delete a large number of records from a table and don't want to overload the server by deleting all the records at once.

### Usage

1. Replace `your_db_name` with the name of your PostgreSQL database.
2. Replace `table1`, `table2`, and `table3` in the `tables` array with the names of the tables you want to delete records from.
3. Set the `batch_size` variable to the number of records you want to delete in each batch.
4. Run the script using the command `bash batch_delete.sh`.

### Script Explanation

The script does the following:

1. Gets the IDs of all the records in the specified tables using a SQL query.
2. Deletes records in batches of size specified by `batch_size`.
3. Prints the number of records deleted and the number of records left to delete after each batch.
4. Deletes any remaining records that were not part of a batch.

### Example

Suppose you want to delete records from the `stock_move`, `stock_move_line`, and `stock_route_product` tables in a database named `my_db`, and you want to delete 100 records at a time. Here's how you would use the script:

1. Copy the script into a file named `batch_delete.sh`.
2. Open the file in a text editor and make the following changes:

database="my_db"
tables=("stock_move" "stock_move_line" "stock_route_product")
batch_size=100


3. Save the file.
4. Open a terminal window and navigate to the directory where the file is saved.
5. Run the script using the command `bash batch_delete.sh`.

### Notes

- This script assumes that each table has an `id` column that contains unique IDs for each record.
- If a table does not have an `id` column, you will need to modify the script to use a different column name.
- This script should be used with caution as it can potentially delete large amounts of data. Make sure to test it on a non-production environment before running it on a production database.
