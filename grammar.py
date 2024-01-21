# Implement your grammar here in the `grammar` variable.
# You may define additional functions, e.g. for generators.
# You may not import any other modules written by yourself.
# That is, your entire implementation must be in `grammar.py`
# and `fuzzer.py`.
from fuzzingbook.GeneratorGrammarFuzzer import opts
import random

table_data = {}
index_data = set()
view_data = set()
schema_data = set()

class Database:
    def __init__(self):
        self.current_table_name = ""
        self.current_foreign_table_name = ""
        self.current_column_name = ""
        self.alter_old_table_name = ""
        self.alter_new_table_name = ""
        self.alter_old_column_name = ""
        self.alter_new_column_name = ""
        self.current_index_name = ""
        self.column_names = []
        self.selected_table_name = []
        self.update_table_name = []
        self.selected_other_table_name = ""
        self.update_other_table_name = ""
        
        
    # CREATE TABLE table_name  ##############################################################################        
    def store_table_name(self, table_name):
        self.current_table_name = table_name
        
        if self.current_table_name not in table_data:
            #New table state is initialized here
            table_data[table_name] = {}
            table_data[table_name].__setitem__("pk", True)
            table_data[table_name].__setitem__("columns", ['col1'])
            return self.current_table_name
        return None
    
    def store_column_name(self, column_name):
        self.current_column_name = column_name        
        if self.current_table_name and self.current_column_name not in table_data[self.current_table_name]["columns"]:
            table_data[self.current_table_name]["columns"].append(column_name)
            return self.current_column_name
        else:
            return None
    
    def get_indexed_column_name(self, index_column_name):
        if index_column_name not in table_data[self.current_table_name]["columns"]:
            return random.choice(table_data[self.current_table_name]["columns"])     
        else:
            # print("INDEX column Error")
            return None   
        
    ### not used ###
    def get_random_own_column_name(self, own_column_name):
        if own_column_name not in table_data[self.current_table_name]["columns"]:
            return random.choice(table_data[self.current_table_name]["columns"])
        else:
            # print("OWN column Error")
            return None
    ### not used ###
    def get_foreign_table_name(self, foreign_table_name):
        foreign_tables = list(table_data.keys())
        if len(foreign_tables) > 2:
            foreign_tables = foreign_tables.remove(self.current_table_name)
            if foreign_table_name not in foreign_tables:
                self.current_foreign_table_name = random.choice(foreign_tables)
                return self.current_foreign_table_name
        else:
            # print("Foreign Table Error")
            return None
    ### not used ###
    def get_foreign_column_name(self, foreign_column_name):
        if foreign_column_name not in table_data[self.current_foreign_table_name]["columns"]:
            return random.choice(table_data[self.current_foreign_table_name]["columns"])
        else:
            # print("Foreign column Error")
            return None
    
    # DROP TABLE table_name ############################################################################
    def get_drop_table_name(self, drop_table_name):
        drop_count = 0
        current_tables = list(table_data.keys())
        
        if drop_count <= 5 and drop_table_name not in current_tables:
            removed_table = table_data.pop(random.choice(current_tables))
            drop_count += 1
            return removed_table
        
        elif drop_count > 5 and drop_table_name in current_tables:
            removed_table = table_data.pop(drop_table_name)
            drop_count += 1
            return removed_table
        
        else:
            # print("Drop Table: No such table present")
            return None
        
    ### Attach and Detach Schemas, Analyze: #############################################################
    def attach_database(self, schema_name):
        if schema_name not in schema_data:
            schema_data.add(schema_name)
            return schema_name
        return None
    
    def detach_database(self, schema_name):
        if schema_data and schema_name in schema_data:
            schema_data.remove(schema_name)
            return schema_name
        else:
            # print("Detach DB: No such db present")
            return None
    
    def get_schema_name(self, schema_name):
        if schema_name in schema_data:
            return schema_name
        elif schema_data and schema_name not in schema_data:
            return random.choice(list(schema_data))
        else:
            return None
        
    def get_index_or_table(self, index_or_table):
        if index_or_table in index_data or index_or_table in list(table_data.keys()):
            return index_or_table
        elif index_or_table not in index_data or index_or_table not in list(table_data.keys()):
            list_index_table = []
            list_index_table.extend(index_data)
            list_index_table.extend(list(table_data.keys()))
            return random.choice(list_index_table)
        else:
            return None
        
        
    # Select Statements ######################################################################################
    def get_selected_table_name(self, select_table_name):
        if select_table_name not in list(table_data.keys()):
            self.current_table_name = random.choice(list(table_data.keys()))
            self.selected_table_name.append(self.current_table_name)
            return self.current_table_name
        return None
    
    def get_selected_index_name(self, select_index_name):
        if self.current_table_name:
            available_columns = table_data[self.current_table_name]["columns"]
        
        if self.current_table_name and available_columns and select_index_name not in available_columns:
            return random.choice(table_data[self.current_table_name]["columns"])
        return None
    
    def get_selected_other_table_name(self, select_other_table_name):
        all_tables = list(table_data.keys())
        selected_tables = self.selected_table_name
        available_tables = [table for table in all_tables if table not in selected_tables]
        
        if select_other_table_name not in available_tables:
            self.selected_other_table_name = random.choice(available_tables)
            self.selected_table_name.append(self.selected_other_table_name)
            return self.selected_other_table_name
        return None
    
    # INSERT Statement #######################################################################################
    
    def get_insert_table_name(self, insert_table_name):
        if insert_table_name not in list(table_data.keys()):
            self.current_table_name = random.choice(list(table_data.keys()))
            return self.current_table_name 
        return None
    
    def get_insert_column_name(self, insert_column_name):
        if self.current_table_name:
            available_columns = table_data[self.current_table_name]["columns"]
        
        if self.current_table_name and available_columns and insert_column_name not in available_columns:
            return random.choice(table_data[self.current_table_name]["columns"])
        return None
    
    # Update Statement #######################################################################################
    
    def get_update_table_name(self, update_table_name):
        if update_table_name not in list(table_data.keys()):
            self.current_table_name = random.choice(list(table_data.keys()))
            self.update_table_name.append(self.current_table_name)
            return self.current_table_name
        return None
    
    def get_update_column_name(self, update_column_name):
        if self.current_table_name:
            available_columns = table_data[self.current_table_name]["columns"]
            
        if self.current_table_name and available_columns and update_column_name not in available_columns:
            return random.choice(table_data[self.current_table_name]["columns"])
        return None
    
    def get_update_other_table_name(self, update_other_table_name):
        all_tables = list(table_data.keys())
        update_tables = self.selected_table_name
        available_tables = [table for table in all_tables if table not in update_tables]
        
        if available_tables and update_other_table_name not in available_tables:
            self.update_other_table_name = random.choice(available_tables)
            self.update_table_name.append(self.update_other_table_name)
            return self.selected_other_table_name
        return None
    
    def get_update_other_column_name(self, update_other_column_name):
        if self.update_other_table_name:
            available_columns = table_data[self.update_other_table_name]["columns"]
        
        if self.update_other_table_name and available_columns and update_other_column_name not in available_columns:
            return random.choice(table_data[self.update_other_table_name]["columns"])
        return None
            
    
    # Alter Table Statements #################################################################################    
    def get_alter_old_table_name(self, alter_table_name):
        if alter_table_name in list(table_data.keys()):
            self.alter_old_table_name = alter_table_name
            self.current_table_name = self.alter_old_table_name
            return self.current_table_name
        if alter_table_name not in list(table_data.keys()):
            self.alter_old_table_name = random.choice(list(table_data.keys()))
            self.current_table_name = self.alter_old_table_name
            return self.current_table_name
        else:
            # print("Alter Old Table name error")
            return None
    
    def set_alter_new_table_name(self, alter_table_name):
        if alter_table_name not in list(table_data.keys()) and self.alter_old_table_name:
            self.alter_new_table_name = alter_table_name
            table_data[self.alter_new_table_name] = table_data.pop(self.alter_old_table_name)
            self.current_table_name = self.alter_new_table_name
            return self.alter_new_table_name
        else:
            # print("Alter New Table name error")
            return None
    
    def get_alter_old_column_name(self, alter_column_name):
        if self.current_table_name:
            available_columns = table_data[self.current_table_name]["columns"]
        
        if available_columns and alter_column_name in available_columns:
            self.alter_old_column_name = alter_column_name
            return self.alter_old_column_name
        elif available_columns and alter_column_name not in available_columns:
            self.alter_old_column_name = random.choice(available_columns)
            return self.alter_old_column_name
        else:
            # print("Alter old column name error")
            return None
    
    def set_alter_new_column_name(self, alter_column_name):
        # if self.alter_old_column_name == "":
        #     return None
        
        if self.current_table_name and self.alter_old_column_name and self.alter_old_column_name in table_data[self.current_table_name]["columns"]:
                table_data[self.current_table_name]["columns"].remove(self.alter_old_column_name)
        
        if self.current_table_name and alter_column_name not in table_data[self.current_table_name]["columns"]:
            self.alter_new_column_name = alter_column_name
            table_data[self.current_table_name]["columns"].append(self.alter_new_column_name)
            return self.alter_new_column_name
        else:
            # print("Alter new column name error")
            return None
    
    def alter_add_column(self, alter_column_name):
        if self.current_table_name:
            available_columns = table_data[self.current_table_name]["columns"]
        
        if self.current_table_name and alter_column_name not in available_columns:
            table_data[self.current_table_name]["columns"].append(alter_column_name)
            return alter_column_name
        else:
            # print("Alter ADD column name error")
            return None
    
    def alter_drop_column(self, drop_column_name):
        if self.current_table_name:
            available_columns = table_data[self.current_table_name]["columns"]
        
        if drop_column_name in available_columns:
            table_data[self.current_table_name]["columns"].remove(drop_column_name)
            return drop_column_name
        elif available_columns and drop_column_name not in available_columns:
            drop_col = random.choice(available_columns)
            if drop_col in table_data[self.current_table_name]["columns"]:
                table_data[self.current_table_name]["columns"].remove(drop_col)
                return drop_col
            else:
                return None
    
    # #INDEX: Create, Store, Drop ########################################################################### 
    def store_index_name(self, index_name):
        self.current_index_name = index_name
        current_indexes_list = list(index_data)
        
        if self.current_index_name not in current_indexes_list:
            index_data.add(self.current_index_name)
            return self.current_index_name
        return None
    
    
    def get_drop_index_name(self, drop_index_name):
        current_indexes_list = list(index_data)
        
        if drop_index_name in current_indexes_list:
            removed_index = index_data.remove(drop_index_name)
            return removed_index
        else:
            # print("Drop Index: So such index name present")
            return None
    
    # View Store and Drop View ##############################################################################
    def store_view_name(self, view_name):
        if view_name not in view_data:
            view_data.add(view_name)
            return view_name
        return None
    
    def drop_view_name(self, view_name):
        if view_name in view_data:
            view_data.remove(view_name)
            return view_name
        else:
            # print("Drop View: No such View present")
            return None
    
    def print_state(self):
        print(f"Current Database State:\t {table_data}")
        print(f"Current Index State:\t {index_data}")
        
        
