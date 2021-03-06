from pdfplumber import utils
from operator import itemgetter
import itertools
from decimal import *

DEFAULT_SNAP_TOLERANCE = 3
DEFAULT_JOIN_TOLERANCE = 3
DEFAULT_MIN_WORDS_VERTICAL = 3
DEFAULT_MIN_WORDS_HORIZONTAL = 1


def move_to_avg(objs, orientation):
    """
    Move `objs` vertically/horizontally to their average x/y position.
    """
    if orientation not in ("h", "v"):
        raise ValueError("Orientation must be 'v' or 'h'")
    if len(objs) == 0: return []
    move_axis = "v" if orientation == "h" else "h"
    attr = "top" if orientation == "h" else "x0"
    values = list(map(itemgetter(attr), objs))
    q = pow(10, utils.decimalize(values[0]).as_tuple().exponent)
    avg = utils.decimalize(float(sum(values) / len(values)), q)
    new_objs = [utils.move_object(obj, move_axis, avg - obj[attr])
                for obj in objs]
    return new_objs


def snap_edges(edges, tolerance=DEFAULT_SNAP_TOLERANCE):
    """
    Given a list of edges, snap any within `tolerance` pixels of one another to their positional average.
    """
    v, h = [list(filter(lambda x: x["orientation"] == o, edges))
            for o in ("v", "h")]

    v = [move_to_avg(cluster, "v")
         for cluster in utils.cluster_objects(v, "x0", tolerance)]

    h = [move_to_avg(cluster, "h")
         for cluster in utils.cluster_objects(h, "top", tolerance)]

    snapped = list(itertools.chain(*(v + h)))
    return snapped


def join_edge_group(edges, orientation, tolerance=DEFAULT_JOIN_TOLERANCE):
    """
    Given a list of edges along the same infinite line, join those that are within `tolerance` pixels of one another.
    """
    if orientation == "h":
        min_prop, max_prop = "x0", "x1"
    elif orientation == "v":
        min_prop, max_prop = "top", "bottom"
    else:
        raise ValueError("Orientation must be 'v' or 'h'")

    sorted_edges = list(sorted(edges, key=itemgetter(min_prop)))
    joined = [sorted_edges[0]]
    for e in sorted_edges[1:]:
        last = joined[-1]
        if e[min_prop] <= (last[max_prop] + tolerance):
            if e[max_prop] > last[max_prop]:
                # Extend current edge to new extremity
                joined[-1] = utils.resize_object(last, max_prop, e[max_prop])
            else:
                # Do nothing; edge is fully contained in pre-existing edge
                pass
        else:
            # Edge is separate from previous edges
            joined.append(e)

    return joined


def merge_edges(edges, snap_tolerance, join_tolerance):
    """
    Using the `snap_edges` and `join_edge_group` methods above, merge a list of edges into a more "seamless" list.
    """

    def get_group(edge):
        if edge["orientation"] == "h":
            return ("h", edge["top"])
        else:
            return ("v", edge["x0"])

    if snap_tolerance > 0:
        edges = snap_edges(edges, snap_tolerance)

    if join_tolerance > 0:
        _sorted = sorted(edges, key=get_group)
        edge_groups = itertools.groupby(_sorted, key=get_group)
        edge_gen = (join_edge_group(items, k[0], join_tolerance)
                    for k, items in edge_groups)
        edges = list(itertools.chain(*edge_gen))
    return edges


def words_to_edges_h(words,
                     word_threshold=DEFAULT_MIN_WORDS_HORIZONTAL):
    """
    Find (imaginary) horizontal lines that connect the tops of at least `word_threshold` words.
    """
    by_top = utils.cluster_objects(words, "top", 1)
    large_clusters = filter(lambda x: len(x) >= word_threshold, by_top)
    rects = list(map(utils.objects_to_rect, large_clusters))
    if len(rects) == 0:
        return []
    min_x0 = min(map(itemgetter("x0"), rects))
    max_x1 = max(map(itemgetter("x1"), rects))
    edges = [{
        "x0": min_x0,
        "x1": max_x1,
        "top": r["top"],
        "bottom": r["top"],
        "width": max_x1 - min_x0,
        "orientation": "h"
    } for r in rects] + [{
        "x0": min_x0,
        "x1": max_x1,
        "top": r["bottom"],
        "bottom": r["bottom"],
        "width": max_x1 - min_x0,
        "orientation": "h"
    } for r in rects]

    return edges


