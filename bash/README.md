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

### Generate .epub file using mark2epub

```bash

## Arguments [title]
mkdir docs/
mv links.txt docs/
cd docs/
mkdir css images
while read p; do papeer get "$p"; done <links.txt


## Generate description.json (First init a variable)
description="{\n  \"metadata\": {\n    \"dc:title\": \"$(date +"%Y_%m_%d_%I_%M_%p")\",\n    \"dc:creator\": \"duykhanh471\",\n    \"dc:language\": \"en-US\",\n    \"dc:identifier\": \"\",\n    \"dc:source\": \"\",\n    \"meta\": \"\",\n    \"dc:date\": \"\",\n    \"dc:publisher\": \"\",\n    \"dc:contributor\": \"\",\n    \"dc:rights\": \"\",\n    \"dc:description\": \"\",\n    \"dc:subject\": \"\"\n  },\n  \"cover_image\": \"\",\n  \"default_css\": [],\n  \"chapters\": [\n    "
for file in $( ls *.md ); do
  description="${description}{\n      \"markdown\": \"$file\",\n      \"css\": \"\"\n    },"
done

description="${description::-1}\n  ]\n}"


## Echo the generated content to the new .json file  
echo -e "${description}" > description.json

## Move out of the current directory
cd ..

## Generate an .epub file from markdown files in the docs/ dir
python3 /home/duykhanh471/Applications/mark2epub/script.py docs/ "$(date +"%Y_%m_%d_%I_%M_%p").epub"
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