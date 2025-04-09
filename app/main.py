from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from . import models, schemas, utils, database
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/shorten", response_model=schemas.URLInfo)
def shorten_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    short_code = utils.generate_short_code()
    while db.query(models.URL).filter_by(short_code=short_code).first():
        short_code = utils.generate_short_code()
    db_url = models.URL(original_url=str(url.original_url), short_code=short_code)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

@app.get("/{short_code}")
def original_url(short_code: str, db: Session = Depends(get_db)):
    url = db.query(models.URL).filter_by(short_code=short_code).first()
    if url:
        return {"original_url": url.original_url, "short_code": url.short_code}
    return {"error": "Not found"}