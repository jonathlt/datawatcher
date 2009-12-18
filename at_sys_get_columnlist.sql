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

-- Function: at_sys_get_columnlist(text)

-- DROP FUNCTION at_sys_get_columnlist(text);

CREATE OR REPLACE FUNCTION at_sys_get_columnlist(_tablename text)
  RETURNS text AS
$BODY$
DECLARE
	v_qry TEXT;
	tablecols RECORD;
	v_colCSList TEXT;
	v_tableName TEXT;
BEGIN
	v_colCSList = '';
	v_tableName := '^(' || btrim(_tableName,'"') || ')$';

	v_qry :='SELECT a.attname ' ||
		'FROM pg_catalog.pg_attribute a ' ||
		'WHERE a.attnum > 0 ' ||
		'AND NOT a.attisdropped ' ||
		'AND a.attrelid = ' ||
		'( ' ||
		'SELECT c.oid ' ||
		'FROM pg_catalog.pg_class c LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace ' ||
		'WHERE c.relname = ''' || _tablename || ''' AND pg_catalog.pg_table_is_visible(c.oid) )' ;

	FOR tablecols IN EXECUTE v_qry LOOP
		v_colCSList :=  v_colCSList || '"' || tablecols.attname || '",';
	END LOOP;

	-- Strip off last comma as don't need it.
	v_colCSList = trim(trailing ',' from v_colCSList);

	RETURN v_colCSList;

END;

$BODY$
  LANGUAGE 'plpgsql' VOLATILE;
ALTER FUNCTION at_sys_get_columnlist(text) OWNER TO postgres;
COMMENT ON FUNCTION at_sys_get_columnlist(text) IS 'Reserved - Astun Technology Core Function';