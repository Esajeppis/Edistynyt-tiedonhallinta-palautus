from sqlalchemy import text
from db import get_db



def query_1(year,month):
    with get_db() as _db:
        query = """
        SELECT YEAR(created_at) AS year,MONTH(created_at) as month, WEEK(created_at) AS week, COUNT(*) AS items 
        FROM rental_items AS ri
        WHERE YEAR(created_at) = :year AND MONTH(created_at) = :month
        GROUP BY week;
        """
        try:
            result = _db.execute(text(query), {'year': year,'month':month})
            print("Year\tMonth\tWeek\tItems")
            for row in result:
                print("\t".join(str(col) for col in row))
        except Exception as e:
            print(e)

def query_2(year,month):
    with get_db() as _db:
        query = """
        SELECT YEAR(created_at) AS year,MONTH(created_at) as month, DAY(created_at) AS day, COUNT(*) AS items 
	    FROM rental_items 
	    WHERE YEAR(created_at) = :year AND MONTH(created_at) = :month
	    GROUP BY day;
        """
        try:
            result = _db.execute(text(query), {'year': year,'month':month})
            print("Year\tMonth\tDay\tItems")
            for row in result:
                print("\t".join(str(col) for col in row))
        except Exception as e:
            print(e)

def query_3(year):
    with get_db() as _db:
        query = """
        SELECT YEAR(created_at) AS year,MONTH(created_at) as month, COUNT(*) AS items 
	    FROM rental_items 
	    WHERE YEAR(created_at) = :year
	    GROUP BY month;
        """
        try:
            result = _db.execute(text(query), {'year': year})
            print("Year\tMonth\tItems")
            for row in result:
                print("\t".join(str(col) for col in row))
        except Exception as e:
            print(e)


def allthetimeTop10():
    with get_db() as _db:
        query = """
            SELECT ri.name, COUNT(*) AS items 
            FROM rental_transaction AS rt
            INNER JOIN rental_items AS ri ON ri.id = rt.rental_items_id
            GROUP BY rt.rental_items_id
            ORDER BY items DESC
            LIMIT 10;
        """
        try:
            result = _db.execute(text(query))
            print("{:<30}\t{:<10}".format("Name","Items"))
            for row in result:
                print("{:<30}\t{:<10}".format(*row))
        except Exception as e:
            print(e)


def query2_top10(year):
    with get_db() as _db:
        query = """
        SELECT ri.name, 
        YEAR(rt.created_at) AS year, 
        MONTH(rt.created_at) AS month,
        COUNT(*) AS items 
	    FROM rental_transaction AS rt
	    INNER JOIN rental_items AS ri ON ri.id = rt.rental_items_id
	    WHERE YEAR(rt.created_at) = :year
	    GROUP BY rt.rental_items_id, YEAR(rt.created_at), MONTH(rt.created_at)
	    ORDER BY year, month, items DESC
	    LIMIT 10;
        """
        try:
            result = _db.execute(text(query), {'year': year})
            print("{:<30}\t{:<10}\t{:<10}\t{:<10}".format("Name", "Year", "Month", "Items"))
            for row in result:
                print("{:<30}\t{:<10}\t{:<10}\t{:<10}".format(*row))
        except Exception as e:
            print(e)

def query3_top10(year):
    with get_db() as _db:
        query = """
        SELECT YEAR(ri.created_at) AS year,
        MONTH(ri.created_at) AS month,
        COUNT(*) AS items_added 
	    FROM rental_items AS ri
	    WHERE YEAR(ri.created_at) = :year
	    GROUP BY YEAR(ri.created_at), MONTH(ri.created_at)
	    ORDER BY items_added DESC
	    LIMIT 1;
        """
        try:
            result = _db.execute(text(query), {'year': year})
            print("Year\tMonth\tItems")
            for row in result:
                print("\t".join(str(col) for col in row))
        except Exception as e:
            print(e)


