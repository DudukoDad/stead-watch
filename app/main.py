from fastapi import FastAPI

from api.v1 import router as v1_router
# import settings

app = FastAPI()


# app = FastAPI(
#     title=settings.APP_NAME,
#     version=settings.APP_VERSION,
#     lifespan=lifespan,
# )

# Routers
app.include_router(v1_router.router, prefix="/api")

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}