CREATE TABLE "table_name" ("col1" TEXT,"col2" TEXT);



/* --------------------------------------- DELETE QUERIES --------------------------------------------- */

/*Deletes all records from a table, but keeps the table structure*/
DELETE FROM "table_name";

/*Delete records using multiple conditions:*/
DELETE FROM "table_name" WHERE "col1" = "value" AND "col2" = "value2" OR "col3" = "value3";


/* ------------------------------------------ DROP TABLE -- QUERIES --------------------------------------- */

/*Drop a single table:*/
DROP TABLE "table_name";

/*Drop a table only if it exists*/
DROP TABLE IF EXISTS "table_name";

/* Drop multiple tables */
DROP TABLE "table_1", "table_2", "table_3"; 


/* ------------------------------------- INSERT INTO TABLE -- QUERIES ------------------------------- */

/* Insert a single record with values */
INSERT INTO "table_name" ("column1", "column2") VALUES ("value1", 'value2');

/* Insert multiple records in a single query: */
INSERT INTO "table_name" ("column1", "column2") VALUES ("value1a", 'value2a'), ("value1b", 'value2b'),("value1c", 'value2c');


/* ------------------------------------- SELECT FROM TABLE -- QUERIES ------------------------------- */

/*Select all columns from a table:*/
SELECT * FROM "table_name";

/*Select specific columns from a table:*/
SELECT "column1", "column2" FROM "my_table";

/*Select distinct values from a column:*/
SELECT DISTINCT "column1" FROM "my_table";

/*Filter rows based on a condition:*/
SELECT * FROM "my_table" WHERE "column1" > "value";

/*Order the result set:*/
SELECT * FROM "my_table" ORDER BY "column1" DESC;

/*Limit the number of rows returned:*/
/*SELECT * FROM "my_table" LIMIT "INT_VALUE";*/

/* Join two tables: */
SELECT * FROM "table1" INNER JOIN "table2" ON "table1.id" = "table2.id";

/* Aggregate functions (e.g., SUM, AVG, COUNT): */
SELECT AVG("column1"), COUNT(*) FROM "my_table" WHERE "column2" = 'value';

/* Grouping and HAVING clause */
SELECT "column1", COUNT(*) FROM "my_table" GROUP BY "column1" HAVING COUNT(*) > "Value";

/* Subqueries: */
/*SELECT "column1" FROM "my_table" WHERE "column2" IN (SELECT "column2" FROM "other_table" WHERE "condition");*/



/* ------------------------------------- UPDATE TABLE -- QUERIES ------------------------------- */

/* Update a single column for all records: */
UPDATE "my_table" SET "column1" = "new_value";

/* Update multiple columns for a specific record: */
/*UPDATE "my_table" SET "column1" = "new_value1", "column2" = "new_value2" WHERE "non_boolean_condition";*/

/**/

/**/

/**/

/**/

/**/

/**/

/**/

/**/

/**/