def words_to_edges_v(words,
                     word_threshold=DEFAULT_MIN_WORDS_VERTICAL):
    """
    Find (imaginary) vertical lines that connect the left, right, or center of at least `word_threshold` words.
    """
    # Find words that share the same left, right, or centerpoints
    by_x0 = utils.cluster_objects(words, "x0", 1)
    by_x1 = utils.cluster_objects(words, "x1", 1)
    by_center = utils.cluster_objects(words, lambda x: (x["x0"] + x["x1"]) / 2, 1)
    clusters = by_x0 + by_x1 + by_center

    # Find the points that align with the most words
    sorted_clusters = sorted(clusters, key=lambda x: -len(x))
    large_clusters = filter(lambda x: len(x) >= word_threshold, sorted_clusters)

    # For each of those points, find the rectangles fitting all matching words
    rects = list(map(utils.objects_to_rect, large_clusters))

    # Iterate through those rectangles, condensing overlapping rectangles
    condensed_rects = []
    for rect in rects:
        overlap = False
        for c in condensed_rects:
            if utils.objects_overlap(rect, c):
                overlap = True
                break
        if overlap == False:
            condensed_rects.append(rect)

    if len(condensed_rects) == 0:
        return []
    sorted_rects = list(sorted(condensed_rects, key=itemgetter("x0")))

    # Find the far-right boundary of the rightmost rectangle
    last_rect = sorted_rects[-1]
    while True:
        words_inside = utils.intersects_bbox(
            [w for w in words if w["x0"] >= last_rect["x0"]],
            (last_rect["x0"], last_rect["top"], last_rect["x1"], last_rect["bottom"]),
        )
        rect = utils.objects_to_rect(words_inside)
        if rect == last_rect:
            break
        else:
            last_rect = rect

    # Describe all the left-hand edges of each text cluster
    edges = [{
        "x0": b["x0"],
        "x1": b["x0"],
        "top": b["top"],
        "bottom": b["bottom"],
        "height": b["bottom"] - b["top"],
        "orientation": "v"
    } for b in sorted_rects] + [{
        "x0": last_rect["x1"],
        "x1": last_rect["x1"],
        "top": last_rect["top"],
        "bottom": last_rect["bottom"],
        "height": last_rect["bottom"] - last_rect["top"],
        "orientation": "v"
    }]

    return edges


