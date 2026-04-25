from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def welcome():
    return "welcome to extra class!"

@app.post("/register", response_model=schemas.mobileResponse)
def register(mobiles: schemas.mobileCreate, db: Session = Depends(get_db)):
    return crud.create_mobiles(db, mobiles)

@app.get("/mobiles", response_model=list[schemas.mobileResponse])
def read_mobiles(db: Session = Depends(get_db)):
    return crud.get_mobiles(db)

@app.get("/mobiles/{mobile_id}", response_model=schemas.mobileResponse)
def read_mobile(mobile_id: int, db: Session = Depends(get_db)):
    mobile = crud.get_mobile(db, mobile_id)
    if not mobile:
        raise HTTPException(status_code=404, detail="mobile not found")
    return mobile

@app.put("/mobiles/{mobile_id}", response_model=schemas.mobileResponse)
def update(mobile_id: int, mobile: schemas.mobileCreate, db: Session = Depends(get_db)):
    updated_mobile = crud.update_mobile(db, mobile_id, mobile)
    if not updated_mobile:
        raise HTTPException(status_code=404, detail="mobile not found")
    return updated_mobile

@app.delete("/mobiles/{mobile_id}")
def delete(mobile_id: int, db: Session = Depends(get_db)):
    mobile = crud.delete_mobile(db, mobile_id)
    if not mobile:
        raise HTTPException(status_code=404, detail="mobile not found")
    return {"message": "mobile deleted"}
