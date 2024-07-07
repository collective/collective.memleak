import pprint
import sys
import tempfile
import random
import types
import objgraph
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Acquisition import Implicit
from six import class_types
import gc

try:
    # Python 2
    from cStringIO import StringIO
except ImportError:
    # Python 3
    from io import StringIO


class MemView(BrowserView):
    def __init__(self, context, request):
        self.request = request
        self.context = context
        self.target = None
        self.type = None


    index = ViewPageTemplateFile("memview.pt")

    def __call__(self):
        if self.request.get("gc"):
            gc.collect()
        target = self.request.get('target', "")
        if target[:2] == '0x':
            self.target, self.type = target.split("|")
            self.target = int(self.target, 16)
        else:
            self.type = target
        if self.type and self.request.get('random'):
            self.target = id(random.choice(objgraph.by_type(self.type)))
        return self.index()

    def top_counts(self, limit=200):
        sort = self.request.get("sort")
        filterq = self.request.get("filter", "")

        def filter(obj):
            name = objgraph._long_typename(obj)
            return filterq in name

        diffs = {
            n: diff
            for n, c, diff in objgraph.growth(
                limit=200, shortnames=False, filter=filter
            )
        }
        refcounts = self.all_refcounts(filterq=filterq)
        gccounts = dict(objgraph.most_common_types(limit=999999999, shortnames=False, filter=filter))
        common = [
            dict(name=n, refcount=refcounts.get(n, 0), count=c, diff=diffs.get(n))
            for n, c in gccounts.items()
        ]
        for n, c in refcounts.items():
            if n not in gccounts:
                common.append(dict(name=n, refcount=c, count=0, diff=0))
        if sort == "diff":
            return sorted(
                common, key=lambda x: x["diff"] if x["diff"] else 0, reverse=True
            )[:limit]
        elif sort == "refcount":
            return sorted(
                common, key=lambda x: x["refcount"] if x["refcount"] else 0, reverse=True
            )[:limit]
        return common[:limit]

    def all_types(self, t=(type(Implicit),) + class_types, filterq=None):
        # from https://github.com/zopefoundation/Zope/blob/master/src/App/ApplicationManager.py#L172
        for m in list(sys.modules.values()):
            if m is None:
                continue
            if not isinstance(m, types.ModuleType) or 'six.' in m.__name__:
                continue
            for sym in dir(m):
                ob = getattr(m, sym)
                if type(ob) in t:
                    ob_name = getattr(ob, "__name__", "unknown")
                    if hasattr(ob, '__module__'):
                        name = '%s.%s' % (ob.__module__, ob_name)
                    else:
                        name = '%s' % ob_name
                    # name = objgraph._long_typename(ob)
                    if not filterq or filterq in name:
                        yield (name, ob)

    def all_refcounts(self, filterq=None):
        counts = {}
        for name, ob in self.all_types(filterq=filterq):
            counts[name] = sys.getrefcount(ob)
        return counts


    def url(self, obj=None):
        sort = self.request.get("sort")
        filter = self.request.get("filter")
        if obj is not None:
            name = objgraph._long_typename(obj)
            target = "{}|{}".format(hex(id(obj)), name)
        else:
            target = self.request.get("target", "")
        return "./memview?sort={}&filter={}&target={}".format(sort, filter, target)
    
    def get_obj(self):
        if self.target:
            return objgraph.at(self.target)
        elif self.type:
            return next(self.all_types(filterq=self.type))
        else:
            return None

    def get_repr(self):
        target = self.request.target
        if target[:2] == '0x':
            return pprint.pformat(self.get_obj(), indent=4)
        else:
            return ""

    def backrefs(self):
        if self.get_obj() is None:
            return ""

        fp = StringIO()
        try:
            objgraph.show_backrefs(
                self.get_obj(), max_depth=3, output=fp, extra_node_attrs=lambda x: dict(URL=self.url(x))
            )
        except IndexError:
            return ""
        return self.quotedot(fp)

    def chain(self):
        if self.get_obj() is None:
            return ""
        try:
            chain = objgraph.find_backref_chain(
                self.get_obj(), objgraph.is_proper_module,
            )
        except IndexError:
            return ""
        fp = StringIO()
        objgraph.show_chain(chain, output=fp, extra_node_attrs=lambda x: dict(URL=self.url(x)))
        return self.quotedot(fp)

    def chain_png(self):
        target = self.request.target
        _, filename = tempfile.mkstemp(prefix="memview-", suffix=".png", text=False)
        chain = objgraph.find_backref_chain(
            random.choice(objgraph.by_type(target)), objgraph.is_proper_module
        )
        objgraph.show_chain(chain, filename=filename)
        self.request.response.setHeader("Content-type", "image/png")
        with open(filename, "rb") as f:
            return f.read()

    def backrefs_png(self):
        target = self.request.target
        _, filename = tempfile.mkstemp(prefix="memview-", suffix=".png", text=False)
        objgraph.show_backrefs(
            random.choice(objgraph.by_type(target)), max_depth=5, filename=filename
        )
        self.request.response.setHeader("Content-type", "image/png")
        with open(filename, "rb") as f:
            return f.read()

    def quotedot(self, fp):
        return fp.getvalue().replace("\n", " ").replace("\\n", " ")


