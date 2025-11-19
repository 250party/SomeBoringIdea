import re

def has_invalid_filename_chars(filename):
    # Windows文件名非法字符：\ / : * ? " < > |
    pattern = r'[\\/:*?"<>|]'
    return bool(re.search(pattern, filename))

if __name__=='__main__':
    test_filenames = [
        "正常文件名.txt",
        "file:name.jpg",
        "my<file>.doc",
        "path/name.pdf",
        "good_file.txt"
    ]

    for name in test_filenames:
        if has_invalid_filename_chars(name):
            print(f"'{name}' 包含非法字符")
        else:
            print(f"'{name}' 是合法的文件名")