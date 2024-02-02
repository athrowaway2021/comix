from __future__ import (unicode_literals, division, absolute_import, print_function)

import base64
import io
from lxml import etree
import math
from PIL import Image
import random

from .epub_output import (add_meta_name_content, SVG, SVG_NAMESPACES, XLINK_HREF)
from .ion import (ion_type, IonStruct, IonSymbol, IS)
from .message_logging import log
from .utilities import (Deserializer, disable_debug_log, type_name, urlrelpath)


__license__ = "GPL v3"
__copyright__ = "2016-2023, John Howell <jhowell@acm.org>"


CREATE_SVG_FILES_IN_EPUB = True
PNG_SCALE_FACTOR = 8
PNG_DENSITY_GAMMA = 3.5
PNG_EDGE_FEATHERING = 0.75
INCLUDE_PRIOR_LINE_SEGMENT = True
ROUND_LINE_ENDINGS = True
QUANTIZE_THICKNESS = True

SVG_DOCTYPE = b"<!DOCTYPE svg PUBLIC '-//W3C//DTD SVG 1.1//EN' 'http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd'>"

ERASER = "eraser"
FOUNTAIN_PEN = "fountain pen"
HIGHLIGHTER = "highlighter"
MARKER = "marker"
ORIGINAL_PEN = "original pen"
PEN = "pen"
PENCIL = "pencil"
UNKNOWN = "unknown"

THICKNESS_NAME = ["fine", "thin", "medium", "thick", "heavy"]

THICKNESS_CHOICES = {
    FOUNTAIN_PEN: [23.625, 31.5, 47.25, 78.75, 126.0],
    HIGHLIGHTER: [252.0, 315.0, 441.0, 567.0, 756.0],
    MARKER: [31.5, 63.0, 94.5, 189.0, 315.0],
    PEN: [23.625, 39.375, 55.125, 94.5, 126.0],
    ORIGINAL_PEN: [23.625, 31.5, 63.0, 94.5, 126.0],
    PENCIL: [23.625, 39.375, 63.0, 110.25, 189.0],
    UNKNOWN: [],
    }

MIN_TAF = 0
MAX_TAF = 1000

MIN_DAF = 0
MAX_DAF = 300


