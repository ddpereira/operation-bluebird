import sys
import re
import NLPlib.py
   
def process(filename):
    
    f = open(filename, 'r')
    text = f.read().split('\n')
    
    htmlCodes = {'&amp;':'&', '&quot;':'"', '&#39':"'", '&lt;':'<', '&gt;':'>'}
    processedText = []
    
    for t in text:
        
        #Replace fixed pattern html character codes with ASCII                    
        t = replaceHtmlCode(htmlCodes, t)
        
        #Strip html tags                    
        t = stripHtml(t)
        
        #mark sentence boundaries within tweet
        t = markBoundaries(t)
        
        #Preprocess the tweets to remove non-alphanumeric characters ex. extract 
        #meaningful words
        t = removeHandleAndHashtag(t)
        
        t = removeUrl(t)
        
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

def replaceHtmlCode(htmlCodes, text):
    for h in htmlCodes:
        text = text.replace(h, htmlCodes[h])
             
    return text    

def removeHandleAndHashtag(text):
    pattern = '(@|#)'
    return re.sub(pattern, '', text)

def removeUrl(text):
    #pattern = '([0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}|(((news|telnet|nttp|file|http|ftp|https)://)|(www|ftp)[-A-Za-z0-9]*\\.)[-A-Za-z0-9\\.]+)(:[0-9]*)?/[-A-Za-z0-9_\\$\\.\\+\\!\\*\\(\\),;:@&=\\?/~\\#\\%]*[^]\'\\.}>\\),\\\"]'
    
    pattern = '(https?://([-\w\.]+)+(:\d+)?(/([\w/_\.]*(\?\S+)?)?)?)'
                                    
    #pattern = '(http.+\s)|(www.+\s)'
    return re.sub(pattern, '', text)
    
def stripHtml(text):
    pattern = '<.+?>'
    return re.sub(pattern, '', text)

def markBoundaries(text):
    #Naive boundary marker; ignores many cases of abbreviations
    
    pattern = '[!(Mr|Mrs|Ms|Dr|Prof|St)][\.|!|\?] +'
    return re.sub(pattern, '\\n', text)

def separateTokens(text):
    
    tokens = ['.', '(', ')', '/', ':', ';', '?', '!', 
              ',', '\'', '"', '-', '$', '&', '*']
    
    for t in tokens:
        text = text.replace(t, ' ' + t)
      
    return text
    

files = ['aplusk', 'BarackObama', 'bbcnews', 'britneyspears', 'CBCnews', 
        'cnn', 'justinbieber', 'katyperry', 'KimKardashian', 'ladygaga',
        'neiltyson', 'nytimes', 'Reuters', 'rihanna', 'sciencemuseum',
        'shakira', 'StephenAtHome', 'taylorswift13', 'TheOnion', 'torontostarnews']
      
for f in files:
    processedText = postag(process('/h/u5/g1/00/g1nyu/CSC401/A1/A1/tweets' + f), f + '_out') 
  

#SOURCES:
#
# URL regex:
# http://rushi.wordpress.com/2008/04/14/simple-regex-for-matching-urls/
            
