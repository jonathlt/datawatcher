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

-- Function: at_sys_exists_table(text, text)

-- DROP FUNCTION at_sys_exists_table(text, text);

CREATE OR REPLACE FUNCTION at_sys_exists_table(text, text)
  RETURNS integer AS
$BODY$

DECLARE
    sschema alias for $1;
    tablename alias for $2;
    iCount int;
    theschema text;
BEGIN
    -- Work with the schemas
    IF sschema <> '' THEN
      theschema = sschema;
    ELSE
      theschema = 'public';
    END IF;

    -- Get the number of table that satisify the input
    SELECT INTO iCount count(*) FROM information_schema.tables WHERE table_name=tablename AND table_schema=theschema;
    RETURN iCount;
END

$BODY$
  LANGUAGE 'plpgsql' VOLATILE;
ALTER FUNCTION at_sys_exists_table(text, text) OWNER TO postgres;
COMMENT ON FUNCTION at_sys_exists_table(text, text) IS 'Reserved - Astun Technology Core Function';
