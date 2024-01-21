expr = {
    "<start>": ["<start_expr>"],
    "<start_expr>": ["<literal_value>", 
                   #"<bind_parameter>",
                   "<schema_name_dot><table_name_dot><column_name>",
                   "<unary_operator> <expr>",
                   "<expr> <binary_operator> <expr>",
                   "<function_name> ( <function_arguments> ) <filter_clause> ",
                   "( <m_expr> )",
                   "CAST ( <start_expr AS <type_name> )",
                   "<start_expr> COLLATE <collation_name>",
                   "<start_expr> <NOT> LIKE <start_expr> <escape_expr>",
                   "<start_expr> <NOT> <glob_regex_match> <start_expr>",
                   "<start_expr> <null_options>",
                   "<start_expr> IS <NOT> <DISTINCT_FROM> <start_expr>",
                   "<start_expr> <NOT> BETWEEN <start_expr> AND <start_expr>",
                   "<start_expr> <NOT> IN <options_1>",
                   #f"<NOT> <EXISTS> (<{select_stmt}>)",
                   "CASE <start_expr> <m_when_then> <if_else_expr> END",
                   "<raise_function>"],
    "<literal_value>": ["<numeric_literal>", "string_literal", "NULL", "TRUE", "FALSE", 
                        "CURRENT_TIME", "CURRENT_DATE", "CURRENT_TIMESTAMP"],
    #"<bind_parameter>": [],
    "<schema_name_dot>": ["", "<string>."],
    "<table_name_dot>": ["", "<string>."],
    "<column_name>": ["<string>"],
    "<unary_operator>": ["+", "-", "NOT",],
    "<binary_operator>": ["+", "-", "*", "/", "%",
                          "=", "<", ">", "!=", ">=", "<=", 
                          "AND", "OR", 
                          "||",
                          "&", "|", "<<", ">>", "^"],
    "<function_name>": ["<string>"],
    "<function_arguments>": ["", "<DISTINCT> <m_expr> <order_by_clause>", "*"],
    "<m_expr>": ["<start_expr>", "<start_expr>, <m_expr>",],
    "<order_by_clause>": ["", "ORDER BY <m_ordering_term>"],
    "<m_ordering_term>": ["<ordering_term>", "<ordering_term>, <m_ordering_term>"],
    "ordering_term": ["<expr> <collate> <asc_desc> <nulls_first_last>"],
    "<collate>":["", "COLLATE <collation_name>"],
    "<collation_name>": ["<string>"],
    "<asc_desc>": ["", "ASC", "DESC"],
    "nulls_first_last": ["", "NULLS FIRST", "NULLS LAST"],
    "<filter_clause>": ["", "FILTER ( WHERE <start_expr> )"],
    #"<over_clause>": ["", ],
    "<type_name>": ["<m_name> <if_signed_number>"],    
    "<m_name>": ["<name>", "<name> <m_name>"],
    "<name>": ["<string>"],
    "<if_signed_number>": ["", "( <signed_number> )", "( <signed_number>, <signed_number>)"],
    "<signed_number>": ["<numeric_literal>", "+<numeric_literal>", "-<numeric_literal>"],
    "<NOT>": ["", "NOT"],
    "<escape_expr>": ["", "ESCAPE <start_expr>"],
    "<glob_regex_match>": ["GLOB", "REGEXP", "MATCH"],
    "<null_options>": ["ISNULL", "NOTNULL", "NOT NULL"],
    "<DISTINCT_FROM>": ["", "DISTINCT FROM"],
    "<options_1>": [
                    #"()", f"(<{select_stmt}>)", "(<m_expr>)",
                    "<schema_name_dot><table_name>",
                    "<schema_name_dot><table_function_name> ()",
                    "<schema_name_dot><table_function_name> (<m_expr>)"],
    "<table_name>": ["<string>"],
    "<EXISTS>": ["", "<EXISTS>"],
    "<m_when_then>": ["WHEN <start_expr> THEN <start_expr>", "WHEN <start_expr> THEN <start_expr> <m_when_then>"],
    "<if_else_expr>": ["", "ELSE <start_expr>"],
    "<raise_function>": ["RAISE (<raise_options>)"],
    "<raise_options>": ["IGNORE", "ROLLBACK, <error_message>", "ABORT, <error_message>", "FAIL, <error_message>"],
    "<error_message>": ["<string>"],
    "<numeric_literal>": ["<digits>"],
    "<digits>": ["<digit>","<digit><digits>"],
    "<digit>": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
    "<string>": ["<letter>", "<letter><string>"],
    "<letter>": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", 
                 "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
                 "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", 
                 "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"],
}

"""
EXPR:
-- not implemented: blob-literal, 
                    over-clause in function-name
"""

