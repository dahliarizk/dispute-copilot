from fastapi import FastAPI

app = FastAPI(title="Dispute Copilot")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}