# fancytable

Display pandas dataframe table in fancy colors.

## Install

`pip install fancytable`


## Usage

Basic usage:

```py
import fancytable as ft

data = pd.DataFrame(np.random.randn(5, 10))

ft.display(data)
```

![](https://gyazo.com/ad19d2ee45898c03d6a0414d80f30f5f.png)

Filter only topk or bottomk:

```py
ft.display(data, topk=1)
```

![](https://i.gyazo.com/c08f9d8641f31448f567ec9470fb2dca.png)


In row based:

```py
ft.display(data, topk=1, axis=1)
```

![](https://i.gyazo.com/08d8d2268a7c63ca22a8d4569576ffb8.png)
