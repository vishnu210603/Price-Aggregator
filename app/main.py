# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from app.scraper_factory import get_scrapers
# import traceback
# from dotenv import load_dotenv

# load_dotenv()
# app = FastAPI()

# class QueryRequest(BaseModel):
#     country: str
#     query: str

# @app.get("/")
# def root():
#     return {"message": "Welcome"}

# @app.post("/search")
# async def search_products(req: QueryRequest):
#     try:
#         scrapers = get_scrapers(req.country.upper())
#         if not scrapers:
#             raise HTTPException(status_code=400, detail="Country not supported.")

#         results = []
#         for sc in scrapers:
#             results += await sc.scrape(req.query)

#         if not results:
#             raise HTTPException(status_code=404, detail="No products found.")

#         return sorted(results, key=lambda x: x["price"])

#     except Exception:
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail="Internal error")



# from fastapi.middleware.cors import CORSMiddleware
# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from app.scraper_factory import get_scrapers
# import traceback
# from dotenv import load_dotenv

# load_dotenv()

# app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Change to ["http://localhost:5173"] in production
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ✅ Allow frontend (React) to access the API
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Replace with your frontend origin in production
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ✅ Request model
# class QueryRequest(BaseModel):
#     country: str
#     query: str

# # ✅ Health check
# @app.get("/")
# def root():
#     return {"message": "Welcome to the Price Aggregator API 🚀"}

# # ✅ Search endpoint
# @app.post("/search")
# async def search_products(req: QueryRequest):
#     try:
#         scrapers = get_scrapers(req.country.upper())
#         if not scrapers:
#             raise HTTPException(status_code=400, detail="Country not supported.")

#         results = []
#         for sc in scrapers:
#             results += await sc.scrape(req.query)

#         if not results:
#             raise HTTPException(status_code=404, detail="No products found.")

#         return sorted(results, key=lambda x: x["price"])

#     except Exception as e:
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail="Internal server error")



from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.scraper_factory import get_scrapers
import traceback
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS: allow your frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your actual frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    country: str
    query: str

@app.get("/")
def root():
    return {"message": "Welcome to the Price Aggregator API 🚀"}

@app.post("/search")
async def search_products(req: QueryRequest):
    try:
        scrapers = get_scrapers(req.country.upper())
        if not scrapers:
            raise HTTPException(status_code=400, detail="Country not supported.")

        results = []
        for sc in scrapers:
            results += await sc.scrape(req.query)

        if not results:
            raise HTTPException(status_code=404, detail="No products found.")

        # sort by numeric price
        try:
            results = sorted(results, key=lambda x: float(x["price"]))
        except Exception:
            pass

        return results

    except HTTPException:
        raise
    except Exception:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error")
