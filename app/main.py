from fastapi import FastAPI
from api.v1 import router as v1_router
# from settings import APP_NAME, APP_VERSION

app = FastAPI()


# app = FastAPI(
#     title=APP_NAME,
#     version=settings.APP_VERSION
# )

# Routers
app.include_router(v1_router.router, prefix="/api")

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}