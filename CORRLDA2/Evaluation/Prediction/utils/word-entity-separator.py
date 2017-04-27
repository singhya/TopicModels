import sys
import entityUtils


def main():
    sample_file = sys.argv[1]
    op_entity_file = "op-ents.txt"
    op_word_file = "op-word.txt"
    with open(sample_file, "r") as src, open(op_entity_file, "w") as ent_fo, open(op_word_file, "w") as word_fo:
        for line in src:
            ents, words = entityUtils.process_article(line)
            ent_fo.write("{}\n".format(" ".join(ents)))
            word_fo.write("{}\n".format(" ".join(words)))
main()