create_table_stmt = {
    "<create_table>": ["CREATE <temp> <temporary> TABLE <if_not_exists> <schema_name_dot><table_name> \
        (<m_column_definiton> <m_table_constraint>)"],
    "<temp>": ["", "TEMP"],
    "<temporary>": ["", "TEMPORARY"],
    "<if_not_exists>":["", "IF NOT EXISTS"],
    "<schema_name_dot>": ["", "<string>."],
    "<table_name>": ["<string>"],
    "<m_column_definiton>":["<column_definiton>", "<m_column_definiton>,<column_definiton>"],
    "<column_definiton>": ["<string> <data_type>"],
    "<m_table_constraint>": ["", ", <table_constraint>" , "<table_constraint> <m_table_constraint>"],
    "<table_constraint>": ["<constraint_name> PRIMARY KEY ( <m_indexed_column> ) <conflict_clause>",
                           "<constraint_name> UNIQUE ( <m_indexed_column> ) <conflict_clause>",
                           "<constraint_name> CHECK (<expr>)",
                           "<constraint_name> FOREIGN KEY ( <m_column_name> ) <foreign_key_clause>"],
    "<constraint_name>": ["", "CONSTRAINT <name>"],
    "<name>": ["<string>"],
    "<m_indexed_column>": ["<indexed_column>", "<indexed_column>, <m_indexed_column>"],
    "<indexed_column>": ["<column_name> <collate> <asc_desc>",
                         "<expr> <collate> <asc_desc>"],
    "<collate>": ["", "COLLATE <collation_name>"],
    "<collation_name>": ["<string>"],
    "<asc_desc>": ["", "ASC", "DESC"],
    "<conflict_clause>": ["", "ON CONFLICT <conflict_options>"],
    "<conflict_options>": ["ROLLBACK", "ABORT", "FAIL", "IGNORE", "REPLACE"],
    "<expr>": expr,
    "<m_column_name>": ["<column_name>", "<column_name>, <m_column_name>"],
    "<column_name>": ["<string>"],
    "<foreign_key_clause>": ["REFERENCES <foreign_table> <m_foreign_column_name> <m_foreign_options> <deferable>"],
    "<foreign_table>": ["<string>"],
    "<m_foreign_column_name>": ["", "( <m_column_name> )"],
    "<m_foreign_options>": ["", "ON <delete_or_update> <foreign_options> <m_foreign_options>", "MATCH <name> <m_foreign_options>"],
    "<delete_or_update>": ["DELETE", "UPDATE"],
    "<foreign_options>": ["SET NULL", "SET DEFAULT", "CASCADE", "RESTRICT", "NO ACTION"],
    "<deferable>": ["", " <NOT> DEFERABLE <deferable_options>"],
    "<NOT>": ["", "NOT"],
    "<deferable_options>": ["", "INITIALLY DEFERRED", "INITIALLY IMMEDIATE"],
    "<data_type>": ["TEXT", "INTEGER", "REAL", "BLOB", "NULL"],
    "<string>": ["<letter>", "<letter><string>"],
    "<letter>": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", 
                 "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
                 "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", 
                 "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"],
}

"""
IN CREATE TABLE STATEMENT:
-- not implemented:  AS [select-stmt], table-options

"""


