from pickle import load, dump


def merge_appearance_lists(appearance_list_1, appearance_list_2, method="union"):
    """Merge two appearance lists into one following the 'union' method or the 'intersection' method"""
    if method == "union":
        result = set(appearance_list_1)
        result.update(appearance_list_2)
        return sorted(list(result))
    elif method == "intersection":
        result = []
        index1 = 0
        index2 = 0
        n1 = len(appearance_list_1)
        n2 = len(appearance_list_2)
        while index1 < n1 and index2 < n2:
            if appearance_list_1[index1] == appearance_list_2[index2]:
                result.append(appearance_list_1[index1])
                index1 += 1
                index2 += 1
            elif appearance_list_1[index1] > appearance_list_2[index2]:
                index2 += 1
            elif appearance_list_1[index1] < appearance_list_2[index2]:
                index1 += 1
        return result
    else:
        raise ValueError('Invalid method, please set it to "union" or "intersection"')


def load_pickle_file(folder_name, filename):
    return load(open("pickle/{}_{}.p".format(folder_name, filename), "rb"))


def save_pickle_file(folder_name, filename, content):
    target_file = open("pickle/{}_{}.p".format(folder_name, filename), "wb")
    dump(content, target_file)
