import os
import ipywidgets as widgets
import tensorflow as tf
from IPython import display
from dragnn.protos import spec_pb2
from dragnn.python import graph_builder
from dragnn.python import spec_builder
from dragnn.python import load_dragnn_cc_impl  # This loads the actual op definitions
from dragnn.python import render_parse_tree_graphviz
from dragnn.python import visualization
from google.protobuf import text_format
from syntaxnet import load_parser_ops  # This loads the actual op definitions
from syntaxnet import sentence_pb2
from syntaxnet.ops import gen_parser_ops
from tensorflow.python.platform import tf_logging as logging
import copy
import pandas as pd
import numpy as np
import glob
import json
import ast
import annotator

segmenter_model = annotator.load_model("data/en/segmenter", "spec.textproto", "checkpoint_new")
parser_model = annotator.load_model("data/en", "parser_spec.textproto", "checkpoint_new")
files = open('Stop.csv')
ss = files.read()
s = ss.split(',')
stop = []
for i in s:
    stop.append(i.strip())


def annotate_text(text):
    sentence = sentence_pb2.Sentence(
        text=text,
        token=[sentence_pb2.Token(word=text, start=-1, end=-1)]
    )

    # preprocess
    with tf.Session(graph=tf.Graph()) as tmp_session:
        char_input = gen_parser_ops.char_token_generator([sentence.SerializeToString()])
        preprocessed = tmp_session.run(char_input)[0]
    segmented, _ = segmenter_model(preprocessed)

    annotations, traces = parser_model(segmented[0])
    assert len(annotations) == 1
    assert len(traces) == 1
    return sentence_pb2.Sentence.FromString(annotations[0]), traces[0]

def TAG(j):
    #print type(j.tag), j.word
    p = j.replace('attribute','')
    p = p.replace('{ ','')
    p = p.replace('value:',':')
    p = p.replace('name:','')
    p = p.strip()
    p = p.replace('}','')
    p = p.replace('    ',',')
    p.strip()
    p = '{'+p+'}'
    #print p
    d = ast.literal_eval(p)
    return d

def get_verb(par):
    
    ver= []
    for j in par.token:
        s = TAG(j.tag)
        if 'VER' in s['fPOS']:
            ver.append(j.word)
    return ver

def get_events(m,verb,ent):

    g = 0
    done = []
    tup = []
    for i,s in enumerate(verb):
        #print s, i
        pred = []
        end = m.find(s+ ' ')+len(s)
        span_subject = m[g:end]

        if i<len(verb)-1:
            end2 = m.find(verb[i+1]+ ' ')+len(verb[i+1])

        else:
            end2 = len(m)-1
        span_object = m[end:end2]
        #print span_object,span_subject, ' GHALLLLLLLLLLLLLLLLLL'
        #print span_subject, s, span_object
        rec = get_s(span_subject,ent,0)
        if rec:
            pred.append(rec)
        pred.append(s)
        #print span_object, 'ONB'
        #print span_object, 'SPANNNNNNNNNN'
        rec = get_s(span_object,ent,1)
        if rec:
            #print span_object,rec
            pred.append(rec)
        #print tuple(pred)
        tup.append(tuple(pred))


        g = end
        #print subm
    return tup
    #print m[g:]

def get_mark(par):
    b = []
    for y in par.token:
        if 'mark' in y.label:
            b.append(y.word)
    return b

def NER(tex):
    included = []
    g = tex.split('. ')

    dicto = {}
    to_be = {}
    words = []
    conj = {}
    final_conj = []
    to_replace = {}
    for m in g:
        dicto = {}
        to_be = {}
        included = []
        conj = {}
        final_conj = []
        to_replace = {}
        if m != '' and m != ' ':
            m = m + '.'
            par,l = annotate_text(m)
            #print "HEREEEEEEEE"
            for i, token in enumerate(par.token):
                #included = []
                #print par.token
                #print token.word, token.label
                if ('ob' in token.label or 'sub' in token.label or 'name' in token.label or 'nmod' in token.label or 'appos' in token.label) and ('csubj' not in token.label):
                    included.append(i)
                    #print token.word, "+++++++++++++="
                    dicto[i] = token.word
                elif 'comp' in token.label or 'flat' in token.label or 'nummod' in token.label:
                    included.append(i)
                    #print token.word
                    if token.head in dicto:
                        dicto[token.head] = dicto[token.head] + " " + token.word
                    else:
                        wor = token.word
                        if i in to_be:
                            wor  = to_be[i] + ' ' + wor 
                        if token.head in to_be:
                            to_be[token.head] = to_be[token.head] + ' ' + wor
                        else:
                            to_be[token.head]=wor
                elif 'conj' in token.label:
                    #print token.head, included, 'CONJ'
                    if token.head in included:
                        val = par.token[token.head]
                        #print val
                        if ('ob' in val.label or 'sub' in val.label or 'name' in val.label or 'nmod' in val.label or 'appos' in val.label) and ('csubj' not in val.label):
                            t = token.head
                        else:
                            t = val.head
                        bl = val.word
                            
                            #print token.word, 'WORDDD'
                        #    dicto[i] = token.word
                        #else: 
                        
                        #print token.word, token.label, val.label, 'VAL CHECK'
                        while 'conj' in val.label:
                            t = val.head
                            #print t, 'CHECKINGGGGGG HEADDD'
                            val = par.token[val.head]
                            bl = val.word
                        #print val.word, 'CHECKING++++++++++++', bl
                        to_replace[i] = copy.deepcopy(bl)
                        conj[i] =  copy.deepcopy(t)
                        #if t in dicto:
                        '''    
                        else:
                            while t not in dicto:
                                t = t.head
                        '''
                        included.append(i)
                                                
            for j in to_be:
                if j in dicto:
                    dicto[j] = to_be[j] + " " + dicto[j]
            for f in dicto:
                if dicto[f].lower() not in stop:
                    words.append(copy.deepcopy(dicto[f]))
            for l in conj:
                rep = to_replace[l]
                #print dicto[l], 'CHECK DICTO', rep
                #print l, 'CHECK DICTO', conj[l], rep, par.token[l].word
                #print dicto.keys()
                #print par.token[conj[l]].word
                if conj[l] in dicto:
                    final_conj.append(dicto[conj[l]].replace(rep,par.token[l].word))
                    #print dicto[conj[l]],'VALUEE'
                else:
                    t = conj[l]
                    while (t not in dicto) and ('root' not in par.token[t].label):
                        t = par.token[t].head
                    if t in dicto:
                        final_conj.append(dicto[t].replace(rep,par.token[l].word))
                    #print dicto[conj[l]],'VALUEE'
                
                '''
                print rep, 'REPEAT',  dicto[l].(rep[0])
                print conj[l], l, 'C CHECK'
                if l > conj[l]:
                    final_conj.append(par.token[conj[l]].word + ' ' + dicto[l])
                else:
                    final_conj.append(dicto[l]+ ' ' + par.token[conj[l]].word)
                '''
                    
           
            #print final_conj
            words.extend(final_conj)
            
            for i in par.token:
                #print i.word, TAG(i.tag)['fPOS'],i.label
                if 'root' in i.label  and 'NOUN' in TAG(i.tag)['fPOS']:
                    words.append(i.word)
                    break
            
    #print final_conj
    return words

    #print token.word, token.label, par.token[token.head].word

