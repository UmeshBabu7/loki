from pydantic import BaseModel


class GitLeaksSchema(BaseModel):
    RuleID: str
    File: str
    StartLine: int
    Description: str
