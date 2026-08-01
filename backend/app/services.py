from sqlalchemy.orm import Session
from app.models import Release
SEED=[("gateway","2.8.1","production","healthy","canary","a9c31e2"),("identity","1.14.0","production","healthy","rolling","bf14ac9"),("workflow-api","3.2.4","staging","verifying","blue-green","7d81c1a"),("web-console","5.6.0","production","healthy","rolling","1e5a00c")]
def seed(db:Session):
    if db.query(Release).count()==0:
        for x in SEED: db.add(Release(service=x[0],version=x[1],environment=x[2],status=x[3],strategy=x[4],commit_sha=x[5]))
        db.commit()
def clone_release(db,row,environment,status):
    new=Release(service=row.service,version=row.version,environment=environment,status=status,strategy=row.strategy,commit_sha=row.commit_sha)
    db.add(new);db.commit();db.refresh(new);return new
