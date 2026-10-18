# Bash

### Loop đọc từ tệp txt

```bash
while read p; do yt-dlp "$p" -o; done <tmp.txt
```

### Gộp toàn bộ các tệp .txt thành một tệp .txt

```bash

## Nếu không bao gồm sub-folders
cat ./* > merged-file

## Nếu có
find . ! -path ./merged-file -type f -exec cat {} + > merged-file
```

### Tải trang từ Wayback Machine về

```bash
wget -rc --accept-regex '.*https://loda.me/articles.*' "https://web.archive.org/web/20230321225500/https://loda.me/articles"
```

### Sending POST Request using `curl`

```bash
curl -X POST https://localhost:5001/api -H "Content-Type: application/json" -d @/some/directory/some.json
```

### Loop & Tim toan bo cac tep

```bash
find . -name "*.rar" -print0 | while read -d $'\0' file
do
   unrar x "$file"
done

```

### loop cac dong trong tep

```bash
while read p; do papeer get "$p"; done <links.txt
```
### Sort by number
if u want the `ls` output looks like:

```bash
1.md 2.md 3.md 10.md
``` 

instead of

```bash
1.md 10.md 2.md 3.md 
``` 

here is the command

```bash
ls *.md | sort -V | awk '{str=str$0" "}END{sub(/, $/,"",str);print str}'
```


### list all files with a specific string

```bash
ls -c -ltd -- *"Thích Nhất Hạnh"*.txt

mv "$(ls -lt | grep '^-' | head -1 | awk '{ print $9 }')" /abc/home/asd451/Output
```

### HTML to markdown

```
pandoc -f html -t markdown+pipe_tables "$i" -o "${i%.*}.md";
```