class KFX_EPUB_Notebook(object):

    def __init__(self):
        pass

    def process_scribe_notebook_page_section(self, section, page_template, section_name, seq):
        nmdl_canvas_width = section.pop("nmdl.canvas_width")
        nmdl_canvas_height = section.pop("nmdl.canvas_height")
        nmdl_normalized_ppi = section.pop("nmdl.normalized_ppi")

        if (nmdl_canvas_width, nmdl_canvas_height, nmdl_normalized_ppi) not in [
                (15624, 20832, 2520),
                (13726, 7350, 2520)]:
            log.error("Unexpected nmdl.canvas width=%d height=%d ppi=%d" % (
                nmdl_canvas_width, nmdl_canvas_height, nmdl_normalized_ppi))

        book_part = self.new_book_part(filename=self.NOTEBOOK_TEXT_FILEPATH % section_name)
        book_part.is_fxl = True
        add_meta_name_content(book_part.head(), "viewport", "width=%d, height=%d" % (
            nmdl_canvas_width, nmdl_canvas_height))

        body = book_part.body()

        page_svg_elem = etree.Element(SVG, nsmap=SVG_NAMESPACES, attrib={
            "version": "1.1", "preserveAspectRatio": "xMidYMid meet",
            "viewBox": "0 0 %d %d" % (nmdl_canvas_width, nmdl_canvas_height)})

        self.process_notebook_content(page_template, page_svg_elem)
        self.check_empty(page_template, "Section %s page_template" % section_name)

        if CREATE_SVG_FILES_IN_EPUB:

            page_svg_filename = self.resource_location_filename(
                "%s.svg" % section_name, "", self.IMAGE_FILEPATH, is_symbol=False)

            svg_document = etree.ElementTree(page_svg_elem)
            svg_data = etree.tostring(svg_document, encoding="utf-8", doctype=SVG_DOCTYPE, xml_declaration=True)
            self.manifest_resource(page_svg_filename, data=svg_data)

            html_svg_elem = etree.SubElement(body, SVG, nsmap=SVG_NAMESPACES, attrib={
                "version": "1.1", "preserveAspectRatio": "xMidYMid meet",
                "viewBox": "0 0 %d %d" % (nmdl_canvas_width, nmdl_canvas_height)})

            etree.SubElement(html_svg_elem, "rect", attrib={
                "x": "0", "y": "0", "width": "100%", "height": "100%", "fill": "white"})

            etree.SubElement(html_svg_elem, "image", attrib={
                "x": "0", "y": "0", "width": "100%", "height": "100%",
                XLINK_HREF: urlrelpath(page_svg_filename, ref_from=book_part.filename)})
        else:
            body.append(page_svg_elem)
            html_svg_elem = page_svg_elem

        self.add_style(html_svg_elem, {"height": "100%", "width": "100%"})

        if "$58" in section or "$59" in section:
            section["$183"] = IS("$324")
            content_props = self.process_content_properties(section)
            self.add_style(html_svg_elem, content_props, replace=True)

    def process_scribe_notebook_template_section(self, section, page_template, section_name):
        nmdl_template_type = section.pop("nmdl.template_type")
        log.info("Notebook template: %s" % nmdl_template_type)

        book_part = self.new_book_part(filename=self.NOTEBOOK_TEXT_FILEPATH % section_name)
        book_part.is_fxl = True
        top_level_elem = book_part.html
        self.process_content(page_template, top_level_elem, book_part, self.writing_mode, is_section=True)
        self.check_empty(page_template, "Section %s page_template" % section_name)

        if CREATE_SVG_FILES_IN_EPUB:
            svg_elem = book_part.body().find(SVG)
            if svg_elem is not None:
                template_svg_filename = self.resource_location_filename(
                    "%s.svg" % nmdl_template_type, "", self.IMAGE_FILEPATH, is_symbol=False)
                etree.cleanup_namespaces(book_part.html)
                svg_elem.attrib.pop("class", None)
                svg_elem.attrib.pop("style", None)
                svg_document = etree.ElementTree(svg_elem)
                svg_data = etree.tostring(svg_document, encoding="utf-8", doctype=SVG_DOCTYPE, xml_declaration=True)
                self.manifest_resource(template_svg_filename, data=svg_data)
                book_part.omit = True

                if section_name == self.nmdl_template_id:
                    for page_book_part in self.book_parts:
                        if page_book_part is not book_part:
                            html_svg_elem = page_book_part.body().find(SVG)
                            if html_svg_elem is not None:
                                if len(html_svg_elem) == 3:
                                    log.error("SVG image already has template in Scribe notebook page: %s" % page_book_part.filename)
                                    html_svg_elem.remove(html_svg_elem[1])

                                html_svg_elem.insert(1, etree.Element("image", attrib={
                                    "x": "0", "y": "0", "width": "100%", "height": "100%",
                                    XLINK_HREF: urlrelpath(template_svg_filename, ref_from=book_part.filename)}))
                            else:
                                log.error("Failed to locate the SVG image within Scribe notebook page: %s" % page_book_part.filename)
            else:
                log.error("Failed to locate the SVG image within Scribe notebook template: %s" % book_part.filename)

    def process_notebook_content(self, content, parent):
        if self.DEBUG:
            log.debug("process notebook content: %s\n" % repr(content))

        data_type = ion_type(content)

        if data_type is IonSymbol:
            self.process_notebook_content(self.get_fragment(ftype="$608", fid=content), parent)
            return

        if data_type is not IonStruct:
            log.info("content: %s" % repr(content))
            raise Exception("%s has unknown content data type: %s" % (self.content_context, type_name(content)))

        content_type = content.pop("$159", None)
        location_id = self.get_location_id(content)
        self.push_context("%s %s" % (content_type, location_id))

        if content_type == "$270":
            layout = content.pop("$156", None)

            if "$146" in content:
                for list_content in content.pop("$146", []):
                    self.process_notebook_content(list_content, parent)

            elif "$176" in content:
                story = self.get_named_fragment(content, ftype="$259")
                story_name = story.pop("$176")
                if self.DEBUG:
                    log.debug("Processing story %s" % story_name)

                self.push_context("story %s" % story_name)

                for story_content in story.pop("$146", []):
                    self.process_notebook_content(story_content, parent)

                self.pop_context()
                self.check_empty(story, self.content_context)

            if layout is None:
                if "nmdl.type" in content:
                    self.scribe_notebook_stroke(content, parent, location_id)
            elif layout != "$323":
                log.error("%s has unknown %s layout: %s" % (self.content_context, content_type, layout))
        else:
            log.error("%s has unknown content type: %s" % (self.content_context, content_type))

        self.pop_context()
        self.check_empty(content, "%s content type %s" % (self.content_context, content_type))

    def scribe_notebook_stroke(self, content, parent, location_id):

        nmdl_type = content.pop("nmdl.type")

        if nmdl_type == "nmdl.stroke_group":
            nmdl_chunked = content.pop("nmdl.chunked", None)
            nmdl_chunk_threshold = content.pop("nmdl.chunk_threshold", None)

            if nmdl_chunked is not True:
                log.error("%s has unexpected nmdl.chunked: %s" % (self.content_context, nmdl_chunked))

            if nmdl_chunk_threshold != 50:
                log.error("%s has unexpected nmdl.chunk_threshold: %s" % (self.content_context, nmdl_chunk_threshold))

            group_elem = etree.SubElement(parent, "g")

            if location_id:
                group_elem.set("id", location_id)

        elif nmdl_type == "nmdl.stroke":
            nmdl_brush_type = content.pop("nmdl.brush_type", None)
            nmdl_color = content.pop("nmdl.color", None)
            nmdl_random_seed = content.pop("nmdl.random_seed", None)
            nmdl_stroke_bounds = content.pop("nmdl.stroke_bounds", None)
            nmdl_thickness = float(content.pop("nmdl.thickness", None))

            nmdl_stroke_points = content.pop("nmdl.stroke_points", {})
            nmdl_num_points = nmdl_stroke_points.pop("nmdl.num_points", 0)

            nmdl_stroke_values = {}
            for name in [
                    "nmdl.position_x", "nmdl.position_y", "nmdl.density_adjust_factor", "nmdl.thickness_adjust_factor",
                    "nmdl.tilt_x", "nmdl.tilt_y", "nmdl.pressure"]:
                if name in nmdl_stroke_points:
                    nmdl_stroke_values[name] = decode_stroke_values(nmdl_stroke_points.pop(name), nmdl_num_points, name)
                else:
                    nmdl_stroke_values[name] = []

            self.check_empty(nmdl_stroke_points, "%s nmdl_stroke_points" % self.content_context)

            bound_width = nmdl_stroke_bounds[2] - nmdl_stroke_bounds[0]
            bound_height = nmdl_stroke_bounds[3] - nmdl_stroke_bounds[1]

            if nmdl_color != 0:
                log.error("Unexpected color %d" % nmdl_color)

            opacity = 1.0

            for daf in nmdl_stroke_values["nmdl.density_adjust_factor"]:
                if daf != 100:
                    variable_density = True
                    break
            else:
                variable_density = False

            for taf in nmdl_stroke_values["nmdl.thickness_adjust_factor"]:
                if taf != 100:
                    variable_thickness = True
                    break
            else:
                variable_thickness = False

            if nmdl_brush_type == 0:
                brush_name = ORIGINAL_PEN
            elif nmdl_brush_type == 1:
                brush_name = HIGHLIGHTER
                opacity = 0.2
            elif nmdl_brush_type == 5:
                brush_name = PENCIL
            elif nmdl_brush_type == 6:
                brush_name = FOUNTAIN_PEN
            elif nmdl_brush_type == 7:
                brush_name = MARKER if variable_thickness else PEN
            else:
                log.error("Unexpected brush type %d" % nmdl_brush_type)
                brush_name = UNKNOWN + str(nmdl_brush_type)

            for thickness_index, thickness_choice in enumerate(THICKNESS_CHOICES.get(brush_name, [])):
                if abs(thickness_choice - nmdl_thickness) / thickness_choice < 0.01:
                    thickness_name = THICKNESS_NAME[thickness_index]
                    break
            else:
                log.warning("Unexpected thickness %s for %s" % (nmdl_thickness, brush_name))
                thickness_name = "%1.3f" % nmdl_thickness

            thickness = round(nmdl_thickness)
            last_x = last_y = None
            points = []

            for i in range(nmdl_num_points):

                x = nmdl_stroke_values["nmdl.position_x"][i] + nmdl_stroke_bounds[0]
                y = nmdl_stroke_values["nmdl.position_y"][i] + nmdl_stroke_bounds[1]
                taf = nmdl_stroke_values["nmdl.thickness_adjust_factor"][i] if variable_thickness else 100
                daf = nmdl_stroke_values["nmdl.density_adjust_factor"][i] if variable_density else 100

                if x < nmdl_stroke_bounds[0] or x > nmdl_stroke_bounds[2] or y < nmdl_stroke_bounds[1] or y > nmdl_stroke_bounds[3]:
                    log.error("point %d position out of range: (%d, %d) with bounds %s" % (i, x, y, nmdl_stroke_bounds))

                if taf < MIN_TAF or taf > MAX_TAF:
                    log.error("point %d thickness_adjust_factor out of range: %d" % (i, taf))

                if daf < MIN_DAF or daf > MAX_DAF:
                    log.error("point %d density_adjust_factor out of range: %d" % (i, daf))

                if QUANTIZE_THICKNESS:
                    taf = (taf // 10) * 10

                t = round(nmdl_thickness * taf / 100.0)

                d = daf / 100.0

                if x != last_x or y != last_y:
                    points.append((x, y, t, d))

                last_x, last_y = x, y

            if opacity < 1.0:
                svg_elem = parent
                while svg_elem.tag != SVG:
                    svg_elem = svg_elem.parent

                opacity_str = "%1.2f" % opacity
                for opacity_group_elem in svg_elem:
                    if opacity_group_elem.tag == "g" and opacity_group_elem.get("opacity", "") == opacity_str:
                        break
                else:
                    opacity_group_elem = etree.SubElement(svg_elem, "g")
                    opacity_group_elem.set("opacity", opacity_str)

                parent = opacity_group_elem

            group_elem = etree.SubElement(parent, "g")

            if location_id:
                group_elem.set("id", location_id)

            desc_elem = etree.SubElement(group_elem, "desc")
            desc_elem.text = "%s %s" % (brush_name, thickness_name)

            if False:
                pass

            elif variable_density:
                group_elem.set("stroke", "none")
                group_elem.set("fill", self.color_str(nmdl_color))

            else:
                group_elem.set("fill", "none")
                group_elem.set("stroke", self.color_str(nmdl_color))
                group_elem.set("stroke-width", "%d" % thickness)

                if ROUND_LINE_ENDINGS:
                    group_elem.set("stroke-linejoin", "round")
                    group_elem.set("stroke-linecap", "round")

            if "$98" in content:
                group_elem.set("transform", self.process_transform(content.pop("$98"), True))

            if False:
                pass

            elif variable_density:
                def add_points_if_needed(pts, x1, y1, r1, d1, x2, y2, r2, d2):
                    distance = math.dist((x1, y1), (x2, y2))
                    if distance > max(r1, r2, 2):
                        x3 = (x1 + x2) // 2
                        y3 = (y1 + y2) // 2
                        r3 = (r1 + r2) // 2
                        d3 = (d1 + d2) // 2
                        add_points_if_needed(pts, x1, y1, r1, d1, x3, y3, r3, d3)
                        add_points_if_needed(pts, x3, y3, r3, d3, x2, y2, r2, d2)
                        pts.append((x3, y3, r3, d3))

                pts = []
                last_x = last_y = last_r = last_d = None
                for x, y, t, d in points:
                    x0 = (x - nmdl_stroke_bounds[0]) // PNG_SCALE_FACTOR
                    y0 = (y - nmdl_stroke_bounds[1]) // PNG_SCALE_FACTOR
                    r0 = t / (PNG_SCALE_FACTOR * 2)

                    if last_x is not None:
                        add_points_if_needed(pts, last_x, last_y, last_r, last_d, x0, y0, r0, d)

                    pts.append((x0, y0, r0, d))
                    last_x, last_y, last_r, last_d = x0, y0, r0, d

                prng = random.Random()
                if nmdl_random_seed is not None:
                    prng.seed(nmdl_random_seed)

                png_width = bound_width // PNG_SCALE_FACTOR
                png_height = bound_height // PNG_SCALE_FACTOR
                density_map = [0] * (png_width * png_height)

                for x, y, r, d in pts:
                    adjusted_d = 1.0 - ((1.0 - min(max(d, 0.0), 1.0)) ** PNG_DENSITY_GAMMA)

                    int_radius = int(math.ceil(r * 1.5))
                    for xx in range(x - int_radius, x + int_radius + 1):
                        for yy in range(y - int_radius, y + int_radius + 1):
                            if xx >= 0 and yy >= 0 and xx < png_width and yy < png_height:
                                i = xx + (yy * png_width)
                                rel_distance = math.dist((x, y), (xx, yy)) / r
                                if rel_distance <= PNG_EDGE_FEATHERING:
                                    if density_map[i] < adjusted_d:
                                        density_map[i] = adjusted_d
                                elif rel_distance <= prng.random() * (2.0 - PNG_EDGE_FEATHERING):
                                    reduced_d = adjusted_d * ((2.0 - PNG_EDGE_FEATHERING) - rel_distance)
                                    if density_map[i] < reduced_d:
                                        density_map[i] = reduced_d

                png_data = []
                for adjusted_d in density_map:
                    png_data.append(0 if prng.random() < adjusted_d else 1)

                with disable_debug_log():
                    png = Image.new("P" if nmdl_color != 0 else "1", (png_width, png_height))

                    if png.mode == "P":
                        png.putpalette(
                            [(nmdl_color >> 16) & 255, (nmdl_color >> 8) & 255, nmdl_color & 255, 0, 0, 0],
                            rawmode="RGB")

                    png.putdata(png_data)
                    outfile = io.BytesIO()
                    png.save(outfile, "PNG", transparency=1, optimize=True)
                    png.close()

                image_data = outfile.getvalue()
                outfile.close()

                etree.SubElement(group_elem, "image", attrib={
                    "x": "%d" % nmdl_stroke_bounds[0], "y": "%d" % nmdl_stroke_bounds[1],
                    "width": "%d" % bound_width, "height": "%d" % bound_height,
                    XLINK_HREF: "data:image/png;base64,%s" % (base64.b64encode(image_data).decode("ascii"))})

            else:
                prev_t = prev_d = None
                paths = []

                for i, (x, y, t, d) in enumerate(points):
                    if i == 0 or t != prev_t or d != prev_d:
                        path = []
                        paths.append((path, t, d))

                        for j in [2, 1] if INCLUDE_PRIOR_LINE_SEGMENT else [1]:
                            if i >= j:
                                path.append((points[i-j][0], points[i-j][1]))

                    path.append((x, y))
                    prev_t, prev_d = t, d

                for path, t, d in paths:
                    if len(path) > 1:
                        path_elem = etree.SubElement(group_elem, "path")

                        if t != nmdl_thickness:
                            path_elem.set("stroke-width", "%d" % round(t))

                        z = []
                        for x, y in path:
                            z.append("%s %d %d" % ("L" if z else "M", x, y))
                        path_elem.set("d", " ".join(z))
                    else:
                        pass

        else:
            log.error("%s has unknown nmdl.type: %s" % (self.content_context, nmdl_type))


def adjust_color_for_density(color, density):
    r = (color >> 16) & 255
    g = (color >> 8) & 255
    b = color & 255
    lum = (r + g + b) // 3
    lum2 = min(max(round(255 - int((255 - lum) * density)), 0), 255)
    return (lum2 << 16) + (lum2 << 8) + lum2


def decode_stroke_values(data, num_points, name):
    error = False
    serial = Deserializer(data)

    signature = serial.extract(2)
    if signature != b"\x01\x01":
        log.error("%s signature is incorrect (%s)" % (name, signature.hex()))
        error = True

    num_vals = serial.unpack("<I")
    if num_vals != num_points:
        log.error("%s expected %d values, found %d" % (name, num_points, num_vals))
        error = True

    if len(serial) * 2 < num_vals:
        log.error("%s not enough data (%d bytes) to extract %d values" % (name, len(serial), num_vals))
        return

    instrs = []
    while len(instrs) < num_vals:
        b = serial.unpack("B")
        instrs.append(b >> 4)
        instrs.append(b & 0x0f)

    if len(instrs) > num_vals:
        pad = instrs.pop(-1)
        if pad != 0:
            log.error("%s incorrect padding value %d" % (name, pad))
            error = True

    vals = []
    for i in range(num_vals):
        instr = instrs[i]
        n = instr & 3

        if instr & 4:
            increment = n
        else:
            if len(serial) < n:
                log.error("%s pos %d instr %d - out of data" % (name, i, instr))
                error = True
                break

            if n == 0:
                increment = 0
            elif n == 1:
                increment = serial.unpack("B")
            elif n == 2:
                increment = serial.unpack("<H")
            else:
                log.error("%s pos %d instr %d - check number of bytes" % (name, i, instr))
                error = True
                increment = serial.unpack("B")
                increment += serial.unpack("<H") << 8

        if instr & 8:
            if increment == 0:
                log.error("%s pos %d instr %d - negative zero increment" % (name, i, instr))
                error = True

            increment = -increment

        if i == 0:
            change = 0
            value = increment
        else:
            change += increment
            value += change

        vals.append(value)

    if len(serial):
        log.error("%s has extra data: %s" % (name, serial.extract().hex()))
        error = True

    if error:
        log.info("%s raw: %s" % (name, data.hex()))
        log.info("%s values: %s" % (name, vals))

    return vals
