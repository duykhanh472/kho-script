# Một số câu lệnh tải video hay bằng `yt-dlp`

### Chỉnh sửa tên tệp (Output)
Khi tải video Youtube chẳng hạn, thường thì nó sẽ trả về kiểu `Tiêu đề video [id của video].webm` chẳng hạn. Nó khá là khó chịu =)) (Ít nhất với mình).

```
yt-dlp -o "%(title)s.%(ext)s" [link ở đây]
```
Thường là mình để mặc định thế này, chỉ có tiêu đề với đuôi tệp thôi.

### Tải cả cái Podcast
Lên trên [Podcastindex.org](https://podcastindex.org/) và tìm Podcast bạn muốn tải. Ví dụ mình sẽ tải Podcast có đường dẫn là [https://podcastindex.org/podcast/366334](https://podcastindex.org/podcast/366334).

Bạn chỉ cần bấm **Copy RSS** rồi ném vào trong `yt-dlp` là xong:

```
yt-dlp https://feeds.simplecast.com/dfh_verV
```

Rồi nó sẽ tải toàn bộ cho bạn.


### Danh sách các lệnh tổng hợp
Tải một danh sách phát trên Youtube, độ phân giải 480p, có phụ đề Tiếng Anh với Output tên đẹp đẹp xíu.

```
yt-dlp -S res:480 --write-subs --write-auto-subs --sub-lang=en --convert-subs=srt -o "%(title)s.%(ext)s" [Cho link ở đây]
```

Giải thích thêm:

- `-S res:480`: Độ phân giải 480p.
- `--write-subs`
- `--write-auto-subs`: Tải sub tự Youtube tạo 
- `--sub-lang=en`: Chọn ngôn ngữ phụ đề
- `--convert-subs=srt`: Chuyển đổi sang định dạng `.srt`, mặc định `yt-dlp` sẽ dùng `.vtt`
- `-o "%(title)s.%(ext)s"` - Tên tệp đẹp


#### Other

#### Download whole channel

`yt-dlp -f best -ciw -o "%(title)s.%(ext)s" -v https://www.youtube.com/channel/ABC123`

#### Download portion of video

`yt-dlp --postprocessor-args "-ss HH:MM:SS -to HH:MM:SS" "video_URL"`

#### Audio only

`yt-dlp -i --extract-audio --audio-format mp3 video_URL`

Hoặc 

`yt-dlp -f m4a video_URL`
#### Download as mp4

`yt-dlp -S res,ext:mp4:m4a --recode mp4 "video_URL"`

### Archive

I also suggest this. Basically just make your liked videos playlist public and give the url to yt-dlp. I also suggest adding the option --download-archive archive.txt, which tells it to remember which videos were already downloaded so you can run it again at a later time and only download new stuff. --all-subs --embed-subs --embed-metadata --merge-output-format mkv if you want to grab all the subs and metadata too and embed then.


```
--download-archive archive.txt
```