db = Database()




literal_value = {
    "<literal_value>": ["<numeric_literal>", "'<string_literal>'", "NULL", "TRUE", "FALSE", 
                        "CURRENT_TIME", "CURRENT_DATE", "CURRENT_TIMESTAMP"],
}

glob_regex_match = {
    "<glob_regex_match>": ["GLOB", "REGEXP", "MATCH"],
}

null_options = {
    "<null_options>": ["ISNULL", "NOTNULL", "NOT NULL"],
}

raise_options = {
    "<raise_options>": ["IGNORE", "ROLLBACK, <error_message>", 
                        "ABORT, <error_message>", "FAIL, <error_message>"],
}

conflict_options = {
    "<conflict_options>": ["ROLLBACK", "ABORT", "FAIL", "IGNORE", "REPLACE"],
}

foreign_key_options = {
"<foreign_key_options>": ["", "ON DELETE SET NULL", "ON DELETE SET DEFAULT", "ON DELETE CASCADE", "ON DELETE RESTICT",
    "ON DELETE NO ACTION", "ON UPDATE SET NULL", "ON UPDATE SET DEFAULT", "ON UPDATE CASCADE", "ON UPDATE RESTICT",
    "ON UPDATE NO ACTION", "DEFERRABLE", "DEFERRABLE INITIALLY DEFERRED", "DEFERRABLE INITIALLY IMMEDIATE",
    "NOT DEFERRABLE", "NOT DEFERRABLE INITIALLY DEFERRED", "NOT DEFERRABLE INITALLY DEFERRED", "NOT DEFERRABLE INITIALLY IMMEDIATE",],
}

data_type = {
    "<data_type>": ["TEXT", "INTEGER", "REAL", "BLOB", "NULL"],
}

natural_join = {
    "<natural_join>": ["NATURAL JOIN", "NATURAL LEFT JOIN", "NATURAL RIGHT JOIN",
        "NATURAL FULL JOIN", "NATURAL INNER JOIN", "NATURAL LEFT OUTER JOIN", 
        "NATURAL RIGHT OUTER JOIN", "NATURAL FULL INNER JOIN"],
}

nulls_first_last = {
    "<nulls_first_last>": ["", "NULLS FIRST", "NULLS LAST"],
}

asc_desc = {
    "<asc_desc>": ["", "ASC", "DESC"],
}

compound_operator = {
    "<compound_operator>": ["UNION", "UNION ALL", "INTERSECT", "EXCEPT"],
}

unary_operator = {
    "<unary_operator>": ["+", "-", "NOT",],
}

binary_operator = {
    "<binary_operator>": ["+", "-", "*", "/", "%",
                          "=", "<", ">", "!=", ">=", "<=", 
                          "AND", "OR", 
                          "||",
                          "&", "|", "<<", ">>",],
}

digit = {
    "<digit>": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
}

letter = {
    "<letter>": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", 
                 "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
                 "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", 
                 "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"],
}

