import csv

class Memory:
    def __init__(self) -> None:
        self.index = {} # hold the index in main memory as a hash table. Could be a b-tree, bitmap, or anything else.

    # load the index file into the hash map self.index
    # this function assumes each line in the index is it's own key-value pair. like
    # index.csv:
    # record1, index1
    # record2, index2
    # record3, index3
    def load_index(self, file):
        self.index = {} # make sure index is flushed before loading another index file
        with open(file, 'r', newline="\n") as index:
            csv_reader = csv.reader(index)
            for record in csv_reader:
                self.index[record[0]] = record[1]
    
    def write_index(self, key, value):
        self.index[key] = value

class DatabaseEngine:
    def __init__(self) -> None:
        self.memory = Memory()
        self.table_metadata = {}

    # schema is a dictionary where the key is the name of the column, and the
    #value is the maximum size of each entry in the column.
    def create_table(self, table_name: str, schema: dict, key: str) -> None:
        self.table_metadata[table_name] = {
            "schema": schema,
            "max_record": sum(schema.values()),
            "key": key,
            "size": 0
        }
        # format the schema for the index file
        schema_line = ""
        for attribute in schema:
            schema_line += attribute + ","
        schema_line = schema_line[:-1] + "\n" # get rid of last comma
        # write the schema to the index file
        with open(table_name + "_index" + ".bin", 'w') as file:
            file.write(schema_line)

        # write the schema to the data file
        with open(table_name + "_data" + ".bin", 'wb') as file:
            # format the schema for the data file
            schema_line = b''
            for attribute in schema:
                padding = schema[attribute] - len(attribute) # padding = MAX size - size used
                schema_line += attribute.encode("utf-8")
                schema_line += padding * b"\x00"
            file.write(schema_line)
            print(schema_line)
        print("created table with the folowing properties:")
        print("max record size: ", self.table_metadata[table_name]['max_record'])
        print("schema: ", self.table_metadata[table_name]['schema'])
        print("key: ", self.table_metadata[table_name]['key'])

    def write(self, table: str, record: dict):
        # write the schema to the data file
        with open(table + "_data" + ".bin", 'wb') as file:
            # format the schema for the data file
            schema_line = b''
            for attribute in record:
                padding = self.table_metadata[table]["schema"][attribute] - len(record[attribute])
                schema_line += record[attribute].encode("utf-8")
                schema_line += padding * b"\x00"
            file.write(schema_line)
            print(schema_line)
            print(len(schema_line))
        
        key = self.table_metadata[table]["key"]
        self.memory.write_index(record[key], self.table_metadata[table]["size"]+1)
        self.table_metadata[table]["size"] += 1
    
    def read(self, table, key):
        index = self.memory.index[key] - 1
        offset = index * self.table_metadata[table]["max_record"]

        with open(table + "_data.bin", 'rb') as file:
            file.seek(offset)
            data = file.read(self.table_metadata[table]["max_record"])
        print(data)
        print(len(data))

if __name__ == "__main__":
    mem = Memory()
    mem.load_index("index.csv")
    print(mem.index)

    db = DatabaseEngine()
    db.create_table("players", {"name": 32, "team": 32, "position": 32}, key="name")
    db.write("players", {"name": "Tom Brady", "team": "New England Patriots", "position": "Quarterback"})
    db.read("players", "Tom Brady")

    

    