def edges_to_intersections(edges, x_tolerance=5, y_tolerance=5):
    """
    Given a list of edges, return the points at which they intersect within `tolerance` pixels.
    """
    intersections = {}
    points = {}
    v_edges, h_edges = [list(filter(lambda x: x["orientation"] == o, edges))
                        for o in ("v", "h")]
    new_v_edges, new_h_edges = [list(filter(lambda x: x["orientation"] == o, edges))
                                for o in ("v", "h")]
    for v in sorted(v_edges, key=itemgetter("x0", "top")):
        for h in sorted(h_edges, key=itemgetter("top", "x0")):
            if ((v["top"] <= (h["top"] + y_tolerance)) and
                    (v["bottom"] >= (h["top"] - y_tolerance)) and
                    (v["x0"] >= (h["x0"] - x_tolerance)) and
                    (v["x0"] <= (h["x1"] + x_tolerance))):
                vertex = vertex = (v["x0"], h["top"])
                if vertex not in points.keys():
                    points[vertex] = 1
                    points, new_v_edges, new_h_edges = if_add_first(v, h, points, new_v_edges, new_h_edges)

    for v in sorted(v_edges, key=itemgetter("x0", "top"), reverse=True):
        for h in sorted(h_edges, key=itemgetter("top", "x0"), reverse=True):
            if ((v["top"] <= (h["top"] + y_tolerance)) and
                    (v["bottom"] >= (h["top"] - y_tolerance)) and
                    (v["x0"] >= (h["x0"] - x_tolerance)) and
                    (v["x0"] <= (h["x1"] + x_tolerance))):
                points, new_v_edges, new_h_edges = if_add_after(v, h, points, new_v_edges, new_h_edges)
                ## we should merge edges again
    edges = list(new_v_edges) + list(new_h_edges)
    edges = merge_edges(edges,
                        snap_tolerance=3,
                        join_tolerance=3,
                        )
    new_v_edges, new_h_edges = [list(filter(lambda x: x["orientation"] == o, edges))
                                for o in ("v", "h")]

    for v in sorted(new_v_edges, key=itemgetter("x0", "top")):
        for h in sorted(new_h_edges, key=itemgetter("top", "x0")):
            if ((v["top"] <= (h["top"] + y_tolerance)) and
                    (v["bottom"] >= (h["top"] - y_tolerance)) and
                    (v["x0"] >= (h["x0"] - x_tolerance)) and
                    (v["x0"] <= (h["x1"] + x_tolerance))):
                vertex = (v["x0"], h["top"])
                if vertex not in intersections:
                    intersections[vertex] = {"v": [], "h": []}
                intersections[vertex]["v"].append(v)
                intersections[vertex]["h"].append(h)
    return intersections


def if_add_after(v, h, points, v_edges, h_edges):
    point = [v['x0'], h['top']]

    if h['x1'] >= point[0] or abs(h['x1'] - point[0]) < 1:
        vertex = (h["x1"], h["top"])
        if vertex not in points:
            points[vertex] = 1
            if h['x1'] > point[0] + 5:
                v1 = v.copy()
                v1['x0'] = h['x1']
                v1['x1'] = h['x1']
                v_edges.append(v1)

    if v['bottom'] >= point[1] or abs(v['bottom'] - point[1]) < 1:
        vertex = (v["x0"], v["bottom"])
        if vertex not in points:
            points[vertex] = 1
            if v['top'] > point[1] + 5:
                h1 = h.copy()
                h1['top'] = v['bottom']
                h1['bottom'] = v['bottom']
                h_edges.append(h1)
    return points, v_edges, h_edges


def if_add_first(v, h, dicts, v_edges, h_edges):
    point = [v['x0'], h['top']]
    if h['x0'] <= point[0] or abs(h['x0'] - point[0]) < 1:
        vertex = (h["x0"], h["top"])
        if vertex not in dicts.keys():
            dicts[vertex] = 1
            if h['x0'] < point[0] - 5:
                v1 = v.copy()
                v1['x0'] = h['x0']
                v1['x1'] = h['x0']
                v_edges.append(v1)

    if v['top'] <= point[1] or abs(v['top'] - point[1]) < 1:
        vertex = (v["x0"], v["top"])
        if vertex not in dicts.keys():

            dicts[vertex] = 1

            if v['top'] <= point[1] - 5:
                h1 = h.copy()
                h1['top'] = v['top']
                h1['bottom'] = v['top']
                h_edges.append(h1)

    return dicts, v_edges, h_edges


