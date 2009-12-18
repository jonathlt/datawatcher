REM Script to set up sample database

createdb -U postgres -O postgres -E UTF8 DataWatcherTest
psql -U postgres -d DataWatcherTest <..\at_CompareTablesWithKey.sql
psql -U postgres -d DataWatcherTest <..\at_sys_table_compatible.sql
psql -U postgres -d DataWatcherTest <..\at_sys_get_columnlist.sql
psql -U postgres -d DataWatcherTest <..\at_sys_exists_table2.sql
psql -U postgres -d DataWatcherTest <..\at_sys_exists_table.sql
