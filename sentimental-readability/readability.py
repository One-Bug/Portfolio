from cs50 import get_string

text = get_string("Text: ")
letters = 0
sentences = 0
words = 1
for c in text:
    if c.isalpha():
        letters += 1
    elif c.isspace():
        words += 1
    elif c in ["!", ".", "?"]:
        sentences += 1
l = letters / words * 100
s = sentences / words * 100
index = round(0.0588 * l - 0.296 * s - 15.8)
if index < 1:
    print("Before Grade 1")
else:
    if index >= 1 and index <= 16:
        print(f"Grade {index}")
    else:
        print("Grade 16+")
