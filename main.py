from fastapi import FastAPI, HTTPException,Response
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List

app = FastAPI(title="Two Sum API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def health_check():
    return {"status": "ok"}



@app.head("/")
def head_check():
    return Response(status_code=200)


class TwoSumRequest(BaseModel):
    nums: List[int]
    target: int

class TwoSumResponse(BaseModel):
    indices: List[int]

@app.post("/two-sum", response_model=TwoSumResponse)
def two_sum(payload: TwoSumRequest):
    nums = payload.nums
    target = payload.target

    seen = {}  # value -> index

    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return {"indices": [seen[complement], i]}
        seen[num] = i

    # As per problem statement, this should not happen
    raise HTTPException(status_code=400, detail="No valid two-sum solution found")
