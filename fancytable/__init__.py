import numpy as np

DEFAULT_GRADIENT = ('#FE9800', '#FFFFCC', '#CCDB39')


class FancyTable:

    def __init__(self, colors=None):
        '''
        Parameters:
            colors (tuple): Set of gradient colors in hex. (start, middle, end)
        '''
        self._grad = DEFAULT_GRADIENT if colors is None else colors

    def display(self, df, axis=0, topk=None, bottomk=None):
        '''Display pd.DataFrame with colors.

        Add colors based on the strength of the z-score in each row or column.

        Parameters:
            df (pd.DataFrame): Dataframe object to display.
            axis (int)       : axis to calculate z-score.
            topk (int)       : Add colors only for topk items.
            bottomk (int)    : Add colors only for bottomk items.
        '''
        assert axis in (0, 1)
        if axis == 1:
            df = df.T

        n = len(df)

        z = df.rank() - 1

        if axis == 1:
            z = z.T

        gradients = grad(*self._grad, n=n)

        def attn(h):
            hcolors = []
            for i in h.index:
                rank = z[h.name][i]

                if np.isnan(rank):
                    hcolors.append(None)
                    continue

                if topk is not None and rank >= (n-topk):
                    hcolors.append(gradients[int(rank)])
                    continue

                if bottomk is not None and rank <= (bottomk-1):
                    hcolors.append(gradients[int(rank)])
                    continue

                if topk is not None or bottomk is not None:
                    hcolors.append(None)
                    continue

                hcolors.append(gradients[int(rank)])

            return ['background-color: {};'.format(v) if v else '' for v in hcolors]

        if axis == 1:
            df = df.T

        return df.style.apply(attn)


def hex2rgb(hex):
    return [int(hex[i:i+2], 16) for i in range(1,6,2)]


def rgb2hex(rgb):
    rgb = [int(x) for x in rgb]
    return "#"+"".join([
        "0{0:x}".format(v) if v < 16 else "{0:x}".format(v)
        for v in rgb
    ])


def grad(start, mid, end, n=10, by='hex'):
    if n <= 3:
        if n == 1:
            c = [mid]
        elif n == 2:
            c = [start, end]
        elif n == 3:
            c = [start, mid, end]
        if by == 'rgb':
            return list(map(rgb2hex, c))
        return c

    if n % 2 == 0:
        nin = n//2 + 1
        nout = n//2
    else:
        nin = n // 2 + 1
        nout = n // 2 + 1

    return (
        _grad(start, mid, n=nin, by=by)[:-1] +
        _grad(mid, end, n=nout, by=by)
    )

def _grad(start, end, n=10, by='hex'):
    '''
    Parameters:
        start (str):
            hex color start gradient from.
        end (str):
            hex color end gradient on.
        n (int):
            # of gradient colors to get.
    '''
    s = hex2rgb(start)
    f = hex2rgb(end)

    colors = [s]

    for t in range(1, n):

        # Interpolate RGB vector for color at the current value of t
        curr_vector = [
          int(s[j] + (float(t)/(n-1))*(f[j]-s[j]))
          for j in range(3)
        ]

        # Add it to our list of output colors
        colors.append(curr_vector)

    if by == 'hex':
        return [rgb2hex(c) for c in colors]
    elif by == 'rgb':
        return colors


ft = FancyTable()


def display(df, axis=0, topk=None, bottomk=None):
    return ft.display(df, axis, topk, bottomk)
