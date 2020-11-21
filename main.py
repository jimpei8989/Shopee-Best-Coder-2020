from datetime import datetime
from pathlib import Path

from tqdm import tqdm

from modules.box import Box
from modules.sku import SKU
from modules.utils import greedy_way, stack_skus, stack_skus_with_rotation

BOX_CSV = Path('data/box_dimension.csv')
ORDER_CSV = Path('data/order_sku.csv')
SKU_DIMENSION_CSV = Path('data/sku_dimenssion.csv')
ANS_CSV = Path(f'predictions/{datetime.now().strftime(f"%H-%M.csv")}')

print(ANS_CSV)

def main():
    boxes = []
    with open(BOX_CSV) as f:
        for line in f.readlines()[1:]:
            line = line.split(',')
            box_idx = int(line[0])
            box_name = line[1]
            l, w, h = map(float, line[2:])
            boxes.append(Box(box_idx, box_name, l, w, h))
    boxes.sort(key=lambda b: (b.volume, b.idx))

    skus = {}
    with open(SKU_DIMENSION_CSV) as f:
        for line in f.readlines()[1:]:
            line = line.split(',')
            sku_name = line[0]
            l, w, h = map(float, line[1:])
            skus[sku_name] = SKU(l, w, h, sort=True)

    orders = {}
    order_ids = []
    with open(ORDER_CSV) as f:
        for line in f.readlines()[1:]:
            order_id, sku_id, quantity = line.split(',')
            quantity = int(quantity)

            if order_id not in orders:
                orders[order_id] = []
                order_ids.append(order_id)

            # orders[order_id].extend([skus[sku_id]] * quantity)
            orders[order_id].append(skus[sku_id] * quantity)


    ans = {}
    for order_id in order_ids:
        best_box = 'ERROR'

        if len(orders[order_id]) == 1:
            best_box = stack_skus(boxes, orders[order_id])
        elif 2 <= len(orders[order_id]) <= 4:
            best_box = stack_skus_with_rotation(boxes, orders[order_id])
        else:
            best_box = greedy_way(boxes, orders[order_id])

        # if best_box is None and len(orders[order_id]) >= 10:
        #     total_volume = sum([sku.volume for sku in orders[order_id]])

        #     available_boxes = [box for box in boxes if box.volume > total_volume]
        #     if len(available_boxes) > 0:
        #         first_volume = available_boxes[0].volume
        #         available_boxes = [box for box in boxes if box.volume > first_volume]
        #         if len(available_boxes) > 0:
        #             best_box = available_boxes[0]

        if best_box:
            ans[order_id] = best_box.name
        else:
            ans[order_id] = 'UNFITTED'



    with open(ANS_CSV, 'w', encoding='utf-8') as f:
        print('order_number,box_number', file=f)
        for order_id in order_ids:
            print(f'{order_id},{ans[order_id]}', file=f)

main()