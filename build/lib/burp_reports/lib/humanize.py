
def humanize_file_size(size):
    # It will be used on some prints of text for size representation.
    import math
    size = abs(size)
    if size == 0:
        return "0B"
    units = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']
    p = math.floor(math.log(size, 2) / 10)
    return "%.3f%s" % (size / math.pow(1024, p), units[int(p)])
