# Tổng hợp Pandoc

Pandoc để chuyển đổi tệp. Hết....


### Markdown -> EPUB

```
pandoc file.md -f markdown -t epub -s -o file.epub \
	--metadata title="" \
	--metadata author="Author" \
	--metadata language="en" \
	--metadata rights="Copyleft" \
	--metadata date="`date +'%Y-%m-%d'`" \
	--toc
```

### DOCX -> PDF

```
pandoc -i file.docx -o file.pdf
```

Để chuyển sang PDF thì cần có `pdf-latex` gì đó nên mình gợi ý tải LibreOffice.


### EPUB -> Markdown

```
pandoc input.epub -t gfm -o output.md --extract-media=./img --standalone --wrap=none
```