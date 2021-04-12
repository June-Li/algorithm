from itertools import chain
from pdfplumber import utils

class Container(object):
    cached_properties = [ "_rect_edges", "_edges", "_objects" ]

    def flush_cache(self, properties=None):
        props = self.cached_properties if properties == None else properties
        for p in props:
            if hasattr(self, p):
                delattr(self, p)

    @property
    def rects(self):
        return self.objects.get("rect", [])

    @property
    def lines(self):
        return self.objects.get("line", [])

    @property
    def curves(self):
        return self.objects.get("curve", [])

    @property
    def images(self):
        return self.objects.get("image", [])

    @property
    def figures(self):
        return self.objects.get("figure", [])

    @property
    def chars(self):
        return self.objects.get("char", [])

    @property
    def annos(self):
        return self.objects.get("anno", [])

    @property
    def rect_edges(self):
        if hasattr(self, "_rect_edges"): return self._rect_edges
        rect_edges_gen = (utils.rect_to_edges(r) for r in self.rects)
        self._rect_edges = list(chain(*rect_edges_gen))
        return self._rect_edges

    @property
    def img_edges(self):
        if hasattr(self, "_img_edges"): return self._img_edges
        img_edges_gen = (utils.image_to_edges(r) for r in self.images)
        self._img_edges = list(chain(*img_edges_gen))
        return self._img_edges


    @property
    def edges(self):
        if hasattr(self, "_edges"): return self._edges
        line_edges = list(map(utils.line_to_edge, self.lines))
        self._image_e=self.img_edges
        self._edges = self.rect_edges + line_edges+self._image_e
        
        return self._edges

    @property
    def horizontal_edges(self):
        test = lambda x: x["orientation"] == "h"
        return list(filter(test, self.edges))

    @property
    def vertical_edges(self):
        test = lambda x: x["orientation"] == "v"
        return list(filter(test, self.edges))
