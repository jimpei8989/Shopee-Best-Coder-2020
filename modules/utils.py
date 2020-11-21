from itertools import product

from .box import Box
from .sku import SKU

def stack_skus(boxes, skus):
    stacked_skus = sum(skus, start=SKU())
    return find_optimal_box(boxes, stacked_skus)

def stack_skus_with_rotation(boxes, skus):
    best_box = None
    for possible_order in product(*(sku.all_rotations() for sku in skus)):
        tmp_box = stack_skus(boxes, possible_order)

        if tmp_box is None:
            continue

        if best_box is None:
            best_box = tmp_box
        elif tmp_box < best_box:
            best_box = tmp_box

    return best_box

def greedy_way(boxes, skus):
    t_skus = [sku.copy() for sku in skus]

    while len(t_skus) > 1:
        t_skus.sort()
        a, b = t_skus[:2]
        t_skus = t_skus[2:] + [a + b]

    return find_optimal_box(boxes, t_skus[0])


def find_optimal_box(boxes, sku):
    for box in boxes:
        if box.can_place(sku):
            return box

    return None

