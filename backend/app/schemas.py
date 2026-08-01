from pydantic import BaseModel, Field
class ReleaseCreate(BaseModel):
    service: str=Field(min_length=2,max_length=80)
    version: str=Field(min_length=1,max_length=40)
    environment: str=Field(pattern="^(development|staging|production)$")
    strategy: str=Field(default="rolling",pattern="^(rolling|canary|blue-green)$")
    commit_sha: str=Field(min_length=7,max_length=12)
