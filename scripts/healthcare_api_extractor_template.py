"""Generic paginated REST extractor pattern.

Configure endpoint and credentials via environment variables. This is a template:
the target API's authentication and pagination contract must be confirmed first.
It is intentionally not pointed at any real patient system.
"""
from __future__ import annotations
import json, os, sys, time
from pathlib import Path
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL=os.environ.get("HDA_API_BASE_URL","").rstrip("/")
ENDPOINT=os.environ.get("HDA_API_ENDPOINT","")
TOKEN=os.environ.get("HDA_API_TOKEN","")
OUT=Path(os.environ.get("HDA_API_OUTPUT","api_extract.jsonl"))
PAGE_SIZE=int(os.environ.get("HDA_API_PAGE_SIZE","100"))

def build_session():
    retry=Retry(total=4,connect=4,read=4,backoff_factor=0.8,
        status_forcelist=[429,500,502,503,504],allowed_methods=["GET"],respect_retry_after_header=True)
    session=requests.Session()
    session.mount("https://",HTTPAdapter(max_retries=retry))
    session.headers.update({"Accept":"application/json"})
    if TOKEN: session.headers["Authorization"]=f"Bearer {TOKEN}"
    return session

def main():
    if not BASE_URL or not ENDPOINT:
        raise SystemExit("Set HDA_API_BASE_URL and HDA_API_ENDPOINT before running.")
    if not BASE_URL.startswith("https://"):
        raise SystemExit("Refusing non-HTTPS API base URL. Use an approved secure endpoint.")
    session=build_session()
    url=f"{BASE_URL}/{ENDPOINT.lstrip('/')}"
    params={"limit":PAGE_SIZE}
    count=0
    OUT.parent.mkdir(parents=True,exist_ok=True)
    with OUT.open("w",encoding="utf-8") as f:
        while url:
            response=session.get(url,params=params,timeout=(5,30))
            response.raise_for_status()
            payload=response.json()
            if not isinstance(payload,dict) or not isinstance(payload.get("results"),list):
                raise ValueError("Unexpected API response: expected object with results[]")
            for record in payload["results"]:
                f.write(json.dumps(record,ensure_ascii=False,allow_nan=False)+"\n")
                count+=1
            # Example contract: server returns a full `next` URL or null.
            url=payload.get("next")
            params=None # next URL already carries query parameters
            if url and not url.startswith(BASE_URL+"/"):
                raise ValueError("API next link points outside the configured base URL.")
            time.sleep(0.1)
    print(f"Extracted {count} records to {OUT}")
    print("Validate schema, access scope, retention and PHI handling before production use.")

if __name__=="__main__": main()
