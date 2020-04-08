def merge_posting_lists(posting_list_1, posting_list_2, method="union"):
    """Merge two posting lists into one following the 'union' method or the 'intersection' method"""
    if method == "union":
        result = set(posting_list_1)
        result.update(posting_list_2)
        return sorted(list(result))
    elif method == "intersection":
        return sorted(
            [
                document_id
                for document_id in posting_list_1
                if document_id in posting_list_2
            ]
        )
    else:
        raise ValueError('Invalid method, please set it to "union" or "intersection"')
