import re
link = "comment.php?BOARD_ID=32&amp;COMMENT_ID=58472&amp;PAGE_START=61"

m = re.match('.*?COMMENT_ID=(.*?)\&.*?',link)
print(m.group(1))
