#---------------------------------------------------------------------
#
#  Author: D. Pereira
#
#=====================================================================



import sys
import re

#In order to add new features: 
#  (i)    Create new function def, FUNC 
#  (ii)   Add feature type in featureType() dict
#             ex. 'NAME':'numeric', or 'NAME': '{yes, no}'
#  (iii)  Edit featureFunctions() with new function call, 
#         {'NAME': FUNC}

def featureType(feat):
    #Returns the feature's arff type

    types = {'first_person_prns':'numeric', 'sec_person_prns':'numeric',
            'third_person_prns': 'numeric', 'conjs':'numeric', 
            'past_verbs':'numeric', 'future_verbs':'numeric', 'caps':'numeric', 
            'commas':'numeric', 'cols_semicols':'numeric', 'slangs':'numeric', 
            'dashes':'numeric', 'parens':'numeric', 'ellipses':
            'numeric', 'comm_nouns':'numeric', 'prop_nouns':'numeric',
            'adverbs':'numeric', 'wh_words':'numeric', 'avg_tok_lens':
            'numeric', 'avg_sent_lens':'numeric', 'numSents':'numeric'} 
    
    return types[feat]

def featureFunctions():
    #Dictionary of {feature_name: function_name} pairs
    
    return {'first_person_prns': get_first_person_prns, 'sec_person_prns': 
            get_sec_person_prns, 'third_person_prns': get_third_person_prns, 
            'conjs': get_conjs, 'past_verbs': get_past_verbs, 'future_verbs': 
            get_future_verbs, 'commas': get_commas, 'cols_semicols': 
            get_cols_semicols, 'dashes': get_dashes, 'parens': get_parens, 
            'ellipses': get_ellipses, 'comm_nouns': get_comm_nouns,             
            'prop_nouns': get_prop_nouns, 'adverbs': get_adverbs, 'wh_words': 
            get_wh_words, 'slangs': get_slangs, 'caps': get_caps, 
            'avg_tok_lens': get_avgTokLen, 'avg_sent_lens': get_avg_sent_lens, 
            'numSents': get_sent_count}

def extraFunctions():
    return [] 
  
    #return {'newname':new_function, ... etc}


#FEATURE DEFINITIONS

def get_first_person_prns(tw):    
    pattern = '\s(I|me|my|mine|we|us|our|ours)\/PRP'
    matches = re.findall(pattern, tw, re.IGNORECASE)
    return len(matches)

def get_sec_person_prns(tw):   
    pattern = '\s(you|your|yours|u|ur|urs)\/PRP'
    matches = re.findall(pattern, tw, re.IGNORECASE)
    return len(matches)
    
def get_third_person_prns(tw):
    pattern = '\s(he|him|his|she|her|hers|it|its|they|them|their|theirs)\/PRP'
    matches = re.findall(pattern, tw, re.IGNORECASE)
    return len(matches)
   
def get_conjs(tw):
    pattern = '\/conjs\s'
    matches = re.findall(pattern, tw, re.IGNORECASE)
    return len(matches)
   
def get_past_verbs(tw):
    pattern = '\/VBD\s'
    matches = re.findall(pattern, tw, re.IGNORECASE)
    
    return len(matches)
   
def get_future_verbs(tw):
    pat1 = '[\w]+\/VBG\s[\w]+\/TO\s[\w]+\/VB\s?'
    pat2 = 'will\/MD\s[\w]+\/VB\s?'
    pat3 = 'will\/MD\s[\w]+\/PRP\s[\w]+\/VB\s?'
    
    m1 = re.findall(pat1, tw)    
    m2 = re.findall(pat2, tw)    
    m3 = re.findall(pat3, tw)    
    
    return sum([len(m1), len(m2), len(m3)])

def get_commas(tw):
    pattern = '\/,'
    matches = re.findall(pattern, tw, re.IGNORECASE)
    
    return len(matches)

def get_cols_semicols(tw):
    pattern = '(:|;)\/:\s?'
    matches = re.findall(pattern, tw, re.IGNORECASE)
    return len(matches)

def get_dashes(tw):
    pattern = '\/-\s'
    matches = re.findall(pattern, tw, re.IGNORECASE)
    return len(matches)

def get_parens(tw):
    pattern = '\/(\(|\)|{|}|[|])'
    matches = re.findall(pattern, tw, re.IGNORECASE)
    return len(matches)

def get_ellipses(tw):
    pattern = '.../:'
    matches = re.findall(pattern, tw, re.IGNORECASE)
    return len(matches)

def get_comm_nouns(tw):
    pattern = '\/(NN|NNS)\s'
    matches = re.findall(pattern, tw, re.IGNORECASE)
    return len(matches)

