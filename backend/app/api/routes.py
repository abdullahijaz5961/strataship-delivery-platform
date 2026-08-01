from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import Release
from app.schemas import ReleaseCreate
from app.services import seed,clone_release
router=APIRouter()
def data(r): return {"id":r.id,"service":r.service,"version":r.version,"environment":r.environment,"status":r.status,"strategy":r.strategy,"commit_sha":r.commit_sha,"created_at":r.created_at}
@router.get("/releases")
def list_releases(db:Session=Depends(get_db)): seed(db);return [data(r) for r in db.query(Release).order_by(Release.id.desc()).all()]
@router.post("/releases",status_code=201)
def create_release(p:ReleaseCreate,db:Session=Depends(get_db)):
    r=Release(**p.model_dump(),status="verifying");db.add(r);db.commit();db.refresh(r);return data(r)
@router.post("/releases/{release_id}/promote",status_code=201)
def promote(release_id:int,db:Session=Depends(get_db)):
    r=db.get(Release,release_id)
    if not r: raise HTTPException(404,"Release not found")
    if r.environment=="production": raise HTTPException(409,"Release is already in production")
    target="staging" if r.environment=="development" else "production"
    return data(clone_release(db,r,target,"healthy"))
@router.post("/releases/{release_id}/rollback",status_code=201)
def rollback(release_id:int,db:Session=Depends(get_db)):
    r=db.get(Release,release_id)
    if not r: raise HTTPException(404,"Release not found")
    return data(clone_release(db,r,r.environment,"rolled_back"))
@router.get("/summary")
def summary(db:Session=Depends(get_db)):
    seed(db); rows=db.query(Release).all();return {"services":len(set(r.service for r in rows)),"production_healthy":sum(r.environment=="production" and r.status=="healthy" for r in rows),"verifying":sum(r.status=="verifying" for r in rows),"deployment_frequency":18.6}