### BEGIN, COMMIT, ROLLBACK, SAVEPOINT, RELEASE, REINDEX, VACUUM ###################################################

begin_stmt = {
    "<begin_stmt>": ["BEGIN",
                     "BEGIN TRANSACTION",
                     "BEGIN DEFERRED",
                     "BEGIN DEFERRED TRANSACTION",
                     "BEGIN IMMEDIATE",
                     "BEGIN IMMEDIATE TRANSACTION",
                     "BEGIN EXCLUSIVE",
                     "BEGIN EXCLUSIVE TRANSACTION",]
}

commit_stmt = {
    "<commit_stmt>": ["COMMIT", "END",
                      "COMMIT TRANSACTION", "END TRANSACTION"]
}

rollback_stmt = {
    "<rollback_stmt>": ["ROLLBACK", 
                        "ROLLBACK TO <rollback_savepoint_name>",
                        "ROLLBACK TO SAVEPOINT <rollback_savepoint_name>",
                        "ROLLBACK TRANSACTION", 
                        "ROLLBACK TRANSACTION TO <rollback_savepoint_name>",
                        "ROLLBACK TRANSACTION TO SAVEPOINT <rollback_savepoint_name>",],
    "<rollback_savepoint_name>": ["<string>"],
    "<string>": ["<letter>", "<letter><string>"],
    **letter,
    
}

savepoint_stmt = {
    "<savepoint_stmt>": ["SAVEPOINT <savepoint_name>"],
    "<savepoint_name>": ["<string>"],
}

release_stmt = {
    "<release_stmt>": ["RELEASE SAVEPOINT <savepoint_name>",
                       "RELEASE <savepoint_name>"],
}

reindex_stmt = {
    "<reindex_stmt>": ["REINDEX",
                       "REINDEX <reindex_collation_name>",
                       "REINDEX <reindex_table_name>",
                       "REINDEX <reindex_index_name>",
                       "REINDEX <reindex_schema_name>.<reindex_table_name>",
                       "REINDEX <reindex_schema_name>.<reindex_index_name>",
                       ],
    "<reindex_collation_name>": ["<string>"],
    "<reindex_table_name>": ["<string>"],
    "<reindex_index_name>": ["<string>"],
    "<reindex_schema_name>": ["<string>"],
    "<string>": ["<letter>", "<letter><string>"],
    **letter,
}

vacuum_stmt = {
    "<vacuum_stmt>": ["VACUUM",
                      "VACUUM <vacuum_schema_name>",
                      "VACUUM INTO <vacuum_file_name>",
                      "VACUUM <vacuum_schema_name> INTO <vacuum_file_name>"],
    "<vacuum_schema_name>": ["<string>"],
    "<vacuum_file_name>": ["<string>"],
    "<string>": ["<letter>", "<letter><string>"],
    **letter,
}

### PRAGMA STATEMENTS #######################################################################################

pragma_stmt = {
    "<pragma_stmt>": ["PRAGMA <pragma_name>",
                      "PRAGMA <pragma_name> = <pragma_value>",
                      "PRAGMA <pragma_name> (<pragma_value>)",
                      ],
    **digit,
    "<pragma_value>": ["<signed_number>",],
    "<pragma_name>": ["analysis_limit", "application_id", "auto_vacuum", "automatic_index", "busy_timeout" ,
                       "cache_size", "cache_spill", "cell_size_check", "checkpoint_fullfsync", "collation_list",
                       "compile_options", "data_version", "database_list", "defer_foreign_keys", "encoding", 
                       "foreign_key_check", "foreign_key_list", "foreign_keys", "freelist_count", "fullfsync", 
                       "function_list", "hard_heap_limit", "ignore_check_constraints", "incremental_vacuum", 
                       "index_info", "index_list", "index_xinfo", "integrity_check", "journal_mode", 
                       "journal_size_limit", "legacy_alter_table", "legacy_file_format", "locking_mode", 
                       "max_page_count", "mmap_size", "module_list", "optimize", "page_count", "page_size", 
                       "pragma_list", "query_only", "quick_check", "read_uncommitted", "recursive_triggers",
                       "reverse_unordered_selects", "secure_delete", "shrink_memory", "soft_heap_limit", "synchronous",
                       "table_info", "table_list", "table_xinfo", "temp_store", "threads", "trusted_schema", 
                       "user_version", "wal_autocheckpoint", "wal_checkpoint"],
    "<signed_number>": ["<numeric_literal>", "+<numeric_literal>", "-<numeric_literal>"],
    "<numeric_literal>": ["<digits>"],
    "<digits>": ["<digit>","<digit><digits>"],
}

### DATE TIME FUNCTIONS ################################################################################

