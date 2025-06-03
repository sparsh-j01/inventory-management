from merge_sort import merge_sort

def binary_search_by_id(products, product_id):
    sorted_list = merge_sort(products, key=lambda x: x.product_id)
    left, right = 0, len(sorted_list) - 1
    while left <= right:
        mid = (left + right) // 2
        if sorted_list[mid].product_id == product_id:
            return sorted_list[mid]
        elif sorted_list[mid].product_id < product_id:
            left = mid + 1
        else:
            right = mid - 1
    return None