from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
SHARE = ROOT / "share"
SKIP = {".git", ".github", "share", "scripts"}
IMAGE_EXTS = {".jpg", ".jpeg", ".png"}
LABELS = {
    "wonji": "원지",
    "omh": "외매화",
}


def is_project_folder(path: Path) -> bool:
    if not path.is_dir() or path.name in SKIP or path.name.startswith("."):
        return False
    return any(
        child.is_file() and child.suffix.lower() in IMAGE_EXTS
        for child in path.iterdir()
    )


def build_html(folder: str, label: str) -> str:
    target = (
        "https://gonzaljeong.github.io/360-pano/manager.html"
        f"?folder={quote(folder)}&assigned=1"
    )
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{label} 360 Panorama</title>
  <meta http-equiv="refresh" content="0; url={target}" />
  <style>
    body {{
      margin:0; min-height:100vh; display:grid; place-items:center;
      background:#f4f7fb; color:#1f2937;
      font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,"Noto Sans KR",sans-serif;
    }}
    .box {{
      width:min(520px,calc(100% - 32px)); padding:28px;
      background:#fff; border:1px solid #dbe3ec; border-radius:16px;
      text-align:center; box-shadow:0 8px 24px rgba(31,41,55,.06);
    }}
    a {{ color:#2563eb; font-weight:700; }}
  </style>
</head>
<body>
  <div class="box">
    <h2>{label} 360 Panorama</h2>
    <p>담당자용 관리 페이지를 여는 중입니다.</p>
    <p>자동으로 열리지 않으면 <a href="{target}">여기를 클릭하세요.</a></p>
  </div>
  <script>location.replace({target!r});</script>
</body>
</html>
'''


def main() -> None:
    SHARE.mkdir(exist_ok=True)
    projects = sorted(
        (p for p in ROOT.iterdir() if is_project_folder(p)),
        key=lambda p: p.name.lower(),
    )

    expected = set()
    for project in projects:
        folder = project.name
        label = LABELS.get(folder.lower(), folder)
        filename = f"{folder}_360관리.html"
        expected.add(filename)
        (SHARE / filename).write_text(
            build_html(folder, label), encoding="utf-8", newline="\n"
        )

    for old_file in SHARE.glob("*_360관리.html"):
        if old_file.name not in expected:
            old_file.unlink()

    print(f"Generated {len(expected)} assignee manager file(s).")


if __name__ == "__main__":
    main()
