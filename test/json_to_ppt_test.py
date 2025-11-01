import pytest
from app.tools.JsonToPPT import json_to_ppt_bytes
from io import BytesIO
def test_empty_slides_raises():
    with pytest.raises(ValueError):
        json_to_ppt_bytes({"slides": []})

def test_single_slide_str_bullet():
    slide_json = {"slides": [{"header": "Title", "bullets": "One point"}]}
    result = json_to_ppt_bytes(slide_json)
    assert isinstance(result, BytesIO)
