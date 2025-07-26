import pathlib
import re

def test_markdown_code_fences_closed():
    for md_path in pathlib.Path('.').rglob('*.md'):
        text = md_path.read_text(encoding='utf-8')
        fence_count = len(re.findall(r'^```', text, flags=re.MULTILINE))
        assert fence_count % 2 == 0, f"Unclosed code block in {md_path}"
