from pathlib import Path
from PIL import Image, ImageOps, ImageDraw

root = Path(__file__).resolve().parent.parent
source = root / 'tmp/pdfs/pages-hires'
target = root / 'assets/codex'
target.mkdir(parents=True, exist_ok=True)
pages = sorted(source.glob('page-*.png'))
assert len(pages) == 10, f'Expected 10 pages, got {len(pages)}'
sheet = Image.new('RGB', (1000, 740), '#dddddd')
draw = ImageDraw.Draw(sheet)
for index, page in enumerate(pages, 1):
    with Image.open(page) as image:
        image = image.convert('RGB')
        image.save(target / f'page-{index:02}.webp', 'WEBP', lossless=True, method=6)
        thumb = ImageOps.contain(image, (184, 334))
        x = ((index - 1) % 5) * 200 + (200 - thumb.width) // 2
        y = ((index - 1) // 5) * 370 + 10
        sheet.paste(thumb, (x, y))
        draw.text((x, y + thumb.height + 4), f'Page {index}', fill='black')
sheet.save(root / 'tmp/pdfs/contact-sheet.jpg')
print(f'Exported {len(pages)} lossless pages: {sum(p.stat().st_size for p in target.glob("*.webp"))} bytes')
