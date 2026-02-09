from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

# --------------------
# App initialization
# --------------------
app = FastAPI(title="Two Sum API")

# --------------------
# CORS configuration (browser-safe)
# --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,   # MUST be False with "*"
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------
# Health check endpoints (required by platform)
# --------------------
@app.get("/")
def health_check():
    return {"status": "ok"}

@app.head("/")
def head_root():
    return Response(status_code=200)

# --------------------
# Request / Response models
# --------------------
class TwoSumRequest(BaseModel):
    nums: List[int]
    target: int

class TwoSumResponse(BaseModel):
    indices: List[int]

# --------------------
# HEAD support for /two-sum (platform probe)
# --------------------
@app.head("/two-sum")
def two_sum_head():
    return Response(status_code=200)

# --------------------
# GET fallback for /two-sum (platform compatibility)
# Example:
# --------------------
@app.get("/two-sum")
def two_sum_get(nums: str, target: int):
    nums_list = list(map(int, nums.split(",")))
    seen = {}

    for i, num in enumerate(nums_list):
        complement = target - num
        if complement in seen:
            return {"indices": [seen[complement], i]}
        seen[num] = i

    raise HTTPException(status_code=400, detail="No valid two-sum solution found")

# --------------------
# POST /two-sum (main required endpoint)
# --------------------
@app.post("/two-sum", response_model=TwoSumResponse)
def two_sum_post(payload: TwoSumRequest):
    seen = {}

    for i, num in enumerate(payload.nums):
        complement = payload.target - num
        if complement in seen:
            return {"indices": [seen[complement], i]}
        seen[num] = i

    raise HTTPException(status_code=400, detail="No valid two-sum solution found")
