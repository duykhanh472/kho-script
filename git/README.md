# Học Git

## Cơ bản (Local)

### Tạo thư mục

Tạo một thư mục rồi `cd thư_mục/`:

```
user@user:~$ cd Downloads/learn-git-repo/
```

### `git init`

Khởi tạo `git` trong thư mục hiện tại (Muốn biết thì `pwd`)

```
user@user:~/Downloads/learn-git-repo$ git init
hint: Using 'master' as the name for the initial branch. This default branch name
hint: is subject to change. To configure the initial branch name to use in all
hint: of your new repositories, which will suppress this warning, call:
hint: 
hint: 	git config --global init.defaultBranch <name>
hint: 
hint: Names commonly chosen instead of 'master' are 'main', 'trunk' and
hint: 'development'. The just-created branch can be renamed via this command:
hint: 
hint: 	git branch -m <name>
Initialized empty Git repository in /home/user/Downloads/learn-git-repo/.git/
```

### Tạo tệp + `git add` + `git commit`

- `git add` để thêm tệp vào trong danh sách tệp sẽ được `commit`.
- `git commit` để tạo một phiên bản mới cho kho code. Nhanh hơn nữa là `git commit -am` (Cả `add` và `commit`)

```
user@user:~/Downloads/learn-git-repo$ touch README.md
user@user:~/Downloads/learn-git-repo$ git add *
user@user:~/Downloads/learn-git-repo$ git commit -m "Initial commit"
[main (root-commit) 53eb1b8] Initial commit
 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 README.md
```

### Tạo một nhánh (branch) mới

Gõ `git branch [tên nhánh]` để tạo nhánh mới nhé.

```
user@user:~/Downloads/learn-git-repo$ git branch temp_branch

user@user:~/Downloads/learn-git-repo$ git branch
* main
  temp_branch

user@user:~/Downloads/learn-git-repo$ git switch temp_branch
Switched to branch 'temp_branch'
```

Bạn cũng có thể dùng `git checkout -b` để tạo một nhánh mới cũng như di chuyển qua nhánh đó:

```
user@user:~/Downloads/learn-git-repo$ git checkout -b temp_branch-2
Switched to a new branch 'temp_branch-2'
```

### Đổi tên nhánh: master -> main

Không rõ lắm nhưng mà mình dùng `git` trên Debian 12, nó có thể là bản `git` cũ quá nên vẫn mặc định nhánh mới khởi tạo là `master`, giờ mình muốn đổi qua `main` thì có thể chạy lệnh sau:

```
user@user:~/Downloads/learn-git-repo$ git branch -m main
```

Mẹo hay phết: `git checkout -` để chuyển về branch mình mới làm việc trước đó.

### merge branch to main

### Checkout to older version 

Thử nghiệm chút. Đây là phần thông tin hiện tại (Mình đã cập nhật tệp `README.md` sau khi commit cái "Initial commit"):

```
user@user:~/Downloads/learn-git-repo$ vim README.md

user@user:~/Downloads/learn-git-repo$ git log
commit 53eb1b856acb04735d9fb60dc2037039c60ee7dd (HEAD -> main, origin/main, temp_branch)
Author: Khanh Duy <user@email.com>
Date:   Thu Jun 11 16:27:15 2026 +0700

    Initial commit
```

Tạo nhanh một phiên bản code mới:

```
user@user:~/Downloads/learn-git-repo$ git add *

user@user:~/Downloads/learn-git-repo$ git commit -m "second version"
[main ac5035d] second version
 1 file changed, 2 insertions(+)
```

Giờ kiểm tra Output của `git log`

```
user@user:~/Downloads/learn-git-repo$ git log
commit ac5035da17acf3cf2b436d4e1961d92ba6589e7e (HEAD -> main)
Author: Khanh Duy <user@email.com>
Date:   Thu Jun 11 16:32:34 2026 +0700

    second version

commit 53eb1b856acb04735d9fb60dc2037039c60ee7dd (origin/main, temp_branch)
Author: Khanh Duy <user@email.com>
Date:   Thu Jun 11 16:27:15 2026 +0700

    Initial commit
```

Giờ để trở lại phiên bản code ban đầu (Cái có comment: "Initial commit") thì mình sẽ chạy `git checkout` cộng với mã commit (Cái đoạn `53eb1b8...` sau chữ `commit ` á):


``` 
user@user:~/Downloads/learn-git-repo$ git checkout 53eb1b856acb04735d9fb60dc2037039c60ee7dd
Note: switching to '53eb1b856acb04735d9fb60dc2037039c60ee7dd'.
user@user:~/Downloads/learn-git-repo$ 
```

### Xử lý conflict như thế nào?

(Đang học)

## Nghịch ngợm với remote

### Đẩy code lên remote

(Mình đã thực hiện `add` và `commit` ở trên nên ở đây chỉ tập trung vào giai đoạn thêm `remote` và `push` lên `remote` thôi)