def intersections_to_cells(intersections):
    """
    Given a list of points (`intersections`), return all retangular "cells" those points describe.

    `intersections` should be a dictionary with (x0, top) tuples as keys,
    and a list of edge objects as values. The edge objects should correspond
    to the edges that touch the intersection.
    """

    def edge_connects(p1, p2):
        def edges_to_set(edges):
            return set(map(utils.obj_to_bbox, edges))

        if p1[0] == p2[0]:
            common = edges_to_set(intersections[p1]["v"]) \
                .intersection(edges_to_set(intersections[p2]["v"]))
            if len(common): return True

        if p1[1] == p2[1]:
            common = edges_to_set(intersections[p1]["h"]) \
                .intersection(edges_to_set(intersections[p2]["h"]))
            if len(common): return True
        return False

    points = list(sorted(intersections.keys()))
    n_points = len(points)

    def find_smallest_cell(points, i):
        if i == n_points - 1: return None
        pt = points[i]

        rest = points[i + 1:]
        # Get all the points directly below and directly right
        below = [x for x in rest if x[0] == pt[0]]
        right = [x for x in rest if x[1] == pt[1]]
        for below_pt in below:
            if not edge_connects(pt, below_pt): continue

            for right_pt in right:
                if not edge_connects(pt, right_pt): continue

                bottom_right = (right_pt[0], below_pt[1])

                if ((bottom_right in intersections) and
                        edge_connects(bottom_right, right_pt) and
                        edge_connects(bottom_right, below_pt)):
                    return (
                        pt[0],
                        pt[1],
                        bottom_right[0],
                        bottom_right[1]
                    )

    cell_gen = (find_smallest_cell(points, i) for i in range(len(points)))

    return list(filter(None, cell_gen))


def cells_to_tables(cells):
    """
    Given a list of bounding boxes (`cells`), return a list of tables that hold those those cells most simply (and contiguously).
    """

    def bbox_to_corners(bbox):
        # print(bbox)
        x0, top, x1, bottom = bbox

        return list(itertools.product((x0, x1), (top, bottom)))

    cells = [{
        "available": True,
        "bbox": bbox,
        "corners": bbox_to_corners(bbox)
    } for bbox in cells if bbox[3] > bbox[1] + Decimal(0.5) and bbox[2] > bbox[0] + Decimal(0.5)]

    # Iterate through the cells found above, and assign them
    # to contiguous tables

    def init_new_table():
        return {"corners": set([]), "cells": []}

    def assign_cell(cell, table):
        table["corners"] = table["corners"].union(set(cell["corners"]))
        table["cells"].append(cell["bbox"])
        cell["available"] = False

    n_cells = len(cells)
    n_assigned = 0
    tables = []
    current_table = init_new_table()
    while True:
        initial_cell_count = len(current_table["cells"])
        for i, cell in enumerate(filter(itemgetter("available"), cells)):
            if len(current_table["cells"]) == 0:
                assign_cell(cell, current_table)
                n_assigned += 1
            else:
                corner_count = sum(c in current_table["corners"] for c in cell["corners"])
                if corner_count > 0 and cell["available"]:
                    assign_cell(cell, current_table)
                    n_assigned += 1
        if n_assigned == n_cells:
            break
        if len(current_table["cells"]) == initial_cell_count:
            tables.append(current_table)
            current_table = init_new_table()

    if len(current_table["cells"]):
        tables.append(current_table)

    _sorted = sorted(tables, key=lambda t: min(t["corners"]))
    filtered = [t["cells"] for t in _sorted if len(t["cells"]) > 1]
    return filtered


class CellGroup(object):
    def __init__(self, cells):
        self.cells = cells
        self.bbox = (
            min(map(itemgetter(0), filter(None, cells))),
            min(map(itemgetter(1), filter(None, cells))),
            max(map(itemgetter(2), filter(None, cells))),
            max(map(itemgetter(3), filter(None, cells))),
        )


class Row(CellGroup):
    pass


