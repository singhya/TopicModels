# module containing functions to return string after replacing certain characters as specified in definition

import re


# replace all English characters and numerals using regex
def repl_char_nums_en(txt):
    return re.sub(r'[a-zA-Z0-9]', r' ', txt)


# replace nusable characters with null character or 1 blank space
# characters replaced: ! & : ( ) / ' ` _ # $ @ ^ % ~ + = " - [ ] \
# other Unicode code points removed:
# 00A0 -no-break-space -> null
# 200B - zero-width-non-joiner -> null
# 200C - zero-width-space -> null
# 2013 - en dash -> null
# 2014 - em dash -> null
# 2018 - quotation mark -> space
# 2019 - quotation mark -> space
# 201C - double quotation mark -> space
# 201D - double quotation mark -> space
# 20B9 - rupee symbol -> space
# 00D7 - multiplication sign -> space
# 2032 - prime -> space
# 2022 - bullet -> space
# 2010 - hyphen -> space
# 00B7 - middle dot -> space
# 2026 - ellipsis -> space
# 0970 - devanagari abbreviation sign  -> space
# 2605 - black star -> space
# FEFF - zero width no break space -> space
# 30FB - katakana middle dot -> space
def repl_unusable_chars(line):
    line = re.sub(r"[.!&:()/'`_#$@^%~+=<>\"\-\[\]\\]", r' ', line)
    line = line.decode('utf-8').replace(u'\u00A0', '').encode('utf-8')
    line = line.decode('utf-8').replace(u'\u200B', '').encode('utf-8')
    line = line.decode('utf-8').replace(u'\u200C', '').encode('utf-8')
    line = line.decode('utf-8').replace(u'\u2013', '').encode('utf-8')
    line = line.decode('utf-8').replace(u'\u2014', '').encode('utf-8')
    line = line.decode('utf-8').replace(u'\uFEFF', '').encode('utf-8')

    line = line.decode('utf-8').replace(u'\u2018', ' ').encode('utf-8')
    line = line.decode('utf-8').replace(u'\u2019', ' ').encode('utf-8')
    line = line.decode('utf-8').replace(u'\u201C', ' ').encode('utf-8')
    line = line.decode('utf-8').replace(u'\u201D', ' ').encode('utf-8')
    line = line.decode('utf-8').replace(u'\u20B9', ' ').encode('utf-8')
    line = line.decode('utf-8').replace(u'\u00D7', ' ').encode('utf-8')
    line = line.decode('utf-8').replace(u'\u2032', ' ').encode('utf-8')
    line = line.decode('utf-8').replace(u'\u2022', ' ').encode('utf-8')
    line = line.decode('utf-8').replace(u'\u2010', ' ').encode('utf-8')
    line = line.decode('utf-8').replace(u'\u00B7', ' ').encode('utf-8')
    line = line.decode('utf-8').replace(u'\u2026', ' ').encode('utf-8')
    line = line.decode('utf-8').replace(u'\u0970', ' ').encode('utf-8')
    line = line.decode('utf-8').replace(u'\u2605', ' ').encode('utf-8')
    line = line.decode('utf-8').replace(u'\u30FB', ' ').encode('utf-8')

    # devanagari digits
    line = line.decode('utf-8').replace(u'\u0966', ' ').encode('utf-8')
    line = line.decode('utf-8').replace(u'\u0967', ' ').encode('utf-8')
    line = line.decode('utf-8').replace(u'\u0968', ' ').encode('utf-8')
    line = line.decode('utf-8').replace(u'\u0969', ' ').encode('utf-8')
    line = line.decode('utf-8').replace(u'\u096a', ' ').encode('utf-8')
    line = line.decode('utf-8').replace(u'\u096b', ' ').encode('utf-8')
    line = line.decode('utf-8').replace(u'\u096c', ' ').encode('utf-8')
    line = line.decode('utf-8').replace(u'\u096d', ' ').encode('utf-8')
    line = line.decode('utf-8').replace(u'\u096e', ' ').encode('utf-8')
    line = line.decode('utf-8').replace(u'\u096f', ' ').encode('utf-8')

    doc_content = " ".join(line.split())
    return doc_content


def starts_with_matra(word):
    matras_unicode_points = [
        u'\u0901', u'\u0902', u'\u0903', u'\u093a', u'\u093b', u'\u093c',
        u'\u093e', u'\u093f', u'\u0940', u'\u0941', u'\u0942', u'\u0943',
        u'\u0944', u'\u0945', u'\u0946', u'\u0947', u'\u0948', u'\u0949',
        u'\u094a', u'\u094b', u'\u094c', u'\u094d', u'\u094e', u'\u094f',
        u'\u0951', u'\u0952', u'\u0953', u'\u0954', u'\u0955', u'\u0956',
        u'\u0957', u'\u0962', u'\u0963'
    ]
    decoded = word.decode('utf-8')
    if decoded[0] in matras_unicode_points:
        return True
    else:
        return False
