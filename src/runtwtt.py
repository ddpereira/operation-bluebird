#---------------------------------------------------------------------
#
#  Author: D. Pereira
#
#=====================================================================


import sys
import re
import NLPlib
        
def process(filename):
     
    f = open('/u/cs401/A1/tweets/' + filename, 'r')
    text = f.read().split('\n')
    
    processedText = []
    
    for t in text:
        
        #Replace fixed pattern html character codes with ASCII                    
        t = replaceHtmlCode(t)
        
        #Strip html tags                    
        t = stripHtml(t)
        
        #Strip urls
        t = removeUrl(t)
        
        #Mark sentence boundaries within tweet
        t = markBoundaries(t)
        
        #Preprocess the tweets to remove non-alphanumeric characters ex. extract 
        #meaningful words
        t = removeHandleAndHashtag(t)        
        
        t = separateTokens(t)
        
        processedText.append(t)
        
    f.close()    
    return processedText

def postag(text, outputfile):
    #Tag the tokens in each tweet with a PoS indicator
    
    processedText = '|\n'
    
    tagger = NLPlib.NLPlib()
    
    #process each tweet
    for x in text:
        sentences = re.split('\n', x) 
        
        #process each sentence in the tweet
        for sent in sentences:            
            s = re.split('\s+', sent)
            tags = tagger.tag(s)
        
            
            for t in range(len(s)):
                processedText = processedText + s[t] +'/' + tags[t] + ' '
            
            processedText = processedText + '\n'
                        
        processedText = processedText + '|\n'
      
    #Print tagged text to output file
     
    f = open(outputfile, 'w+')
    f.write(str(processedText))    
    
    f.close()
    
    return processedText

def replaceHtmlCode(text):
    htmlCodes = {'&amp;':'&', '&quot;':'"', '&#39':"'", '&lt;':'<', '&gt;':'>'}
    
    for h in htmlCodes:
        text = text.replace(h, htmlCodes[h])
             
    return text    

def removeHandleAndHashtag(text):
    pattern = '(@|#)'
    return re.sub(pattern, '', text)

def removeUrl(text):
    pat1 = '(https?://([-\w\.]+)+(:\d+)?(/([\w/_\.]*(\?\S+)?)?)?)'
    pat2 = '[\w]+[\..+][\w]+'
    
    temp = re.sub(pat1, '', text, re.IGNORECASE)
    return re.sub(pat2, '', temp, re.IGNORECASE)

def stripHtml(text):
    pattern = '<.+?>'
    return re.sub(pattern, '', text)

def markBoundaries(text):
    #Naive boundary marker; ignores many cases of abbreviations
    abbreviations = open('A1/abbrev.english', 'r').read()
    abbrev = abbreviations.replace('.', '').split('\n ')
    
    for a in abbrev:
        abbreviations = '|[' + a + ']'

    abbreviations = abbreviations[1:]

    pattern = '(?<!' + abbreviations + ')\.'

    return re.sub(pattern, '\\n', text)

def separateTokens(text):
    
    tokens = ['\.', '\(', '\)', '\/', ':', ';', '\?', '\!', 
              ',', '\'', '"', '-', '\$', '&', '\*']
    
    for t in tokens:
       #separate punctuation (preserves ellipses & other repeated punctuation)
        m1 = re.findall(t + '+\w*', text)
        
        for m in m1: 
            if (m): text = re.sub(t + '+', ' ' + m + ' ', text) 
      
    return text.strip()
    
files = ['aplusk', 'BarackObama', 'bbcnews', 'britneyspears', 'CBCNews', 
        'cnn', 'justinbieber', 'katyperry', 'KimKardashian', 'ladygaga',
        'neiltyson', 'nytimes', 'Reuters', 'rihanna', 'sciencemuseum',
        'shakira', 'StephenAtHome', 'taylorswift13', 'TheOnion', 'torontostarnews']
      
for f in files:
    processedText = postag(process(f), f + '_out.twt') 
  

#SOURCES:
#
# URL regex:
# http://rushi.wordpress.com/2008/04/14/simple-regex-for-matching-urls/
            
