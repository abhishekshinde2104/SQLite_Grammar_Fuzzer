# SQLite_Grammar_Fuzzer

# Project Tasks
There are two tasks in this project:
1. Implement a diverse SQLite grammar in grammar.py which is able to generate all commands understood by SQLite. The grammar should be general: For instance, a CREATE TABLE command should be able to generate diverse table names. The page at https://www.sqlite.org/lang.html provides very detailed information about all commands of SQLite.

2. Implement the function fuzz_one_input in fuzzer.py. The signature of this function must not be changed. The function should implement a grammar-based blackbox input generation for SQLite. You may add arbitrary code and functions in this file, but the entry point must be fuzz_one_input. Be creative in this task, and come up with ways to generate interesting inputs!
