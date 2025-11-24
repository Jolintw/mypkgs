def writer_csv_from_strlists(fullfilepath, strlists, header:str = None, delimiter:str = ","):
    """
    fullfilepath: include filename\n
    strlists: [[str1, ...], [str2, ...], ...]\n
    """
    if header:
        lines = [header]
    else:
        lines = []
    for strs in zip(*strlists):
        line = delimiter.join(strs) + "\n"
        lines.append(line)
    lines[-1] = lines[-1][:-1]
    f = open(fullfilepath, "w")
    f.writelines(lines)
    f.close()
