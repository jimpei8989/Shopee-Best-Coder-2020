class Box:
    def __init__(self, idx, name, l, w, h):
        self.idx = idx
        self.name = name
        self.l = l
        self.w = w
        self.h = h

    def __lt__(self, other):
        return (
            (self.volume < other.volume) or
            (self.volume == other.volume and self.idx < other.idx)
        )

    @property
    def volume(self):
        return self.l * self.w * self.h

    def can_place(self, sku):
        return (
            (sku.l <= self.l and sku.w <= self.w and sku.h <= self.h) or
            (sku.l <= self.l and sku.h <= self.w and sku.w <= self.h) or
            (sku.w <= self.l and sku.l <= self.w and sku.h <= self.h) or
            (sku.w <= self.l and sku.h <= self.w and sku.l <= self.h) or
            (sku.h <= self.l and sku.l <= self.w and sku.w <= self.h) or
            (sku.h <= self.l and sku.w <= self.w and sku.l <= self.h)
        )
