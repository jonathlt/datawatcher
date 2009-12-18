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

-- Function: at_sys_table_compatible(text, text)

-- DROP FUNCTION at_sys_table_compatible(text, text);

CREATE OR REPLACE FUNCTION at_sys_table_compatible(_curtable text, _newtable text)
  RETURNS integer AS
$BODY$
DECLARE
	v_res 		INTEGER;
	v_qry   	TEXT;
	v_cnt    	INTEGER;
	v_ncnt 		INTEGER;
	v_newTbl 	TEXT;
	v_curTbl    TEXT;
BEGIN

	v_newTbl := '^(' || btrim(_newTable,'"') || ')$';
	v_curTbl := '^(' || btrim(_curTable,'"') || ')$';

	v_qry := ' SELECT COUNT(*) FROM information_schema.columns WHERE table_name ~ ' ;

	EXECUTE   v_qry ||  quote_literal(v_curTbl)  INTO v_cnt;
	EXECUTE   v_qry ||  quote_literal(v_newTbl)  INTO v_ncnt;
	
	v_res := v_cnt - v_ncnt;

	IF ( v_res != 0  AND v_cnt != 0 )
	THEN
		RAISE EXCEPTION ' Number of columns are not equal';
	END IF;
 
	v_qry := ' SELECT count(*) FROM 	
		(
		SELECT a.attname,  a.atttypid, a.atttypmod,
	 	a.attnum FROM pg_catalog.pg_attribute a, pg_catalog.pg_class c
   	 	WHERE a.attrelid = c.oid and c.relname ~ ' || quote_literal(v_newTbl) || 
		' AND a.attnum > 0 ORDER BY a.attnum
		) AS type1 NATURAL JOIN
		(
		SELECT  a.attname,  a.atttypid, a.atttypmod,
		a.attnum FROM pg_catalog.pg_attribute a, pg_catalog.pg_class c 
		WHERE a.attrelid = c.oid and c.relname ~ ' || quote_literal(v_curTbl) || 
		' AND a.attnum > 0 ORDER BY a.attnum
		) AS type2';

	EXECUTE v_qry INTO v_res;

    IF ( v_res != v_cnt OR v_res != v_ncnt )
	THEN
		RAISE EXCEPTION ' tables are not comparable';
	END IF; 

	RETURN 0;
    EXCEPTION WHEN OTHERS THEN
		RETURN 1;
END;
$BODY$
  LANGUAGE 'plpgsql' VOLATILE;
ALTER FUNCTION at_sys_table_compatible(text, text) OWNER TO postgres;
COMMENT ON FUNCTION at_sys_table_compatible(text,text) IS 'Reserved - Astun Technology Core Function';