date_time_functions = {
    "<date_time_functions>": [("SELECT date(<time_value>, <m_date_modifier>)",
                               opts(order = [1, 2])
                               ),
                              ("SELECT time(<time_value>, <m_date_modifier>)",
                               opts(order = [1, 2])
                               ),
                              ("SELECT datetime(<time_value>, <m_date_modifier>)",
                               opts(order = [1, 2])
                               ),
                              ("SELECT julianday(<time_value>, <m_date_modifier>)",
                               opts(order = [1, 2])
                               ),
                              ("SELECT unixepoch(<time_value>, <m_date_modifier>)",
                               opts(order = [1, 2])
                               ),
                              ("SELECT strftime(<m_date_format>, <time_value>, <m_date_modifier>)",
                               opts(order = [1, 2, 3])
                               ),
                              ("SELECT timediff(<c_time_value>, <c_time_value>)",
                               opts(order = [1, 2])
                               )],
    **digit,
    "<time_value>": ["","<year>-<month>-<d_date>",
                     "<year>-<month>-<d_date> <hour>:<minutes>", "<year>-<month>-<d_date> <hour>:<minutes>:<seconds>", 
                     "<year>-<month>-<d_date> <hour>:<minutes>:<seconds>.<seconds><digit>",
                     "<year>-<month>-<d_date>T<hour>:<minutes>", "<year>-<month>-<d_date>T<hour>:<minutes>:<seconds>", 
                     "<year>-<month>-<d_date>T<hour>:<minutes>:<seconds>.<seconds><digit>",
                     "<hour>:<minutes>", "<hour>:<minutes>:<seconds>", "<hour>:<minutes>:<seconds>.<seconds>digit", 
                     "now", "<d_date><d_date><d_date><d_date><d_date>"
                     ],
    "<m_date_modifier>": ["<date_modifier>", "<date_modifier>, <m_date_modifier>"],
    "<date_modifier>": ["+<digit><digit> days", "-<digit><digit> days",
                        "+<digit><digit> hours", "-<digit><digit> hours",
                        "+<digit><digit> minutes", "-<digit><digit> minutes",
                        "+<digit><digit> seconds", "-<digit><digit> seconds",
                        "+<digit><digit> months", "-<digit><digit> months",
                        "+<digit><digit> years", "-<digit><digit> years",
                        "+<hour>:<minutes>", "-<hour>:<minutes>",
                        "+<hour>:<minutes>:<seconds>", "-<hour>:<minutes>:<seconds>",
                        "+<hour>:<minutes>:<seconds>.<seconds><digit>", "-<hour>:<minutes>:<seconds>.<seconds><digit>",
                        "+<year>-<month>-<d_date>", "-<year>-<month>-<d_date>",
                        "+<year>-<month>-<d_date> <hour>:<minutes>", "-<year>-<month>-<d_date> <hour>:<minutes>",
                        "+<year>-<month>-<d_date> <hour>:<minutes>:<seconds>", "-<year>-<month>-<d_date> <hour>:<minutes>:<seconds>",
                        "+<year>-<month>-<d_date> <hour>:<minutes>:<seconds>.<seconds><digit>", "-<year>-<month>-<d_date> <hour>:<minutes>:<seconds>.<seconds><digit>",
                        "start of month", "start of year", "start of day", "weekday <digit>", "unixepoch", "julianday",
                        "auto", "localtime", "utc", "subsec", "subsecond",
                        ],
    "<m_date_format>": ["<date_format>", "<date_format> <m_date_format>"],
    "<date_format>": ["%/d","%/e","%/f","%/F","%H","%I","%j","%J","%k","%l","%m","%M","%p",
                      "%P","%R","%/s","%S","%T","%T","%/u","%w","%W","%Y","%/%/"],
    "<c_time_value>": [ "<year>-<month>-<d_date>",
                        "<year>-<month>-<d_date> <hour>:<minutes>", "<year>-<month>-<d_date> <hour>:<minutes>:<seconds>", 
                        "<year>-<month>-<d_date> <hour>:<minutes>:<seconds>.<seconds><digit>",
                        "<year>-<month>-<d_date>T<hour>:<minutes>", "<year>-<month>-<d_date>T<hour>:<minutes>:<seconds>", 
                        "<year>-<month>-<d_date>T<hour>:<minutes>:<seconds>.<seconds><digit>",
                        "<hour>:<minutes>", "<hour>:<minutes>:<seconds>", "<hour>:<minutes>:<seconds>.<seconds>digit", 
                        "now", "<d_date><d_date><d_date><d_date><d_date>",
                    ],
    "<year>": ["<digit><digit><digit><digit>"],
    "<month>": ["<digit><digit>"],
    "<d_date>": ["<digit><digit>"],
    "<hour>": ["<digit><digit>"],
    "<minutes>": ["<digit><digit>"],
    "<seconds>": ["<digit><digit>"],
}


#### EXPR Grammar ############################################################################################
expr = {
    "<expr>": ["<literal_value>", 
                   "<table_name_dot><column_name>",
                   "<unary_operator> <expr>",
                   "<expr> <binary_operator> <expr>",
                   "<function_name> ( <function_arguments> ) <filter_clause> ",
                   "( <m_expr> )",
                   "CAST ( <expr> AS <type_name> )",
                   "<expr> COLLATE <collation_name>",
                   "<expr> <NOT> LIKE <expr> <escape_expr>",
                   "<expr> <NOT> <glob_regex_match> <expr>",
                   "<expr> <null_options>",
                   "<expr> IS <NOT> <DISTINCT_FROM> <expr>",
                   "<expr> <NOT> BETWEEN <expr> AND <expr>",
                   "<expr> <NOT> IN <options_1>",
                   "CASE <expr> <m_when_then> <if_else_expr> END",
                   "<raise_function>"],
    **asc_desc,
    **nulls_first_last,
    **glob_regex_match,
    **null_options,
    **raise_options,
    **digit,
    **letter,
    **unary_operator,
    **binary_operator,
    **literal_value,
    "<NOT>": ["", "NOT"],
    "<function_arguments>": ["", "<DISTINCT> <m_expr> <order_by_clause>", "*"],
    "<m_expr>": ["<expr>", "<expr>, <m_expr>",],
    "<order_by_clause>": ["", "ORDER BY <m_ordering_term>"],
    "<m_ordering_term>": ["<ordering_term>", "<ordering_term>, <m_ordering_term>"],
    "<ordering_term>": ["<expr> <collate> <asc_desc> <nulls_first_last>"],
    "ordering_term": ["<expr> <collate> <asc_desc> <nulls_first_last>"],
    "<collate>":["", "COLLATE <collation_name>"],
    "<filter_clause>": ["", "FILTER ( WHERE <expr> )"],
    "<type_name>": ["<m_name> <if_signed_number>"],    
    "<m_name>": ["<name>", "<name> <m_name>"],
    "<if_signed_number>": ["", "( <signed_number> )", "( <signed_number>, <signed_number>)"],
    "<signed_number>": ["<numeric_literal>", "+<numeric_literal>", "-<numeric_literal>"],
    "<escape_expr>": ["", "ESCAPE <expr>"],
    "<options_1>": [
                    "<table_name>",
                    "<table_function_name> ()",
                    "<table_function_name> (<m_expr>)"],
    "<m_when_then>": ["WHEN <expr> THEN <expr>", ],
    "<if_else_expr>": ["", "ELSE <expr>"],
    "<raise_function>": ["RAISE (<raise_options>)"],
    "<DISTINCT_FROM>": ["", "DISTINCT FROM"],
    "<DISTINCT>": ["", "DISTINCT"],
    "<EXISTS>": ["", "<EXISTS>"],
    "<collation_name>": ["<string>"],
    "<function_name>": ["<string>"],
    "<table_function_name>": ["<string>"],
    "<string_literal>": ["<string>"],
    "<name>": ["<string>"],
    "<table_name_dot>": ["", "<string>."],
    "<column_name>": ["<string>"],
    "<table_name>": ["<string>"],
    "<error_message>": ["<string>"],
    "<numeric_literal>": ["<digits>"],
    "<digits>": ["<digit>","<digit><digits>"],
    "<string>": ["<letter>", "<letter><string>"],
    
}

### SQL FUNCTIONS ##############################################################################################

simple_function_invocation = {
    "<simple_function_invocation>": ["SELECT <simple_func>()",
                                     "SELECT <simple_func>(*)",
                                     ("SELECT <simple_func>(<m_expr>)",
                                      opts(order = [1, 2])
                                      )],
    **expr,
    "<m_expr>": ["<expr>", "<expr>, <m_expr>",],
    "<simple_func>": ["abs", "changes", "char", "coalesce", "concat", "concat_ws", "format", "glob", "hex", 
                      "ifnull", "iif", "instr", "last_insert_rowid", "length", "like", "like", "likelihood", 
                      "likely", "load_extension", "load_extension", "lower", "ltrim", "ltrim", "max", "min", 
                      "nullif", "octet_length", "printf", "quote", "random", "randomblob", "replace", "round", 
                      "round", "rtrim", "rtrim", "sign", "soundex", "sqlite_compileoption_get", 
                      "sqlite_compileoption_used", "sqlite_offset", "sqlite_source_id", "sqlite_version", 
                      "substr", "substr", "substring", "substring", "total_changes", "trim", "trim", "typeof", 
                      "unhex", "unhex","unicode", "unlikely", "upper", "zeroblob"
        ],
}

