# Overall Structure

Basic information is stored in:

```python
# schema.py
class GraphSchema:
    def __init__(self):
        self.label_num = None
        self.edge_prop_val = None
        self.types2prop = None
        self.node_prop_val = None
        self.prop = None
        self.CG = ConstantGenerator()
```

Any class that needs these information can accept a variable whose type is `GraphSchema`.

![](./structure.png)