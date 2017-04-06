with open("zero-entity-indices.txt", "r") as fo:
    for line in fo:
        index_ctr = 0
        total_lines = 0
        line_comps = line.split()
        fname = line_comps[0]
        indices = [int(index) for index in line_comps[1:]]
        data_fn = "data-dump/data-new-AU/" + fname
        new_data_fn = fname+".updt"
        print "Original file:", fname
        print "Corrupt line index:", indices
        print "No. of corrupt lines:", str(len(indices))
        with open(data_fn, "r") as old_file, open(new_data_fn, "w") as new_file:
            for line_no, each_line in enumerate(old_file):
                try:
                    if line_no != indices[index_ctr]:
                        new_file.write(each_line)
                        total_lines += 1
                    else:
                        if index_ctr < len(indices)-1:
                            index_ctr += 1
                except IndexError:
                    print "final line error: " + str(index_ctr)
            print "Total lines written to {0}: {1}".format(new_data_fn, total_lines)
        print "\n"