class Table(object):
    def __init__(self, page, cells):
        self.page = page
        self.cells = cells
        self.bbox = (
            min(map(itemgetter(0), cells)),
            min(map(itemgetter(1), cells)),
            max(map(itemgetter(2), cells)),
            max(map(itemgetter(3), cells)),
        )

    @property
    def rows(self):
        _sorted = sorted(self.cells, key=itemgetter(1, 0))
        xs = list(sorted(set(map(itemgetter(0), self.cells))))
        rows = []
        for y, row_cells in itertools.groupby(_sorted, itemgetter(1)):
            xdict = dict((cell[0], cell) for cell in row_cells)
            row = Row([xdict.get(x) for x in xs])
            rows.append(row)
        return rows

    def extract(self,
                x_tolerance=utils.DEFAULT_X_TOLERANCE,
                y_tolerance=utils.DEFAULT_Y_TOLERANCE):

        chars = self.page.chars
        # print(chars)
        table_arr = []

        def char_in_bbox(char, bbox):
            v_mid = (char["top"] + char["bottom"]) / 2
            h_mid = (char["x0"] + char["x1"]) / 2
            x0, top, x1, bottom = bbox
            return (
                    (h_mid >= x0) and
                    (h_mid < x1) and
                    (v_mid >= top) and
                    (v_mid < bottom)
            )

        for row in self.rows:
            arr = []
            row_chars = [char for char in chars
                         if char_in_bbox(char, row.bbox)]

            for cell in row.cells:
                if cell == None:
                    cell_text = None
                else:
                    cell_chars = [char for char in row_chars
                                  if char_in_bbox(char, cell)]

                    if len(cell_chars):
                        cell_text = utils.extract_text(cell_chars,
                                                       x_tolerance=x_tolerance,
                                                       y_tolerance=y_tolerance).strip()
                    else:
                        cell_text = ""
                arr.append(cell_text)
            table_arr.append(arr)
        # print(table_arr)
        return table_arr


TABLE_STRATEGIES = ["lines", "lines_strict", "text", "explicit"]
DEFAULT_TABLE_SETTINGS = {
    "vertical_strategy": "lines",
    "horizontal_strategy": "lines",
    "explicit_vertical_lines": [],
    "explicit_horizontal_lines": [],
    "snap_tolerance": DEFAULT_SNAP_TOLERANCE,
    "join_tolerance": DEFAULT_JOIN_TOLERANCE,
    "edge_min_length": 3,
    "min_words_vertical": DEFAULT_MIN_WORDS_VERTICAL,
    "min_words_horizontal": DEFAULT_MIN_WORDS_HORIZONTAL,
    "keep_blank_chars": False,
    "text_tolerance": 3,
    "text_x_tolerance": None,
    "text_y_tolerance": None,
    "intersection_tolerance": 3,
    "intersection_x_tolerance": 2,
    "intersection_y_tolerance": 2,
}


