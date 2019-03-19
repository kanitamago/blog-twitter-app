import easygui

result = easygui.ynbox("本当に記事を削除してよろしいですか？", "確認", ("削除する", "やっぱやめる"))
print(result)