def get_prop_nouns(tw):
    pattern = '\/(NNP|NNPS)\s'
    matches = re.findall(pattern, tw, re.IGNORECASE)
    return len(matches)

def get_adverbs(tw):
    pattern = '\/(RB|RBR|RBS)\s'
    matches = re.findall(pattern, tw, re.IGNORECASE)
    return len(matches)

def get_wh_words(tw):
    pattern = '\/(WTD|WP|WP$|WRB)\s'
    matches = re.findall(pattern, tw, re.IGNORECASE)
    return len(matches)

def get_slangs(tw):
    slwords = '|'.join('smh, fwb, lmfao, lmao, lms, tbh, ro, \
    wtf, bff, wyd, lylc, brb, atm, imao, sml, btw,bw, imho, \
    fyi, ppl, sob, ttyl, imo, ltr, thx, kk, omg, ttys, afn, \
    bbs, cya, ez, f2f, gtr, ic, jk, k, ly, ya, nm, np, plz, \
    ru, so, tc, tmi, ym, ur, u, sol'.split(', '))
    
    pattern = '\s(' + slwords + ')\s'
    matches = re.findall(pattern, tw, re.IGNORECASE)
    return len(matches)

def get_caps(tw):
    #At least two capitals in a row
    pattern = '\s[A-Z][A-Z]+'
    matches = re.findall(pattern, tw)
    return len(matches)

def get_avg_sent_lens(tw):
    sents = tw.split('\n')
    lengths = []
    
    #List of sentence lengths 
    for s in sents:
        lengths.append(len(s.split()))
        
    res = 0
    if len(sents) != 0: res = sum(lengths)/ (len(sents) + 0.0)

    return res

def get_avgTokLen(tw):
    #Find all tagged tokens that are not punctuation
    
    pattern = '\/[\w]+'
    temp = re.sub(pattern, '', tw)
    
    matches = re.findall('[\w]+', temp)

    #Sum of the list of token lengths / total tokens 
    res = 0
    if len(matches) != 0: res = sum(list(map(len, matches))) / (len(matches) + 0.0)

    return res

def get_sent_count(tw):  
    s = tw.split('\n')    
   
    return len(s)
    
if (len(sys.argv) < 3) or (sys.argv[1].startswith('-') and len(sys.argv) < 3):
    print 'Usage: ' + sys.argv[0] + ' [-limit] class1 .. classN outputfile'

else:
    limit = -1
    classes = {}
    outputfile = sys.argv[-1]
    
    sent_count = 0
    tokCounts = 0
    tokLen = 0

    #iterate through and extract arguments
    
    for i in range(len(sys.argv))[1:]:
        
        #check if first arg is the numtweets indicator
        if (i == 1) and (sys.argv[i].startswith('-')):
            limit = int(sys.argv[i][1:])
               
        #append another class name
        else:
            cla = sys.argv[i]
              
            #set class name, files list
            temp = cla.split(':')
            name = temp[0]
            
            files = []                      
            
            if len(temp) == 1:
                files = temp[0].split('+')
            else:
                files = temp[1].split('+')            
             
            classes[name] = files   
    
    
    #SET UP arff FILE TEXT 

    arff = '@relation ' + outputfile + '\n\n'
            
    for feat in featureFunctions():
        arff = arff + '@attribute {!s} {!s}\n'.format(feat, featureType(feat))
    
    for feat in extraFunctions():
        arff = arff + '@attribute {!s} {!s}\n'.format(feat, featureType(feat))
       
    C = [item for item in classes.keys() if item not in [outputfile]]
    
    cls = ','.join(C)
    
    arff = arff + '@attribute twit {!s}\n\n'.format('{' + cls + '}')
        
    arff = arff + '@data\n'
           
    
    #Process information, build attribute relation
    for cla in C:
        #For each class, iterate over files]
        classname = cla
        files = classes[cla]
        
        #Build attribute relation for each file
        
        for f in files: 
            
            file = open(f, 'r')
            
            data = file.read().split('|')[1:-1]
            
            count = 0
            
            while ((count < len(data)) and (count != limit)):
                #Extract features for tweet 
                d = data[count].strip()
                
                #ignore blank tweets
                #if (len(d)>0):                  
                
                line = []
                
                #Call feature functions aconjsordingly
                for feat in featureFunctions().keys():
                    line.append(str(featureFunctions()[feat](d)))
               
                if len(extraFunctions()) > 0:
                    for feat in extraFunctions().keys():
                        line.append(str(extraFunctions()[feat](d)))

                arff = arff + ','.join(line) + ',' + classname + '\n'
                
                               
                count = count + 1
                
            file.close()
        
        
    #CREATE, WRITE TO arff FILE
    
    f = open(outputfile, 'w+')
    f.write(arff)
    
    f.close()
    
      