### ATTACH, DETACH, ANALYZE ####################################################################################

attach_stmt = {
    "<attach_stmt>": ["ATTACH DATABASE <expr> AS <attach_schema_name>",
                      "ATTACH <expr> AS <attach_schema_name>"],
    **expr,
    "<attach_schema_name>": [("<string>",
                              opts(post= lambda schema_name: db.attach_database(schema_name))
                              )],
}

detach_stmt = {
    "<detach_stmt>": ["DETACH DATABASE <detach_schema_name>",
                      "DETACH <detach_schema_name>"],
    **expr,
    "<detach_schema_name>": [("<string>",
                              opts(post= lambda schema_name: db.detach_database(schema_name))
                              )],
}

analyze_stmt = {
    "<analyze_stmt>": ["ANALYZE",
                       "ANALYZE <analyze_schema_name>",
                       "ANALYZE <analyze_index_table>",
                       "ANALYZE <analyze_schema_name>.<analyze_index_table>"],
    "<analyze_schema_name>": [("<string>",
                               opts(post = lambda schema_name: db.get_schema_name(schema_name))
                               )],
    "<analyze_index_table>": [("<string>",
                               opts(post = lambda index_or_table: db.get_index_or_table(index_or_table))
                               )],
    "<string>": ["<letter>", "<letter><string>"],
    **letter,
}

### SELECT STATEMENT ####################################################################################

select_stmt = {
    "<select_stmt>": [("<select_core> <order_or_limit>",
                       opts(order = [1, 2])
                       ), 
                      ("<select_core> <compound_operator> <select_stmt>",
                       opts(order = [1, 2, 3])
                       )],
    "<select_core>": [("SELECT <m_result_column> <from_clause> <where_clause> <group_by_clause>",
                       opts(order = [1, 2, 3, 4])
                       ),
                      ("SELECT DISTINCT <m_result_column> <from_clause> <where_clause> <group_by_clause>",
                       opts(order = [1, 2, 3, 4])
                       ),
                      ("SELECT ALL <m_result_column> <from_clause> <where_clause> <group_by_clause>",
                       opts(order = [1, 2, 3, 4])
                       ),
                      ("SELECT <aggregate_functions>(<select_index_name>) FROM <select_table_name>",
                       opts(order = [1, 2, 3])
                       ),
                      ("SELECT <aggregate_functions>(DISTINCT <select_index_name>) FROM <select_table_name>",
                       opts(order = [1, 2, 3])
                       ),
                      ],
    **natural_join,
    **asc_desc,
    **nulls_first_last,
    **compound_operator,
    **expr,
    **letter,
    "<aggregate_functions>": ["sum", "avg", "count", "min", "max", "total",],
    "<order_or_limit>": ["", "<order_by_clause>", "<order_by_clause> <limit_clause>", "<limit_clause>",],
    "<m_result_column>": ["<result_column>", 
                          ("<result_column>, <m_result_column>",
                           opts(order = [1, 2])
                           )],
    "<result_column>": ["*", 
                        "<select_table_name>.*"],
    "<from_clause>": ["", "FROM <select_table_or_subquery>", "FROM <select_join_clause>"],
    "<select_table_or_subquery>": ["<select_table_name>",
                            ("<select_table_name> <table_alias>",
                             opts(order = [1, 2])
                             ),
                            ("<select_table_name> AS <table_alias>",
                             opts(order = [1, 2])
                             ),
                            "<select_table_name> NOT INDEXED",
                            ("<select_table_name> <table_alias> NOT INDEXED",
                             opts(order = [1, 2])
                             ),
                            ("<select_table_name> AS <table_alias> NOT INDEXED",
                             opts(order = [1, 2])
                             ),
                            "(<select_table_or_subquery>)",
                            "(<select_join_clause>)",
                            ],
    "<select_join_clause>":["<select_table_or_subquery>", 
                     ("<select_table_or_subquery> <join_operator> <select_other_table_or_subquery> <join_constraint>",
                      opts(order = [1, 2, 3, 4])
                      ),
                     ],
    "<join_operator>": [",", "JOIN", "<natural_join>", "CROSS JOIN"],
    "<join_constraint>": ["ON <expr>"],
    "<where_clause>": ["", "WHERE <expr>" ,"WHERE <expr> <having_expr>"],
    "<group_by_clause>": ["","GROUP BY <m_expr>", "GROUP BY <m_expr> <having_expr>"],
    "<m_expr>": ["<expr>", "<expr>, <m_expr>"],
    "<having_expr>": ["HAVING <expr>"],
    "<order_by_clause>": ["ORDER BY <m_ordering_term>"],
    "<m_ordering_term>": ["<ordering_term>", "<ordering_term>, <m_ordering_term>"],
    "<ordering_term>": ["<expr>", "<expr> <collate>", "<expr> <collate> <asc_desc> <nulls_first_last>"],
    "<collate>":["COLLATE <collation_name>"],
    "<limit_clause>": ["LIMIT <expr>", "LIMIT <expr> OFFSET <expr>", "LIMIT <expr> , <expr>"],
    "<table_alias>":["", "<string>"],
    "<column_alias>": ["<string>"],
    "<select_table_name>": [("<string>",
                             opts(post = lambda select_table_name: db.get_selected_table_name(select_table_name))
                             )],
    "<select_table_function_name>": ["<string>"],
    "<select_index_name>": [("<string>",
                             opts(post = lambda select_index_name: db.get_selected_index_name(select_index_name))
                             )],
    "<select_other_table_or_subquery>": [("<string>",
                                          opts(post = lambda select_other_table_name: db.get_selected_other_table_name(select_other_table_name))
                                          )],
    "<collation_name>": ["<string>"],
    "<string>": ["<letter>", "<letter><string>"],
}

### INSERT STATEMENT ##################################################################################

insert_stmt = {
    "<insert_stmt>": [("INSERT <insert_options> INTO <insert_table_name> DEFAULT VALUES",
                       opts(order = [1, 2])
                       ),
                      ("INSERT <insert_options> INTO <insert_table_name> (<m_insert_column_name>) VALUES (<m_expr>)",
                       opts(order = [1, 2, 3, 4])
                       ),
                      ("INSERT <insert_options> INTO <insert_table_name> (<m_insert_column_name>) VALUES <select_stmt>",
                       opts(order = [1, 2, 3, 4])
                       ),
                      ("INSERT <insert_options> INTO <insert_table_name> (<m_insert_column_name>) DEFAULT VALUES",
                       opts(order = [1, 2, 3])
                       ),
                      "REPLACE INTO <insert_table_name> DEFAULT VALUES",
                       #opts(order = [1]),
                      ("REPLACE INTO <insert_table_name> (<m_insert_column_name>) VALUES (<m_expr>)",
                       opts(order = [1, 2, 3])
                       ),
                      ("REPLACE INTO <insert_table_name> (<m_insert_column_name>) VALUES <select_stmt>",
                       opts(order = [1, 2, 3])
                       ),
                      ("REPLACE INTO <insert_table_name> (<m_insert_column_name>) DEFAULT VALUES",
                       opts(order = [1, 2])
                       ),
                      ],
    **select_stmt,
    **expr,
    **letter,
    "<insert_options>": ["", "OR ABORT", "OR FAIL", "OR IGNORE", "OR REPLACE", "OR ROLLBACK"],
    "<m_insert_column_name>": ["<insert_column_name>", "<insert_column_name>, <m_insert_column_name>"],
    "<insert_table_name>": [("<string>",
                            opts(post = lambda insert_table_name: db.get_insert_table_name(insert_table_name))
                            )],
    "<insert_column_name>": [("<string>",
                              opts(post = lambda insert_column_name: db.get_insert_column_name(insert_column_name))
                              )],
    "<m_expr>": ["<expr>", "<expr>, <m_expr>"],
    "<string>": ["<letter>", "<letter><string>"],
}