select_stmt = {
    "<start>": ["<select_query>"],
    "<select_query>": ["<select_core>", "<select_core> <compound_operator> <select_query>"],
    "<select_core>": ["SELECT <DISTINCT_or_ALL> <m_result_column> <from_clause> <where_clause> \
        <group_by_clause> <order_by_clause> <limit_clause>"],
    "<DISTINCT_or_ALL>": ["", "DISTINCT", "ALL"],
    "<m_result_column>": ["<result_column>", "<result_column>, <m_result_column>"],
    "<result_column>": ["<expr>", "<expr> <as> <column_alias>", "*", "<table_name>.*"],
    "<from_clause>": ["","FROM <m_table_or_subquery>", "FROM <join_clause>"],
    "<m_table_or_subquery>": ["<table_or_subquery>", "<table_or_subquery>, <m_table_or_subquery>"],
    "<table_or_subquery>": ["<schema_name_dot><table_name> <as> <table_alias> <indexed>", 
                            "<schema_name_dot><table_function_name> ( <m_expr> ) <as> <table_alias>",
                            #f"( <{select_stmt}> ) <as> <table_alias>",
                            "( <m_table_or_subquery> )",
                            "( <join_clause> )"],
    "<schema_name_dot>": ["","<schema_name>."],
    "<as>": ["", "AS"],
    "<table_alias>":["", "<string>"],
    "<indexed>": ["", "INDEXED BY <index_name>", "NOT INDEXED"],
    "<join_clause>":["<table_or_subquery>", "<table_or_subquery> <m_joins>"],
    "<m_joins>": ["<join_operator> <table_or_subquery> <join_constraint>", 
                  "<join_operator> <table_or_subquery> <join_constraint> <m_joins>"],
    "<join_operator>": [",", "JOIN", "<natural_join>", "CROSS JOIN"],
    "<natural_join>": ["NATURAL JOIN", "NATURAL LEFT JOIN", "NATURAL RIGHT JOIN",
        "NATURAL FULL JOIN", "NATURAL INNER JOIN", "NATURAL LEFT OUTER JOIN", 
        "NATURAL RIGHT OUTER JOIN", "NATURAL FULL INNER JOIN"],
    "<join_constraint>": [" ","ON <expr>", "USING ( <column_names> )"],
    "<column_names>": ["<column_name>", "<column_name>, <column_names>"],
    "<column_name>": ["<string>"],
    "<where_clause>": ["", "WHERE <expr>" ,"WHERE <expr> <having_expr>"],
    "<group_by_clause>": ["","GROUP BY <m_expr>", "GROUP BY <m_expr> <having_expr>"],
    "<m_expr>": ["<expr>", "<expr>, <m_expr>"],
    "<having_expr>": ["HAVING <expr>"],
    #"<value_expr>": ["", "VALUES <values>"],
    #"<values>": ["( <m_expr> )", " ( <m_expr> ), <values>"],
    "<order_by_clause>": ["", "ORDER BY <m_ordering_term>"],
    "<m_ordering_term>": ["<ordering_term>", "<ordering_term>, <m_ordering_term>"],
    "ordering_term": ["<expr> <collate> <asc_desc> <nulls_first_last>"],
    "<collate>":["", "COLLATE <collation_name>"],
    "<asc_desc>": ["", "ASC", "DESC"],
    "nulls_first_last": ["", "NULLS FIRST", "NULLS LAST"],
    "<limit_clause>": ["", "LIMIT <expr>", "LIMIT <expr> OFFSET <expr>", "LIMIT <expr> , <expr>"],
    "<compound_operator>": ["UNION", "UNION ALL", "INTERSECT", "EXCEPT"],
    "<schema_name>": ["<string>"],
    "<column_alias>": ["<string>"],
    "<table_name>": ["<string>"],
    "<table_function_name>": ["<string>"],
    "<index_name>": ["<string>"],
    "<collation_name>": ["<string>"],
    "<expr>":expr,
    "<string>": ["<letter>", "<letter><string>"],
    "<letter>": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", 
                 "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
                 "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", 
                 "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"],
}

"""
SELECT STMT:
Not Implemented: with recursive common-table-expression, values, window-name, window-defn


Select Statement Non-Terminals List:
select_core
select_query
1. distinct_keyword     DONE
2. all_keyword          DONE
result_columns          DONE
3. result_column        DONE
4. table_or_subquery    DONE
5. join_clause          DONE
6. where_clause         DONE
7. group_by_clause      DONE
8. value_expr           DONE
9. values               DONE  
10. order_by_clause     DONE
11. limit_clause        DONE
12. expr
13. column_alias        DONE
14. table_name          DONE
15. m_joins             DONE
16. join_operator       DONE
17. join_constraint     DONE
18. natural_join        DONE
19. column_names        DONE
20. column_name         DONE
21. string              DONE
22. ordering_term       DONE
23. m_expr              DONE
24. having_expr         DONE
25. compound_operator   DONE
26. m_ordering_term     DONE
27. collate             DONE
28. asc_desc            DONE
29. nulls_first_last    DONE
30. as                  DONE
31. table_alias         DONE
32. indexed             DONE
33. index_name          DONE
34. table_function_name DONE
35. letter              DONE
36.
37.
38.
39.
40.
41.
42.
43.
44.
45.
46.
47.
48.
49.
50.
51.

"""

alter_table_grammar = {
    
    "<start>": ["<alter_table>"],
    "<alter_table>": ["ALTER TABLE <old_table_name> <alteration_cause>"],
    "<alteration_cause>": ["ADD COLUMN <m_column_definition>", "DROP COLUMN <column_name>", 
                           "RENAME TO <new_table_name>", "RENAME COLUMN <old_column_name> TO <new_column_name>"], 
    "<m_column_defintion>": ["<column_defintion>", "<m_column_defintion>, <column_defintion>"],
    "<column_defintion>": ["<string> <data_type>"],
    "<column_name>": ["<string>"],
    "<new_table_name>": ["<string>"],
    "<old_column_name>": ["<string>"],
    "<new_column_name>": ["<string>"],
    "<string>": ["letter", "<letter><string>"],
    "<data_type>": ["TEXT", "INTEGER", "REAL", "BLOB", "NULL"],
    "<letter>": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", 
                 "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
                 "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", 
                 "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"],
    
}

delete_table_grammar = {
    "<start>": ["<delete_table>"],
    "<delete_table>": ["DELETE FROM <old_table_name>", "DELETE FROM <old_table_name> <where_clause>"],
    "<where_clause>": ["", "WHERE <expr>"],
    "<expr>": []
}



