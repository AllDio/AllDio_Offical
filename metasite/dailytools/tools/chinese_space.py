def cn_spacer(word):
    spacer_text = ''
    for i in range(len(word)-1):
        if '\u4e00' <= word[i] <= '\u9fff':
            spacer_text += word[i] + ' '
    spacer_text += word[-1]
    return spacer_text