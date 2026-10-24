import sys, os, fitz
src, outdir = sys.argv[1], sys.argv[2]
os.makedirs(outdir, exist_ok=True)
doc = fitz.open(src)
tag = os.path.basename(src).split('-')[-1][:16].replace('.pdf','')
# first page title
print(f"\n=== {os.path.basename(src)} | {doc.page_count}p")
print("  TITLE:", " ".join(doc[0].get_text().split())[:150])
n = 0
for pno in range(doc.page_count):
    for i, img in enumerate(doc[pno].get_images(full=True)):
        xref = img[0]
        try:
            pix = fitz.Pixmap(doc, xref)
            if pix.width < 300 or pix.height < 180:
                continue
            if pix.n - pix.alpha >= 4:
                pix = fitz.Pixmap(fitz.csRGB, pix)
            fn = f"{outdir}/{tag}_p{pno+1:02d}_{i}.png"
            pix.save(fn); n += 1
            print(f"   p{pno+1:<3} {pix.width}x{pix.height}  -> {os.path.basename(fn)}")
        except Exception as e:
            pass
print(f"  extracted {n}")
