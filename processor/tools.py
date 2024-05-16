def sort_list_by_another_list(list_to_sort, ref_list):
    inds   = [ind for _,ind in sorted(zip(ref_list, list(range(len(list_to_sort)))))]
    result = [list_to_sort[ind] for ind in inds]
    return result