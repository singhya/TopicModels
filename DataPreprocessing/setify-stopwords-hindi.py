# if new stop words are added to the list, filter out unique ones and update file
import os

original_file = "hindi-stop-words.txt"
updated_file = "hindi-stop-words-new.txt"
with open(original_file, "r") as orig_fo, open(updated_file, "w") as new_fo:
    lines = [line.rstrip() for line in orig_fo]
    stop_words = list(sorted(set(lines)))
    new_fo.write("\n".join(stop_words))

os.remove(original_file)
os.rename(updated_file, original_file)