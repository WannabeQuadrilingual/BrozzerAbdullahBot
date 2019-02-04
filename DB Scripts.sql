CREATE TABLE already_replied (
comment_id VARCHAR(10),
created_date TIMESTAMP DEFAULT NOW() 
);

delete from already_replied where comment_id in ()

CREATE OR REPLACE FUNCTION keep_limited_rows()
RETURNS TRIGGER AS
$body$
DECLARE
    table_name text;
    delete_key text;
    order_by text;
    max_rows INTEGER;
BEGIN
    table_name := TG_ARGV[0];
    delete_key := TG_ARGV[1];
    order_by := TG_ARGV[2]; 
    max_rows := TG_ARGV[3]; 
    EXECUTE(format('delete from %s where %s in (SELECT %s FROM %s ORDER BY %s DESC, %s DESC OFFSET %s)',table_name, delete_key, delete_key, table_name, order_by, delete_key, max_rows));
    RETURN NULL;
END;
$body$
LANGUAGE plpgsql;

CREATE TRIGGER already_replied_keep_limited_rows
AFTER INSERT ON already_replied
FOR EACH STATEMENT EXECUTE PROCEDURE keep_limited_rows('already_replied', 'comment_id', 'created_date', 100);


