import sys
import re
import NLPlib
       
def process(filename):
    
    f = open(filename, 'r')
    
    #Separate the tweets, which are stored one per line 
    text = f.read().split('\n')
    
    #List will temporarily store each procsesed tweet of the twt file
    processedText = []
    
    #Pre-process each tweet
    for t in text:
        
        #Replace fixed pattern html character codes with ASCII                  
        t = replaceHtmlCode(t)
        
        #Strip html tags                    
        t = stripHtml(t)
        
        #Strip all urls
        t = removeUrl(t)
        
        #Mark sentence boundaries within tweet
        t = markBoundaries(t)
        
        #Remove twitter handles and hasthtags (ie. @ and #)
        t = removeHandleAndHashtag(t)        
        
        #Insert spaces between the processed tokens
        t = separateTokens(t)
        
        processedText.append(t)
        
    f.close()    
    return processedText

def postag(text, outputfile):
    #Tag the tokens in each tweet with a PoS indicator
    
    processedText = '|\n'
    
    tagger = NLPlib.NLPlib()
    
    #Process each tweet
    for x in text:
        sentences = re.split('\n', x) 
        
        #Process each sentence in the tweet
        for sent in sentences:            
            s = re.split('\s+', sent)
            
            #Retrieve tags for each token in the sentence
            tags = tagger.tag(s)
            
            #Suffix each token with the corresponding PoS tag        
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

    #pat1 searches for http patterns  	
    pat1 = '(https?://([-\w\.]+)+(:\d+)?(/([\w/_\.]*(\?\S+)?)?)?)'
    
    #pat2 searches for urls not prefixed by http
    pat2 = '[\w]+[\..+][\w]+'
    
    return re.sub(pat2, '', re.sub(pat1, '', text, re.I), re.I)

def stripHtml(text):
    pattern = '<.+?>'
    return re.sub(pattern, '', text)

def markBoundaries(text):
    #Naive boundary marker; does not account for sentences ending in abbrevs
    abbrevs1 = open('abbrev.english', 'r').read()    
    abbrevs2 = open('pn_abbrev.english', 'r').read()

    abbrevs12 = abbrevs1 + '\n' + abbrevs2

    abbrev = '|'.join(abbrevs12.replace('.','').split('\n '))
    
    abbreviations = ''

    #Construct abbrev pattern
    for a in abbrev:
        abbreviations = '|[' + a + ']'

    abbreviations = abbreviations[1:]

    pattern = '(?<!{!s})\.'.format(abbreviations)
    return re.sub(pattern, '\\n', text)

def separateTokens(text):
    
    tokens = ['\.', '\(', '\)', '\/', ':', ';', '\?', '\!', 
              ',', '\'', '"', '-', '\$', '&', '\*']
    
    for t in tokens:
       #Separate punctuation (preserves ellipses & other repeated punctuation)
        m1 = re.findall(t + '+\w*', text)
        
        for m in m1: 
            if (m): text = re.sub(t + '+', ' ' + m + ' ', text) 
      
    return text.strip()
    

#MAIN
 
tweetfile = ''
outputfile = ''

#Args not correctly supplied
if len(sys.argv) < 3:    
    print 'Usage: ' + sys.argv[0] + ' tweetfile outputfile'
    
else:
    tweetfile = sys.argv[1]
    outputfile = sys.argv[2]
    
    processedText = postag(process(tweetfile), outputfile) 
      


#SOURCES:

# URL regex:
# http://rushi.wordpress.com/2008/04/14/simple-regex-for-matching-urls/
            
