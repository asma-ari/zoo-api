import csv
import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

class UTF8JSONResponse(JSONResponse):
    media_type = "application/json; charset=utf-8"

    def render(self, content) -> bytes:
        return json.dumps(content, ensure_ascii=False, indent=2).encode("utf-8")


app = FastAPI(title="Zoo Visitors API 2569", default_response_class=UTF8JSONResponse)
CSV_FILE = Path(__file__).parent / "zoo_visitors.csv"
RESOURCE_ID = "0ecc96cf-d914-42a1-b184-dbbd013c3c9c"


def read_csv():
    if not CSV_FILE.exists():
        raise HTTPException(status_code=500, detail="ไม่พบไฟล์ zoo_visitors.csv")
    for enc in ("utf-8-sig", "utf-8", "cp874"):
        try:
            with open(CSV_FILE, newline="", encoding=enc) as f:
                return list(csv.DictReader(f))
        except UnicodeDecodeError:
            continue
    raise HTTPException(status_code=500, detail="อ่านไฟล์ CSV ไม่ได้ (encoding ไม่รองรับ)")


@app.get("/")
def root():
    return {"message": "ไปที่ /docs หรือ /api/zoo-visitors"}


@app.get("/api/zoo-visitors")
def zoo_visitors():
    rows = read_csv()
    return {
        "source": "Data.go.th - องค์การสวนสัตว์แห่งประเทศไทย ในพระบรมราชูปถัมภ์",
        "dataset": "zoo-visitors2569",
        "fiscal_year": 2569,
        "resource_id": RESOURCE_ID,
        "total_records": len(rows),
        "fields": list(rows[0].keys()) if rows else [],
        "records": rows,
    }
