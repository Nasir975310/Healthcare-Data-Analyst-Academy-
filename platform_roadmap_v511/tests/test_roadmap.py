import json
from pathlib import Path
ROOT=Path(__file__).parents[2]
def test_roadmap_statuses_and_ids():
    data=json.loads((Path(__file__).parents[1]/"data/roadmap.json").read_text())
    items=[item for track in data["tracks"] for item in track["items"]]
    assert len(items)==34
    assert {item["status"] for item in items} <= {"completed","partial","pending","verify"}
    ids=[item["id"] for item in items]
    assert len(ids)==len(set(ids))
def test_roadmap_view_integrated():
    html=(ROOT/"index.html").read_text()
    assert 'data-view="platform-roadmap-v511"' in html
    assert 'id="view-platform-roadmap-v511"' in html
    assert 'assets/platform-roadmap-v511.js' in html
