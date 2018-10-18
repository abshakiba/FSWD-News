import datetime
import psycopg2


def get_views():
    db = psycopg2.connect(database="news")
    c = db.cursor()
    q = """select A.title, B.num as views
        from articles as A
        JOIN (Select split_part(path,'/',3) as title, count(*) AS num
        from log where status like '%OK%'
        group by path
        order by num desc limit 4) as B
        on A.slug = B.title order by views desc;"""
    c.execute(q)
    return c.fetchall()
    db.close()


def get_authors():
    db = psycopg2.connect(database="news")
    c = db.cursor()
    q = """select A.name, T.sum_views
        from authors as A join (select author, sum(views) as sum_views
        from top_articles
        group by author
        order by sum_views) as T
        on A.id = T.author
        order by T.sum_views desc limit 3;"""
    c.execute(q)
    return c.fetchall()
    db.close()


def get_error():
    db = psycopg2.connect(database="news")
    c = db.cursor()
    q = """select * from (
        select to_char(date_trunc('day',time),'Mon DD, YYYY') as date_only,
        round((100.0 * sum(case when status like '%404%' then 1 else 0 end))
        / count(*),2) from log group by date_only) as t
        where round > 1;"""
    c.execute(q)
    return c.fetchall()
    db.close()
