from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from stroll.database.database import seed_db, try_migration
from stroll.services.core.question_assignments import assign_questions_for_cycle, get_questions_for_cycle
from stroll.database.service import get_db


app = FastAPI()

@app.on_event("startup")
async def startup_event():
    try:
        try_migration()
        print("Migration successful")
        seed_db(next(get_db()))
    except Exception as e:
        raise RuntimeError(f"Failed to migrate or seed database: {e}")

@app.get("/question/{user_id}")
async def get_question_for_user(user_id: int, cycle_number: int, db: Session = Depends(get_db)):
    try:
        question = assign_questions_for_cycle(user_id, cycle_number, db)
        return {"question for this cycle": question}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/questions/{cycle_id}/{region_name}")
async def get_cycle_questions(cycle_id: int, region_name: str, db: Session = Depends(get_db)):
    try:
        questions = get_questions_for_cycle(cycle_id, region_name, db)
        return {"questions for this cycle": questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


