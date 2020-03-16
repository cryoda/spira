# class Meta(type):
#     def __call__(self, *args, **kwargs):
#         print("Meta __call__")
#         super().__call__(*args, **kwargs)
#
#     def __new__(mcs, *args, **kwargs):
#         print("Meta __new__")
#         return super().__new__(mcs, *args, **kwargs)
# #
# #     def __prepare__(msc, name, **kwargs):
# #         print("Meta __prepare__")
# #         return {}
# #
# class SubMeta(type, metaclass=Meta):
#     def __call__(self):
#         print("SubMeta __call__!")
#         super().__call__()
#
#     def __new__(mcs, name, bases, attrs, **kwargs):
#         print("SubMeta __new__")
#         return super().__new__(mcs, name, bases, kwargs)
#
#     def __prepare__(msc, name, **kwargs):
#         print("SubMeta __prepare__")
#         return Meta.__prepare__(name, kwargs)
#
# class B(SubMeta):
#     pass
#
# b = B()
#
# class M(type):
#     def __call__(mmcls, *args, **kwargs):
#         print("M's call", args, kwargs)
#         return super().__call__(*args, **kwargs)
#
# class MM(type, metaclass=M):
#     def __prepare__(cls, *args, **kw):
#         print("MM Prepare")
#         return {}
#     def __new__(mcls, *args, **kw):
#         print("MM __new__")
#         return super().__new__(mcls, *args, **kw)
#
# class klass(metaclass=MM):
#     pass


class Meta(type):
    def __new__(cls, name, bases, newattrs):
        print("metaclass new: %r %r %r %r" % (cls, name, bases, newattrs,))
        return super().__new__(cls, name, bases, newattrs)

    # def __call__(self, *args, **kw):
    #     print("metaclass call: %r %r %r" % (self, args, kw))
    #     return super().__call__(*args, **kw)

class Foo(metaclass=Meta):

    def __new__(self, *args, **kw):
        print("new: %r %r %r" % (self, args, kw))
        # return super().__new__(*args, **kw)
        return object.__new__(self, *args, **kw)

    def __init__(self, *args, **kw):
        print("init: %r %r %r" % (self, args, kw))

    def __call__(self, *args, **kw):
        print("class call: %r %r %r" % (self, args, kw))

f = Foo('bar')
print("main: %r" % f)