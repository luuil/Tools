---
title: 'Python: Decorator'
categories:
  - Tutorial
tags:
  - Python
  - Decorator
date: 2018-09-19 10:25:46
---

Python 的修饰器的英文名叫 Decorator, 当你看到这个英文名的时候, 你可能会把其跟 Design Pattern 里的 Decorator 搞混了, 其实这是完全不同的两个东西. 在介绍装饰器之前, 我们先来点直观的认识, 下面一个 Python 修饰器的示例代码

```python
def tags(tag_name):
    def tags_decorator(func):
        def func_wrapper(name):
            return "<{0}>{1}</{0}>".format(tag_name, func(name))
        return func_wrapper
    return tags_decorator

@tags("div")
@tags("p")
@tags("span")
def get_text(name):
    return "Hello " + name

print(get_text("John"))
```

运行这段代码时, 会有如下输出

```
<div><p><span>Hello John</span></p></div>
```

参考: [https://www.cnblogs.com/zh605929205/p/7704902.html](https://www.cnblogs.com/zh605929205/p/7704902.html)

<!-- more -->

