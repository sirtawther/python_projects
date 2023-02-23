#!/bin/bash

database="your_db_name"
tables=("table1" "table2" "table3") # Replace with your table names
batch_size=100

for table in "${tables[@]}"; do
    if psql -d $database -t -c "SELECT EXISTS(SELECT 1 FROM information_schema.columns WHERE table_name = '$table' AND column_name = 'id')" | grep -q 't'; then
        count=$(psql -d $database -t -c "SELECT COUNT(*) FROM $table")
        if [ $count -eq 0 ]; then
            echo "Table $table is empty. Skipping deletion."
        else
            ids=$(psql -d $database -t -c "SELECT id FROM $table")
            total=$(echo "$ids" | wc -l)
            count=0
            deleted_count=0
            ids_to_delete=""
            echo "Deleting records from $table table..."
            start_time=$(date +%s)
            while read -r id; do
                ((count++))
                ids_to_delete="$ids_to_delete,$id"
                if [ $count -eq $batch_size ]; then
                    psql -d $database -t -q -c "DELETE FROM $table WHERE id IN (${ids_to_delete#,})"
                    ((deleted_count+=$count))
                    echo "$deleted_count row(s) deleted, $(($total - $deleted_count)) row(s) left"
                    count=0
                    ids_to_delete=""
                fi
            done <<< "$ids"

            # Delete any remaining records
            if [ ! -z "$ids_to_delete" ]; then
                psql -d $database -t -q -c "DELETE FROM $table WHERE id IN (${ids_to_delete#,})"
                ((deleted_count+=$(echo "$ids_to_delete" | wc -w)))
                echo "$deleted_count row(s) deleted, $(($total - $deleted_count)) row(s) left"
            fi

            end_time=$(date +%s)
            time_taken=$(($end_time - $start_time))
            printf "Deletion from $table table complete in %02d hour(s),%02d minute(s),%02d seconds(s).\n" $(($time_taken/3600)) $(($time_taken%3600/60)) $(($time_taken%60))
        fi
    else
        count=$(psql -d $database -t -c "SELECT COUNT(*) FROM $table")
        if [ $count -eq 0 ]; then
            echo "Table $table is empty. Skipping deletion."
        else
            psql -d $database -t -q -c "DELETE FROM $table"
            echo "Deleting all records from $table table..."
        fi
    fi
done

echo "Script complete."
