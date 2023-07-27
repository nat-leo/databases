import os # FileManager.delete_table
import csv # FileManager.insert

class FileManager:
    def __init__(self) -> None:
        self.tables = {}

    # create a relation/table, which creates a file table_name.txt to working 
    #dir. The key is the index of one of the elements in the schema.
    def create_table(self, table_name: str, schema: list[str], key: int):
        # convert the schema from a list of attributes to string representing
        #a Comma Separated Value (csv)
        schema_line = ""
        for attribute in schema:
            schema_line += attribute + ","
        schema_line = schema_line[:-1] + "\n" # get rid of last comma
         
        with open(table_name + ".csv", 'w') as file:
            file.write(schema_line)

        # add the table_name to the list of tables in order to keep track of the
        #tables we've created so far and their keys.
        self.tables[table_name] = key

    # delete a relation/table, which deletes a file table_name.txt from working
    #dir.
    def delete_table(self,table_name: str):
        try:
            os.remove(table_name+".csv")
        except FileNotFoundError:
            print("Table does not exist.")
        except Exception as e:
            print(f"An error occurred while deleting table: {e}")
    
    # add a record to the table by loading entire table, inserting
    #record, sorting table, and loading it back into secondary storage.
    def insert(self, record: list[str], table: str):
        # read all the data
        csv_data = []
        with open(table+".csv", newline="\n") as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                csv_data.append(row)
        # append the newest record and sort the data
        csv_data.append(record)
        sorted_csv_data = sorted(csv_data, key=lambda x: 1)
        print(sorted_csv_data)

        # return new data to secondary storage
        with open(table+".csv", "w") as file:
            for row in sorted_csv_data:
                # convert list to string for storage in .csv
                record = ""
                for element in row:
                    record += element+","
                # write record to .csv file
                record = record[:-1]+"\n" # don't include final comma
                file.write(record)             

def main():
    file = FileManager()
    file.create_table("animals", ["genus", "species"], 1)
    file.insert(["canis", "canis"], "animals")
    file.insert(["uniops", "americanus"], "animals")
    file.insert(["tricauda", "arena"], "animals")
    file.insert(["archaeodelphi", "caeruleus"], "animals")
    file.insert(["bisuchus", "leucoceros"], "animals")
    file.insert(["curviped", "ceti"], "animals")
    file.insert(["pentaceros", "cirrirostrum"], "animals")

    file.delete_table("animals")

if __name__ == "__main__":
    main()