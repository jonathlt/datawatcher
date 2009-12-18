-- Copyright (c) 2009 Astun Technology

-- Permission is hereby granted, free of charge, to any person obtaining a copy
-- of this software and associated documentation files (the "Software"), to deal
-- in the Software without restriction, including without limitation the rights
-- to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
-- copies of the Software, and to permit persons to whom the Software is
-- furnished to do so, subject to the following conditions:

-- The above copyright notice and this permission notice shall be included in
-- all copies or substantial portions of the Software.

-- THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
-- IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
-- FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
-- AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
-- LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
-- OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
-- THE SOFTWARE.

CREATE OR REPLACE FUNCTION at_CompareTablesWithKey(_tablename text, _uniquekey text)
  RETURNS integer AS
$BODY$
DECLARE
	v_curTbl	TEXT;
	v_lastTbl	TEXT;
	v_sql		TEXT;
	v_cnt		INTEGER;
	v_colList	TEXT;
	v_lastTblName	TEXT;
	v_view1Name	TEXT;
	v_view2Name	TEXT;
	v_keyName	TEXT;
BEGIN

	v_curTbl := quote_ident(_tablename);
	v_lastTbl := quote_ident( _tablename || '_LASTUPDATE');
	v_view1Name := quote_ident( _tablename || '_view1');
	v_view2Name := quote_ident( _tablename || '_view2');
	v_keyName := quote_ident(_uniquekey);
	
	--Check that the tables are compatible
	v_sql := 'SELECT at_sys_table_compatible(' || quote_literal(_tableName) || ',' || quote_literal(_tableName) || ')';
	EXECUTE v_sql INTO v_cnt;

	IF (v_cnt != 0)
	THEN
		RAISE EXCEPTION 'TABLES NOT COMPATIBLE';
	END IF;

	--Get the column list for the two tables
	v_sql := 'SELECT at_sys_get_columnlist(' || quote_literal(_tableName) || ')';
	EXECUTE v_sql INTO v_colList;

	--Now create a temporary table with the before and after
	v_sql := 'CREATE OR REPLACE VIEW ' || v_view1Name || ' AS ' ||
		 'SELECT MIN(TableName) AS TableName,' || v_colList || ' ' ||
		 'FROM ' ||
		 '( ' ||
		 'SELECT ''_last'' AS TableName, ' || v_colList || ' ' ||
		 'FROM ' || v_lastTbl || ' ' ||
		 'UNION ALL ' ||
		 'SELECT ''_new'' AS TableName, ' || v_colList || ' ' ||
		 'FROM ' || v_curTbl ||
		 ') tmp ' ||
		 'GROUP BY ' || v_colList || ' HAVING COUNT(*) = 1';
	EXECUTE v_sql;

	--Using the supplied key, obtain the rows which have been updated,deleted or inserted
	--Create a view which can be queried directly
	
	v_sql := 'CREATE OR REPLACE VIEW ' || v_view2Name || ' AS ' ||
		 'SELECT ''DELETED''::text as "STATUS"' || ',* FROM ' || v_view1Name || 
		 ' WHERE tablename=''_last'' AND ' || v_keyName || ' NOT IN (SELECT ' || v_keyName || ' FROM ' || v_view1Name || ' WHERE tablename=''_new'')' ||
		 ' UNION ' ||
		 'SELECT ''INSERTED''::text as "STATUS"' || ',* FROM ' || v_view1Name || 
		 ' WHERE tablename=''_new'' AND ' || v_keyName || ' NOT IN (SELECT ' || v_keyName || ' FROM ' || v_view1Name || ' WHERE tablename=''_last'')' ||
		 ' UNION ' ||
		 'SELECT ''UPDATED''::text as "STATUS"' || ',* FROM ' || v_view1Name || 
		 ' WHERE tablename=''_new'' AND ' || v_keyName || ' IN (SELECT ' || v_keyName || ' FROM ' || v_view1Name || ' WHERE tablename=''_last'')';
	EXECUTE v_sql;
	
	RETURN 0;

	EXCEPTION WHEN OTHERS THEN
		RETURN 1;
END

$BODY$
  LANGUAGE 'plpgsql' VOLATILE;