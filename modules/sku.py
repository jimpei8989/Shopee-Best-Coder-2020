class SKU:
    def __init__(self, l=0, w=0, h=0, sort=False):
        if sort:
            l, w, h = sorted([l, w, h], reverse=True)

        self.l = l
        self.w = w
        self.h = h

    def __add__(self, other):
        return SKU(
            l=max(self.l, other.l),
            w=max(self.w, other.w),
            h=self.h+other.h,
        )

    def __mul__(self, n):
        return SKU(
            l=self.l,
            w=self.w,
            h=self.h * n,
            sort=True
        )

    def __lt__(self, other):
        return (self.h, self.w, self.l) < (other.h, other.w, other.l)

    def copy(self):
        return SKU(self.l, self.w, self.h)

    def all_rotations(self):
        return [
            SKU(self.l, self.w, self.h),
            SKU(self.l, self.h, self.w),
            SKU(self.w, self.l, self.h),
            SKU(self.w, self.h, self.l),
            SKU(self.h, self.l, self.w),
            SKU(self.h, self.w, self.l),
        ]

    @property
    def volume(self):
        return self.l * self.w * self.h
