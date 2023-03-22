import jieba.posseg as peg
def userinput_word_splitter(userinput):
    splited_wrds = []
    for line,flag in peg.cut(userinput, True):
      wrd_pty_mk = "%s" % (line)
      splited_wrds.append(wrd_pty_mk)
    return splited_wrds