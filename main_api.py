
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Header
import jwt
from pydantic import BaseModel
from sqlalchemy import text
from db import DW
from passlib.hash import pbkdf2_sha512 as pl
from dotenv import load_dotenv


#ohjelma kaynnistys uvicorn main_api:app
#uvicorn main_api:app
#http://localhost:8000/docs

app = FastAPI()

class RegisterRequest(BaseModel):
    username:str
    password:str
    roles_id:int

SECRET_KEY =os.getenv("SECRET_KEY")


def require_login(dw:DW,authorization=Header(None,alias='api_key')):
    try:
            if authorization is not None and len(authorization.split(' ')) ==2:
                validated=jwt.decode(authorization.split(' ')[1],SECRET_KEY,algorithms=['HS512'])
                user= dw.execute(text('SELECT username FROM auth_users WHERE id = :id'),{'id':validated['id']}).mappings().first()

                if user is None:
                    raise HTTPException(detail='unauthorized', status_code=401)
                return user
            else:
                raise HTTPException(detail='unauthorized', status_code=401)
    except Exception as e:
       raise HTTPException(detail=str(e), status_code=500)


LoggedInUser= Annotated[dict,Depends(require_login)]

@app.get('/api/account')
async def get_account(logged_in_user: LoggedInUser):
    return logged_in_user
   



@app.post('/api/login')
async def login(dw:DW,req:RegisterRequest):
    _query_str=("SELECT * FROM auth_users WHERE username = :username")
    _query = text(_query_str)
    user=dw.execute(_query,{'username':req.username,}).mappings().first()
    if user is None:
        raise HTTPException(detail='user not found', status_code=404)
    
    passwo_correct=pl.verify(req.password, user['password'])
    if passwo_correct:
        token=jwt.encode({'id':user['id']}, SECRET_KEY,algorithm='HS512')
        return{'token':token}
    

@app.post('/api/register')
async def register(dw: DW, req: RegisterRequest):
    try:
        _query_str = ("INSERT INTO auth_users(username,password,roles_id) VALUES(:username, :password, :roles_id)")
        _query = text(_query_str)
        user = dw.execute(_query,{'username': req.username,'password': pl.hash(req.password),'roles_id': req.roles_id})
        dw.commit()
        return {'username': req.username, 'id': user.lastrowid, 'roles_id': req.roles_id}
    except Exception as e:
        dw.rollback()
        print(e)
        raise HTTPException(status_code=422, detail='Error registering user')




@app.get('/api/rentals/1-weekly-by-month/{month}/{year}')
async def get_rentals_weekly_by_month(dw:DW, month:int, year:int,logged_in_user:LoggedInUser):
    _query_str = """
        SELECT YEAR(created_at) AS year,MONTH(created_at) as month, WEEK(created_at) AS week, COUNT(*) AS items 
        FROM rental_items AS ri
        WHERE YEAR(created_at) = :year AND MONTH(created_at) = :month
        GROUP BY week;
        """

    _query = text(_query_str)
    rows= dw.execute(_query,{'year':year, 'month':month})
    data = rows.mappings().all()
    return {'data':data}

@app.get('/api/rentals/2-weekly-by-month/{month}/{year}')
async def get_rentals_daily_by_month(dw:DW, month:int, year:int,logged_in_user:LoggedInUser):
    _query_str = """
        SELECT YEAR(created_at) AS year,MONTH(created_at) as month, DAY(created_at) AS day, COUNT(*) AS items 
	    FROM rental_items as ri
	    WHERE YEAR(created_at) = :year AND MONTH(created_at) = :month
	    GROUP BY day;
        """

    _query = text(_query_str)
    rows= dw.execute(_query,{'year':year, 'month':month})
    data = rows.mappings().all()
    return {'data':data}
    

@app.get('/api/rentals/3-year-group-by-month/{year}')
async def get_rentals_year_groupby_month(dw:DW,year:int,logged_in_user:LoggedInUser):
    _query_str = """
        SELECT YEAR(created_at) AS year,MONTH(created_at) as month, COUNT(*) AS items 
	    FROM rental_items 
	    WHERE YEAR(created_at) = :year
	    GROUP BY month;
        """

    _query = text(_query_str)
    rows= dw.execute(_query,{'year':year})
    data = rows.mappings().all()
    return {'data':data}


@app.get('/api/rentals/4-alltime-top10/')
async def get_rentals_alltime_top10(dw:DW,logged_in_user:LoggedInUser):
    _query_str = """
            SELECT ri.name, COUNT(*) AS items 
            FROM rental_transaction AS rt
            INNER JOIN rental_items AS ri ON ri.id = rt.rental_items_id
            GROUP BY rt.rental_items_id
            ORDER BY items DESC
            LIMIT 10;
        """

    _query = text(_query_str)
    rows= dw.execute(_query)
    data = rows.mappings().all()
    return {'data':data}


@app.get('/api/rentals/5-top10-year-groupby-month/{year}')
async def get_rentals_top10_year_monthly(dw:DW,year:int,logged_in_user:LoggedInUser):
    _query_str = """
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

    _query = text(_query_str)
    rows= dw.execute(_query,{'year':year})
    data = rows.mappings().all()
    return {'data':data}

@app.get('/api/rentals/6-year-most-items-added/{year}')
async def get_rental_year_most_items_added(dw:DW,year:int,logged_in_user:LoggedInUser):
    _query_str = """
        SELECT YEAR(ri.created_at) AS year,
        MONTH(ri.created_at) AS month,
        COUNT(*) AS items_added 
	    FROM rental_items AS ri
	    WHERE YEAR(ri.created_at) = :year
	    GROUP BY YEAR(ri.created_at), MONTH(ri.created_at)
	    ORDER BY items_added DESC
	    LIMIT 1;
        """

    _query = text(_query_str)
    rows= dw.execute(_query,{'year':year})
    data = rows.mappings().all()
    return {'data':data}