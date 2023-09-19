import tkinter as tk
from textblob import TextBlob
from newspaper import Article

def summarize():
    url = utext.get('1.0','end').strip()
    article = Article(url)

    article.download()
    article.parse()
    text = article.text
    per = 1
    import spacy
    from spacy.lang.en.stop_words import STOP_WORDS
    from string import punctuation
    from heapq import nlargest

#def summarize(text,per):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    tokens = [token.text for  token in doc]
    word_freq = {}
    for word in doc:
        if word.text.lower() not in list(STOP_WORDS):
            if word.text.lower() not in punctuation:
                if word.text not in word_freq.keys():
                    word_freq[word.text]=1
                else:
                    word_freq[word.text] +=1
    max_freq = max(word_freq.values())
    for word in word_freq.keys():
        word_freq[word]=word_freq[word]/max_freq
    sentence_tokens = [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_freq.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent]=word_freq[word.text.lower()]
                else:
                    sentence_scores[sent]+=word_freq[word.text.lower()]
    select_length = int(len(sentence_tokens)*per)
    summar = nlargest(select_length,sentence_scores,key=sentence_scores.get)
    final_summary = [word.text for word in summar]
    summar = ''.join(final_summary)
    #return summary

    title.config(state='normal')
    author.config(state='normal')
    publish.config(state='normal')
    summary.config(state='normal')
    sentiment.config(state='normal')

    title.delete('1.0','end')
    title.insert('1.0',article.title)
    aut = article.authors or 'NA'
    author.delete('1.0','end')
    author.insert("1.0",str(f"{aut}"))
    pub = article.publish_date or 'NA'
    publish.delete('1.0','end')
    publish.insert('1.0',str(f"{pub}"))
    summary.delete('1.0','end')
    summary.insert('1.0',summar)
    analysis = TextBlob(text)
    sentiment.delete('1.0','end')
    sentiment.insert('1.0',f'polarity:{analysis.polarity},sentiment : {"positive" if analysis.polarity >0 else "negative" if analysis.polarity<0 else "neutral"}')


    title.config(state='disabled')
    author.config(state='disabled')
    publish.config(state='disabled')
    summary.config(state='disabled')
    sentiment.config(state='disabled')


    
root = tk.Tk()
root.title("NEWS SUMMARIZER")
root.geometry('1200x600')

tlabel = tk.Label(root,text='Title')
tlabel.pack()

title = tk.Text(root,height=1,width=140)
title.config(state='disabled',bg='#dddddd')
title.pack()

alabel = tk.Label(root,text='Author')
alabel.pack()

author = tk.Text(root,height=1,width=140)
author.config(state='disabled',bg='#dddddd')
author.pack()

plabel = tk.Label(root,text='Publishing Data')
plabel.pack()

publish = tk.Text(root,height=1,width=140)
publish.config(state='disabled',bg='#dddddd')
publish.pack()

slabel = tk.Label(root,text='Summary')
slabel.pack()

summary = tk.Text(root,height=20,width=140)
summary.config(state='disabled',bg='#dddddd')
summary.pack()

selabel = tk.Label(root,text='Sentiment Analysis')
selabel.pack()

sentiment = tk.Text(root,height=1,width=140)
sentiment.config(state='disabled',bg='#dddddd')
sentiment.pack()

ulabel = tk.Label(root,text='url')
ulabel.pack()
utext = tk.Text(root,height=1,width=140)
utext.pack()

btn = tk.Button(root,text="summarize",command=summarize)
btn.pack()


root.mainloop()
