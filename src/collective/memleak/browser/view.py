import tempfile
import random
import objgraph
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
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

    index = ViewPageTemplateFile("memview.pt")

    def top_counts(self):
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
        common = [
            dict(name=n, count=c, diff=diffs.get(n))
            for n, c in objgraph.most_common_types(
                limit=200, shortnames=False, filter=filter
            )
        ]
        if sort == "diff":
            return sorted(
                common, key=lambda x: x["diff"] if x["diff"] else 0, reverse=True
            )
        return common

    def backrefs(self):
        target = self.request.target
        fp = StringIO()
        try:
            objgraph.show_backrefs(
                random.choice(objgraph.by_type(target)), max_depth=5, output=fp
            )
        except IndexError:
            return ""
        return self.quotedot(fp)

    def chain(self):
        target = self.request.target
        try:
            chain = objgraph.find_backref_chain(
                random.choice(objgraph.by_type(target)), objgraph.is_proper_module
            )
        except IndexError:
            return ""
        fp = StringIO()
        objgraph.show_chain(chain, output=fp)
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

    def __call__(self):
        import gc

        for i in range(5):
            gc.collect()
        return self.index()