### CREATE VIEW STATEMENT ##################################################################################

create_view_stmt = {
    "<create_view_stmt>": [("CREATE VIEW <view_name> AS <select_stmt>",
                            opts(order = [1, 2])
                            ),
                           ("CREATE VIEW IF NOT EXISTS <view_name> AS <select_stmt>",
                            opts(order = [1, 2])
                            ),
                           ("CREATE VIEW <view_name> (<m_view_column>) AS <select_stmt>",
                            opts(order = [1, 2, 3])
                            ),
                           ("CREATE VIEW IF NOT EXISTS <view_name> (<m_view_column>) AS <select_stmt>",
                            opts(order = [1, 2, 3])
                            ),
                           ],
    **select_stmt,
    "<view_name>": [("<string>",
                     opts(post = lambda view_name: db.store_view_name(view_name))
                     )],
    "<m_view_column>": ["<view_column>", ("<view_column>, <m_view_column>", 
                                          opts(order = [1, 2])
                                          )
                        ],
    "<view_column>": ["<string>"],
    
}

drop_view_stmt = {
    "<drop_view_stmt>": ["DROP TABLE <view_name>",
                          "DROP TABLE IF EXISTS <view_name>",
                          ],
    **letter,
    "<view_name>": [("<string>",
                     opts(post = lambda view_name: db.drop_view_name(view_name))
                     )],
    "<string>": ["<letter>", "<letter><string>"],
    
}

### WITH CLAUSE ###########################################################################################

with_clause = {
    "<with_clause>": ["WITH <cte_table_name> AS (<select_stmt>)",
                      "WITH RECURSIVE <cte_table_name> AS (<select_stmt>)",
                      "WITH <cte_table_name> AS NOT MATERIALIZED (<select_stmt>)",
                      "WITH RECURSIVE <cte_table_name> AS NOT MATERIALIZED (<select_stmt>)",
                      "WITH <cte_table_name> AS MATERIALIZED (<select_stmt>)",
                      "WITH RECURSIVE <cte_table_name> AS MATERIALIZED (<select_stmt>)"],
    **select_stmt,
    **letter,
    "<cte_table_name>": ["<with_table_name>",
                         "<with_table_name> (<m_with_column_name>)",],
    "<with_table_name>": ["<string>"],
    "<m_with_column_name>": ["<with_column_name>", "<with_column_name>, <m_with_column_name>"],
    "<with_column_name>": ["<string>"],
    "<string>": ["<letter>", "<letter><string>"],
}

### CREATE VIRTUAL TABLE ##########################################################################

create_virtual_table_stmt = {
    "<create_virtual_table_stmt>": [("CREATE VIRTUAL TABLE <virtual_table_name> USING <virtual_module_name>",
                                     opts(order = [1, 2])
                                     ),
                                    ("CREATE VIRTUAL TABLE <virtual_table_name> USING <virtual_module_name> (<m_virtual_module_args>)",
                                     opts(order = [1, 2, 3])
                                     ),
                                    ("CREATE VIRTUAL TABLE IF NOT EXISTS <virtual_table_name> USING <virtual_module_name>",
                                     opts(order = [1, 2])
                                     ),
                                    ("CREATE VIRTUAL TABLE IF NOT EXISTS <virtual_table_name> USING <virtual_module_name> (<m_virtual_module_args>)",
                                     opts(order = [1, 2, 3])
                                     ),
                                    ],
    **literal_value,
    **conflict_options,
    **digit,
    **letter,
    "<m_virtual_module_args>": ["<virtual_module_args>", ("<virtual_module_args>, <m_virtual_module_args>",
                                                          opts(order = [1, 2]) )],
    "<virtual_module_args>": [("<virtual_column_name> <column_type> DEFAULT <default_literal_or_number> <virtual_column_constraint>", 
                            opts(order=[1, 2, 3, 4])
                            )],
    "<column_type>": ["","TEXT", "NUM", "INTEGER", "REAL"],
    "<default_literal_or_number>": ["<literal_value>", "<signed_number>",],
    "<signed_number>": ["<numeric_literal>", "+<numeric_literal>", "-<numeric_literal>"],
    "<virtual_column_constraint>": ["NOT NULL <conflict_clause>",
                              "UNIQUE <conflict_clause>",
                              "COLLATE <collation_name>",],
    "<conflict_clause>": ["", "ON CONFLICT <conflict_options>"],
    "<virtual_table_name>": ["<string>"],
    "<virtual_module_name>": ["<string>"],
    "<virtual_column_name>": ["<string>"],
    "<collation_name>": ["<string>"],
    "<numeric_literal>": ["<digits>"],
    "<digits>": ["<digit>","<digit><digits>"],
    "<string>": ["<letter>", "<letter><string>"],
}

### CREATE INDEX #######################################################################################

create_index_stmt = {
    "<create_index_stmt>": [("CREATE INDEX <index_name> ON <index_table_name> (<m_indexed_columns>)",
                             opts(order = [2, 1, 3])
                             ),
                            ("CREATE INDEX <index_name> ON <index_table_name> (<m_indexed_columns>) WHERE <expr>",
                             opts(order = [2, 1, 3, 4])
                             ),
                            ("CREATE INDEX IF NOT EXISTS <index_name> ON <index_table_name> (<m_indexed_columns>)",
                             opts(order = [2, 1, 3])
                             ),
                            ("CREATE INDEX IF NOT EXISTS <index_name> ON <index_table_name> (<m_indexed_columns>) WHERE <expr>",
                             opts(order = [2, 1, 3, 4])
                             ),
                            ("CREATE UNIQUE INDEX <index_name> ON <index_table_name> (<m_indexed_columns>)",
                             opts(order = [2, 1, 3])
                             ),
                            ("CREATE UNQIE INDEX <index_name> ON <index_table_name> (<m_indexed_columns>) WHERE <expr>",
                             opts(order = [2, 1, 3, 4])
                             ),
                            ("CREATE UNIQUE INDEX IF NOT EXISTS <index_name> ON <index_table_name> (<m_indexed_columns>)",
                             opts(order = [2, 1, 3])
                             ),
                            ("CREATE UNIQUE INDEX IF NOT EXISTS <index_name> ON <index_table_name> (<m_indexed_columns>) WHERE <expr>",
                             opts(order = [2, 1, 3, 4])
                             ),
                            ],
    **expr,
    **letter,
    "<index_name>":[("<string>",
                     opts(post = lambda index_name: db.store_index_name(index_name))
                     )],
    "<m_indexed_columns>": ["<index_column_name>", ("<index_column_name>, <m_indexed_columns>", opts(order = [1, 2]))],
    "<index_table_name>": ["<string>"],
    "<index_column_name>": ["<string>"],
    "<string>": ["<letter>", "<letter><string>"],
}

