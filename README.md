This is a bash script that iterates over a list of tables and deletes records from each table in batches. Here's what the script does:

    Sets the database name and table names as variables.
    Sets the batch size to 100.
    Loops over each table name in the list.
    Executes a SQL query to get all the IDs in the table.
    Initializes variables for the count of deleted records, IDs to delete, and the total number of records.
    Starts a timer to measure how long it takes to delete records from the table.
    Loops over each ID and adds it to the IDs to delete string.
    When the batch size is reached, the script executes a DELETE query for the IDs in the string and updates the deleted count and IDs to delete variables.
    If there are any remaining IDs in the IDs to delete string, the script executes a DELETE query for those as well and updates the deleted count.
    Calculates the time it took to delete records from the table.
    Prints a message indicating how long it took to delete records from the table.
    Moves on to the next table in the list.
    When all tables have been processed, the script prints a message indicating that the script is complete.

Overall, this script is useful for deleting large numbers of records from multiple tables efficiently. It uses batch processing to delete records in chunks, which can help reduce the load on the database and make the deletion process faster.