Remote về cơ bản là mấy cái kiểu Github, Gitlab á. Vì tụi mình vừa mới tạo repo bằng `git init` nên nó sẽ vẫn chưa có `remote repo` (Bạn có thể hiểu là để gửi hàng cho khách thì cần phải có địa chỉ nhà của họ ấy. Để gửi code lên remote thì phải có địa chỉ trên cái remote đó. Mong là nó dễ hiểu). Thì đầu tiên cần thêm cái địa chỉ đó (Bạn vào Github hay gì đó rồi chọn cái New Repository, nhập thông tin và rồi sẽ có một cái đường dẫn có đuôi `.git` ở cuối, bạn sao chép cái đó rồi chạy lệnh `git remote add origin` + cái URL đó như hình dưới đây. Ở đây mình dùng Codeberg):

```
user@user:~/Downloads/learn-git-repo$ git remote add origin https://codeberg.org/user1/learn-git.git
```

Rồi sau đó đẩy lên bằng lệnh `push`:

```
user@user:~/Downloads/learn-git-repo$ git push -u origin main

Enumerating objects: 3, done.
Counting objects: 100% (3/3), done.
Writing objects: 100% (3/3), 220 bytes | 220.00 KiB/s, done.
Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
To https://codeberg.org/user1/learn-git.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

Trên thực tế thì bạn có thể chỉ cần gõ `git push` cũng được, nhưng để cho mọi thứ được rõ ràng và tường minh, hãy có một thói quen là ghi đầy đủ ra kiểu như thế này:

```
git push -u origin main
# Trong trường hợp đây là nhánh mới thì bạn nên thêm `--set-upstream` vào nữa nhé
git push -u origin new_feature  --set-upstream
```

### Merge (`pull origin` rồi `push`)

...

### Conflict

(Chưa học)

## Nâng cao hơn một chút

### `git stash`

Đại khái về trường hợp. Trong trường hợp mà code mình chưa muốn "commit" nhưng không lỡ bỏ. Bỏ thì thương và vương thì tội.

```
# Để in ra đống thay đổi trong code
git diff
# Xong rồi thử chạy git stash
git stash
git stash save "Tên là gì"
git stash list
# Cái này là để trở về này
git stash pop
```

### Một mẹo hay liên quan đến `git add`

Bình thường mình hay có thói quen `git add .` để thêm toàn bộ. Nhưng thay vào đó, ta có thể chạy lệnh `git add -p`, nó sẽ hiện thay đổi của từng tệp và yêu cầu mình xác nhận.

Lưu ý là tệp đó đã phải được tạo từ các commit trước. Bạn có thể thử xem ví dụ ở dưới đây:


```
user@user:~/Downloads/hocgit$ git add -p
diff --git a/LICENSE b/LICENSE
index 8a33339..4ee9f76 100644
--- a/LICENSE
+++ b/LICENSE
@@ -1 +1,3 @@
-Unlicense
\ No newline at end of file
+Unlicense
+
+Update
\ No newline at end of file
(1/1) Stage this hunk [y,n,q,a,d,e,?]? n

diff --git a/README.md b/README.md
index 0f999a0..ff5dbc8 100644
--- a/README.md
+++ b/README.md
@@ -186,4 +186,8 @@ git stash pop
 
### Một mẹo hay liên quan đến `git add`
 
-Bình thường mình hay có thói quen `git add .` để thêm toàn bộ. Nhưng thay vào đó, ta có thể chạy lệnh `git add -p`, nó sẽ hiện thay đổi của từng tệp và yêu cầu mình xác nhận.
\ No newline at end of file
+Bình thường mình hay có thói quen `git add .` để thêm toàn bộ. Nhưng thay vào đó, ta có thể chạy lệnh `git add -p`, nó sẽ hiện thay đổi của từng tệp và yêu cầu mình xác nhận.
+
+Lưu ý là tệp đó đã phải được tạo từ các commit trước.
+
+Giả sử mình thêm hai tệp `TMP1.md` và `TMP2.md`.
\ No newline at end of file
(1/1) Stage this hunk [y,n,q,a,d,e,?]? y
```

Kiểm tra kĩ từng tệp mình đã thay đổi để tránh để lọt "tội phạm bug" bất kì. Trong trường hợp bạn chọn `n` thì khi `commit`, những thay đổi của các tệp bạn chọn `n` sẽ không được thêm vào trong phiên bản code được commit lần này.

### hủy cái commit

Trong trường hợp mình lỡ commit và muốn hủy bỏ commit đó?

```
git reset --soft HEAD~1
```

(Cái 1 đó là lùi về một commit thôi không có gì đâu)

Một cái lưu ý nữa là chỉ `reset` được khi làm việc trên máy của bạn thôi. Chứ `push` rồi thì phải `revert`.  
Mình thử nghịch thì thấy là `reset` này chỉ xóa commit thôi, chứ nội dung lúc bạn sửa trước khi commit vẫn sẽ được giữ nhé, cái này khác `revert` ở chỗ đấy.
