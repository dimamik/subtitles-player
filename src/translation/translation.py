from textblob import TextBlob

blob = TextBlob("text to translate")
print(blob.translate(to='pl'))