drop_index_stmt = {
    "<drop_index_stmt>": ["DROP INDEX <drop_index_name>",
                          "DROP INDEX IF EXISTS <drop_index_name>",
                          ],
    **letter,
    "<drop_index_name>": [("<string>", 
                           opts(post = lambda drop_index_name: db.get_drop_index_name(drop_index_name))
                           )],
    "<string>": ["<letter>", "<letter><string>"],
    
}


### CREATE TABLE #####################################################################################

create_table_stmt = {
    "<create_table_stmt>": [("CREATE TABLE <table_table_name> <column_def_table_constraint>",
                            opts(order=[1, 2])
                            ),       
                            ("CREATE TABLE IF NOT EXISTS <table_table_name> <column_def_table_constraint>",
                            opts(order=[1, 2])
                            ),
                         ],
    **conflict_options,
    **expr,
    **literal_value,
    **letter,
    **digit,
    "<column_def_table_constraint>": [("(col1 INTEGER PRIMARY KEY AUTOINCREMENT, <m_column_definiton>, <table_constraint>)",
                                       opts(order=[1, 2])
                                       )],
    "<m_column_definiton>":["<column_definiton>", 
                            ("<column_definiton>, <m_column_definiton>", 
                             opts(order=[1, 2])
                             )],
    "<column_definiton>": [("<table_column_name> <column_type> DEFAULT <default_literal_or_number> <column_constraint>", 
                            opts(order=[1, 2, 3, 4])
                            )],
    "<column_constraint>": ["NOT NULL <conflict_clause>",
                            "UNIQUE <conflict_clause>",
                            "COLLATE <collation_name>",
                            ],
    "<default_literal_or_number>": ["<literal_value>", "<signed_number>",],
    "<signed_number>": ["<numeric_literal>", "+<numeric_literal>", "-<numeric_literal>"],
    "<table_constraint>": [("UNIQUE (<indexed_column>) <conflict_clause>",
                            opts(order=[1, 2])
                            ),
                           "CHECK (<expr>)",],
    "<conflict_clause>": ["", "ON CONFLICT <conflict_options>"],
    "<m_column_name>": ["<column_name>, ", "<column_name><m_column_name>"],
    "<collation_name>": ["BINARY", "RTRIM", "NOCASE"],
    "<column_type>": ["","TEXT", "NUM", "INTEGER", "REAL"],
    "<indexed_column>": [("<string>", 
                          opts(post = lambda index_column_name: db.get_indexed_column_name(index_column_name) ) 
                        )],
    "<table_table_name>": [("<table_name_string>",
                            opts(post = lambda table_name: db.store_table_name(table_name))
                            )],
    "<table_column_name>": [("<string>",
                             opts(post = lambda column_name: db.store_column_name(column_name))
                            )],
    "<table_name_string>": ["<letter><letter><letter><letter>", "<letter><string>"],
    "<string>": ["<letter>", "<letter><string>"],
    "<column_name>": ["<string>"],
    "<string_literal>": ["<string>"],
    "<numeric_literal>": ["<digits>"],
    "<digits>": ["<digit>","<digit><digits>"],
}

drop_table_stmt = {
    "<drop_table_stmt>": ["DROP TABLE <drop_table_name>",
                          "DROP TABLE IF EXISTS <drop_table_name>",
                          ],
    **letter,
    "<drop_table_name>": [("<string>",
                           opts(post = lambda drop_table_name: db.get_drop_table_name(drop_table_name))
                           )],
    "<string>": ["<letter>", "<letter><string>"],
    
}

### ALTER TABLE STATEMENTS #############################################################################

alter_table_stmt = {
    "<alter_table_stmt>": [("ALTER TABLE <alter_old_table_name> RENAME TO <alter_new_table_name>",
                       opts( order=[1, 2] )
                       ),
                      ("ALTER TABLE <alter_old_table_name> RENAME COLUMN <alter_old_column_name> TO <alter_new_column_name>",
                       opts(order = [1, 2, 3])
                       ),
                      ("ALTER TABLE <alter_old_table_name> ADD COLUMN <alter_column_definition>",
                       opts(order = [1, 2])
                       ),
                      ("ALTER TABLE <alter_old_table_name> DROP COLUMN <alter_drop_column_name>",
                       opts(order = [1, 2])
                       ),
                      ],
    **digit,
    **literal_value,
    **conflict_options,
    **letter,
    "<alter_column_definition>": [("<alter_column_name> <column_type> DEFAULT <default_literal_or_number> <column_constraint>", 
                            opts(order=[1, 2, 3, 4])
                            )],
    "<column_constraint>": ["NOT NULL <conflict_clause>",
                            "UNIQUE <conflict_clause>",
                            "COLLATE <collation_name>",
                            ],
    "<default_literal_or_number>": ["<literal_value>", "<signed_number>",],
    "<conflict_clause>": ["", "ON CONFLICT <conflict_options>"],
    "<signed_number>": ["<numeric_literal>", "+<numeric_literal>", "-<numeric_literal>"],
    "<column_type>": ["","TEXT", "NUM", "INTEGER", "REAL"],
    "<alter_drop_column_name>": [("<string>",
                                  opts(post = lambda drop_column_name: db.alter_drop_column(drop_column_name))
                                  )],
    "<alter_new_table_name>": [("<string>",
                                opts(post = lambda alter_table_name: db.set_alter_new_table_name(alter_table_name))
                                )],
    "<alter_old_table_name>": [("<string>",
                                opts(post = lambda alter_table_name: db.get_alter_old_table_name(alter_table_name))
                                )],
    "<alter_old_column_name>": [("<string>",
                                 opts(post = lambda alter_column_name: db.get_alter_old_column_name(alter_column_name))
                                 )],
    "<alter_new_column_name>": [("<string>",
                                 opts(post = lambda alter_column_name: db.set_alter_new_column_name(alter_column_name))
                                 )],
    "<alter_column_name>": [("<string>",
                             opts(post = lambda alter_column_name: db.alter_add_column(alter_column_name))
                             )],
    "<collation_name>": ["<string>"],
    "<numeric_literal>": ["<digits>"],
    "<string>": ["<letter>", "<letter><string>"],
    "<digits>": ["<digit>","<digit><digits>"],
     
}

### DELETE STATEMENT #######################################################################################