class TableFinder(object):
    """
    Given a PDF page, find plausible table structures.

    Largely borrowed from Anssi Nurminen's master's thesis: http://dspace.cc.tut.fi/dpub/bitstream/handle/123456789/21520/Nurminen.pdf?sequence=3

    ... and inspired by Tabula: https://github.com/tabulapdf/tabula-extractor/issues/16
    """

    def __init__(self, page, settings={}):
        for k in settings.keys():
            if k not in DEFAULT_TABLE_SETTINGS:
                raise ValueError("Unrecognized table setting: '{0}'".format(
                    k
                ))
        self.page = page
        self.settings = dict(DEFAULT_TABLE_SETTINGS)
        self.settings.update(settings)
        for var, fallback in [
            ("text_x_tolerance", "text_tolerance"),
            ("text_y_tolerance", "text_tolerance"),
            ("intersection_x_tolerance", "intersection_tolerance"),
            ("intersection_y_tolerance", "intersection_tolerance"),
        ]:
            if self.settings[var] == None:
                self.settings.update({
                    var: self.settings[fallback]
                })
        self.edges = self.get_edges()
        self.intersections = edges_to_intersections(
            self.edges,
            self.settings["intersection_x_tolerance"],
            self.settings["intersection_y_tolerance"],
        )
        self.cells = intersections_to_cells(
            self.intersections
        )
        self.tables = [Table(self.page, t)
                       for t in cells_to_tables(self.cells)]

    def get_edges(self):
        settings = self.settings
        for name in ["vertical", "horizontal"]:
            strategy = settings[name + "_strategy"]
            if strategy not in TABLE_STRATEGIES:
                raise ValueError("{0} must be one of {{{1}}}".format(
                    name + "_strategy",
                    ",".join(TABLE_STRATEGIES)
                ))
            if strategy == "explicit":
                if len(settings["explicit_" + name + "_lines"]) < 2:
                    raise ValueError(
                        "If {0} == 'explicit', {1} must be specified as list/tuple of two or more floats/ints.".format(
                            strategy + "_strategy",
                            "explicit_" + name + "_lines",
                        ))

        v_strat = settings["vertical_strategy"]
        h_strat = settings["horizontal_strategy"]

        if v_strat == "text" or h_strat == "text":
            xt = settings["text_x_tolerance"]
            if xt == None:
                xt = settings["text_tolerance"]
            yt = settings["text_y_tolerance"]
            if yt == None:
                yt = settings["text_tolerance"]
            words = self.page.extract_words(
                x_tolerance=xt,
                y_tolerance=yt,
                keep_blank_chars=settings["keep_blank_chars"]
            )

        def v_edge_desc_to_edge(desc):
            if isinstance(desc, dict):
                edge = {
                    "x0": desc.get("x0", desc.get("x")),
                    "x1": desc.get("x1", desc.get("x")),
                    "top": desc.get("top", self.page.bbox[1]),
                    "bottom": desc.get("bottom", self.page.bbox[3]),
                    "orientation": "v"
                }
            else:
                edge = {
                    "x0": desc,
                    "x1": desc,
                    "top": self.page.bbox[1],
                    "bottom": self.page.bbox[3],
                }
            edge["height"] = edge["bottom"] - edge["top"]
            edge["orientation"] = "v"
            return edge

        v_explicit = list(map(v_edge_desc_to_edge, settings["explicit_vertical_lines"]))

        if v_strat == "lines":
            v_base = utils.filter_edges(self.page.edges, "v", min_length=0)
        elif v_strat == "lines_strict":
            v_base = utils.filter_edges(self.page.edges, "v",
                                        edge_type="lines")
        elif v_strat == "text":
            v_base = words_to_edges_v(words,
                                      word_threshold=settings["min_words_vertical"])
        elif v_strat == "explicit":
            v_base = []

        v = v_base + v_explicit

        def h_edge_desc_to_edge(desc):
            if isinstance(desc, dict):
                edge = {
                    "x0": desc.get("x0", self.page.bbox[0]),
                    "x1": desc.get("x1", self.page.bbox[2]),
                    "top": desc.get("top", desc.get("bottom")),
                    "bottom": desc.get("bottom", desc.get("top")),
                }
            else:
                edge = {
                    "x0": self.page.bbox[0],
                    "x1": self.page.bbox[2],
                    "top": desc,
                    "bottom": desc,
                }
            edge["width"] = edge["x1"] - edge["x0"]
            edge["orientation"] = "h"
            return edge

        h_explicit = list(map(h_edge_desc_to_edge, settings["explicit_horizontal_lines"]))

        if h_strat == "lines":
            h_base = utils.filter_edges(self.page.edges, "h", min_length=0)
        elif h_strat == "lines_strict":
            h_base = utils.filter_edges(self.page.edges, "h",
                                        edge_type="lines", min_length=0)
        elif h_strat == "text":
            h_base = words_to_edges_h(words,
                                      word_threshold=settings["min_words_horizontal"])
        elif h_strat == "explicit":
            h_base = []

        h = h_base + h_explicit

        edges = list(v) + list(h)

        if settings["snap_tolerance"] > 0 or settings["join_tolerance"] > 0:
            edges = merge_edges(edges,
                                snap_tolerance=settings["snap_tolerance"],
                                join_tolerance=settings["join_tolerance"],
                                )
        # return edges
        return utils.filter_edges(edges,
                                  min_length=5)
