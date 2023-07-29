# File I/O in Python

There's no way of getting around dealing with files in databases, unless you're creating an in-memory only database.

## Secondary Storage is on Disk

That means files. like `file.txt`. Each file itself usually represents a single relation/table. Like if you run 

`CREATE TABLE table_name(...);`

You'll get a table, but that "table" isn't actually a table in the DBMS, it's a file.

## Every table/relation has two files (maybe three)

```
index.txt
data.txt
```

Tables and relations are the same thing - a file. 

Three actually. One is for the actual data, one is for the indexes, and one is for the schema, (but I suppose to you can make the first line in the index file the table schema if you want.)

For InnoDB, the engine that runs MySQL:
```
table_index.ibd
table_data.ibd
```
For MyISAM, the old engine for MySQL:
```
table.MYI # index file
table.MYD # data file
```

## Index files

You want this whole thing to fit in main memory for speed purposes. You check the index file for a record, and then the index file will tell you where the record is in the datafile, and then jump to that spot in the data file and grab JUST THAT RECORD. 

Need a record?

1. Search the index file for the record key.

2. Get the index associated with the record key. 

3. Grab the data from the data file at that index. 
