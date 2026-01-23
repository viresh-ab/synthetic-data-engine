def chunk_list(data, size):
    """Split list into batches"""
    for i in range(0, len(data), size):
        yield data[i:i + size]


def align_lengths(*arrays):
    """Trim all arrays to the same minimum length"""
    min_len = min(len(arr) for arr in arrays)
    return [arr[:min_len] for arr in arrays]