delete_stmt = {
    "<delete_stmt>": ["DELETE FROM <delete_qualified_table_name>",
                      ("DELETE FROM <delete_qualified_table_name> WHERE <expr>",
                       opts(order = [1, 2])
                       )],
    **expr,
    **letter,
    "<delete_qualified_table_name>": ["<delete_table_name>",
                               "<delete_table_name> AS <delete_alias>",
                               "<delete_table_name> INDEXED BY <delete_index_name>",
                               "<delete_table_name> AS <update_alias> INDEXED BY <delete_index_name>",
                               "<delete_table_name> NOT INDEXED",
                               "<delete_table_name> AS <update_alias> NOT INDEXED"
                               ],
    "<delete_table_name>": ["<string>"],
    "<delete_alias>": ["<string>"],
    "<delete_index_name>": ["<string>"],
    "<string>": ["<letter>", "<letter><string>"],
    
}

### UPDATE STATEMENT ###################################################################################

update_stmt = {
    "<update_stmt>": [("UPDATE <update_options> <update_qualified_table_name> SET <update_column_name> = <expr>",
                       opts(order = [1, 2, 3, 4])
                       ),
                      ("UPDATE <update_options> <update_qualified_table_name> SET <update_column_name> = <expr> <from_clause>",
                       opts(order = [1, 2, 3, 4, 5])
                       ),
                      ("UPDATE <update_options> <update_qualified_table_name> SET <update_column_name> = <expr> <where_clause>",
                       opts(order = [1, 2, 3, 4, 5])
                       ),
                      ("UPDATE <update_options> <update_qualified_table_name> SET <update_column_name> = <expr> <from_clause> <where_clause>",
                       opts(order = [1, 2, 3, 4, 5, 6])
                       ),
                      ("UPDATE <update_options> <update_qualified_table_name> SET <update_column_list> = <expr>",
                       opts(order = [1, 2, 3, 4])
                       ),
                      ("UPDATE <update_options> <update_qualified_table_name> SET <update_column_list> = <expr> <from_clause>",
                       opts(order = [1, 2, 3, 4, 5])
                       ),
                      ("UPDATE <update_options> <update_qualified_table_name> SET <update_column_list> = <expr> <where_clause>",
                       opts(order = [1, 2, 3, 4, 5])
                       ),
                      ("UPDATE <update_options> <update_qualified_table_name> SET <update_column_list> = <expr> <from_clause> <where_clause>",
                       opts(order = [1, 2, 3, 4, 5, 6])
                       ),
                      ],
    **expr,
    **natural_join,
    "<update_options>": ["", "OR ABORT", "OR FAIL", "OR IGNORE", "OR REPLACE", "OR ROLLBACK"],
    "<update_qualified_table_name>":  ["<update_table_name>",
                               "<update_table_name> AS <update_alias>",
                               "<update_table_name> INDEXED BY <update_index_name>",
                               "<update_table_name> AS <update_alias> INDEXED BY <update_index_name>",
                               "<update_table_name> NOT INDEXED",
                               "<update_table_name> AS <update_alias> NOT INDEXED"],
    "<update_column_list>": ["(<m_update_column_name>)"],
    "<m_update_column_name>": ["<update_column_name>", "<update_column_name>, <m_update_column_name>"],
    "<from_clause>": ["FROM <update_table_or_subquery>", "FROM <update_join_clause>"],
    "<update_table_or_subquery>": ["<update_other_table_name>",
                            ("<update_other_table_name> <update_alias>",
                             opts(order = [1, 2])
                             ),
                            ("<update_other_table_name> AS <update_alias>",
                             opts(order = [1, 2])
                             ),
                            ("<update_other_table_name> INDEXED BY <update_index_name>",
                             opts(order = [1, 2])
                             ),
                            ("<update_other_table_name> <update_alias> INDEXED BY <update_index_name>",
                             opts(order = [1, 3, 2])
                             ),
                            ("<update_other_table_name> AS <update_alias> INDEXED BY <update_index_name>",
                             opts(order = [1, 3, 2])
                             ),
                            "<update_other_table_name> NOT INDEXED",
                            ("<update_other_table_name> <update_alias> NOT INDEXED",
                             opts(order = [1, 2])
                             ),
                            ("<update_other_table_name> AS <update_alias> NOT INDEXED",
                             opts(order = [1, 2])
                             ),
                            "(<update_table_or_subquery>)",
                            "(<update_join_clause>)"],
    "<update_join_clause>":["<update_table_or_subquery>", 
                            ("<update_other_table_name> <join_operator> <update_table_or_subquery> <join_constraint>",
                            opts(order = [1, 2, 3, 4])
                            ),
                            ],
    "<join_operator>": [",", "JOIN", "<natural_join>", "CROSS JOIN"],
    "<join_constraint>": ["ON <expr>"],
    "<where_clause>": ["WHERE <expr>" ,"WHERE <expr> <having_expr>"],
    "<having_expr>": ["HAVING <expr>"],
    "<update_alias>": ["<string>"],
    "<update_table_name>": [("<string>",
                             opts(post = lambda u_table_name: db.get_update_table_name(u_table_name))
                             )],
    "<update_column_name>": [("<string>",
                              opts(post = lambda u_column_name: db.get_update_column_name(u_column_name))
                              )],
    "<update_other_table_name>": [("<string>",
                                   opts(post = lambda update_other_table_name: db.get_update_other_table_name(update_other_table_name))
                                   )],
    "<update_index_name>": [("<string>",
                             opts(post = lambda u_index_name: db.get_update_other_column_name(u_index_name))
                             )],
}

### GRAMMAR ###############################################################################################

grammar = {
    "<start>": ["<create_table_phase>", "<create_index_view_phase>", "<other_phase>"],
    
    "<create_table_phase>": ["<create_table_stmt>",],
    
    "<create_index_view_phase>": ["<create_index_stmt>", "<create_view_stmt>", 
                                  "<create_virtual_table_stmt>"
                                  ],
    
    "<other_phase>": ["<select_stmt>", "<insert_stmt>",
                      "<alter_table_stmt>", "<delete_stmt>", "<update_stmt>",
                      "<attach_stmt>", "<detach_stmt>",
                      "<analyze_stmt>", "<begin_stmt>", "<commit_stmt>", "<rollback_stmt>",
                      "<savepoint_stmt>", "<release_stmt>", "<reindex_stmt>", "<vacuum_stmt>",
                      "<pragma_stmt>", "<simple_function_invocation>",
                      "<date_time_functions>",
                      "<drop_index_stmt>", "<drop_table_stmt>", "<drop_view_stmt>",
                      "<with_clause>",
                    ],

    **create_table_stmt,
    **create_index_stmt,
    **create_view_stmt,
    **create_virtual_table_stmt,
    **select_stmt,
    **insert_stmt,
    **alter_table_stmt,
    **delete_stmt,
    **update_stmt,
    **attach_stmt,
    **detach_stmt,
    **analyze_stmt,
    **begin_stmt,
    **commit_stmt,
    **rollback_stmt,
    **savepoint_stmt,
    **release_stmt,
    **reindex_stmt,
    **vacuum_stmt,
    **pragma_stmt,
    **simple_function_invocation,
    **date_time_functions,
    **drop_index_stmt,
    **drop_table_stmt,
    **drop_view_stmt,
    **with_clause,
}