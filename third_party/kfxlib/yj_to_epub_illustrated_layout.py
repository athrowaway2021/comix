from __future__ import (unicode_literals, division, absolute_import, print_function)

from lxml import etree
import urllib.parse

from .message_logging import log
from .utilities import (get_url_filename, urlabspath)
from .yj_to_epub_navigation import visible_elements_before


__license__ = "GPL v3"
__copyright__ = "2016-2023, John Howell <jhowell@acm.org>"


ADD_FINAL_CONTENT = True
EMIT_EMPTY_CONDITIONS = False

EMIT_PAGE_TEMPLATES = False          # emit content inline in KFX Input plugin


class KFX_EPUB_Illustrated_Layout(object):
    CONDITION_OPERATOR_NAMES = {
        "$294": "anchor-id",
        "$299": "range-id.le",
        "$298": "range-id.lt",
        }

    def __init__(self):
        self.has_conditional_content = False

    def fixup_illustrated_layout_anchors(self):
        if not self.has_conditional_content:
            return

        for book_part in self.book_parts:
            body = book_part.body()
            anchor_ids = []
            range_end_ids = []

            for e in body.findall("div"):
                if "style" in e.attrib:
                    style = self.get_style(e)
                    if "-kfx-amzn-condition" in style:
                        oper, anchor = style["-kfx-amzn-condition"].split()
                        url = self.get_anchor_uri(anchor)
                        purl = urllib.parse.urlparse(url)
                        id = purl.fragment

                        if purl.path == book_part.filename and id:
                            style["-kfx-amzn-condition"] = "%s %s" % (oper.partition(".")[0], id)
                            self.set_style(e, style)

                            if oper == "anchor-id":
                                anchor_ids.append(id)
                            else:
                                range_end_ids.append((id, e, oper, anchor))
                        else:
                            log.error("-kfx-amzn-condition anchor %s in file %s links to %s" % (anchor, book_part.filename, url))

            if EMIT_PAGE_TEMPLATES:
                start_idx = 0
                ranges = []

                for id, cond_elem, oper, anchor in range_end_ids:
                    e = id_element = find_by_id(body, id)
                    characters_after = 0

                    while True:
                        p = e.getparent()
                        pidx = p.index(e)

                        if p.tag == "body":
                            end_idx = pidx
                            break

                        while pidx < len(p) - (0 if e is id_element else 1):
                            characters_after += positions_in_tree(p[pidx])
                            pidx += 1

                        e = p

                    if oper == "range-id.lt" and not visible_elements_before(e, body[end_idx]):
                        end_idx -= 1

                    elif characters_after > 1:
                        log.error("Conditional range %s id %s has %d characters following within a top level element in %s" % (
                                oper, id, characters_after, book_part.filename))

                    ranges.append((start_idx, end_idx, id, cond_elem, oper, anchor))
                    start_idx = end_idx + 1

                final_range = True
                master_roots = []
                for range_idx, (start_idx, end_idx, id, cond_elem, oper, anchor) in reversed(list(enumerate(ranges))):

                    range_id = "amzn_master_range_%d" % range_idx
                    self.add_style(cond_elem, {"-kfx-amzn-condition": "%s %s" % (oper.partition(".")[0], range_id)}, replace=True)

                    range_div = etree.Element("div")
                    range_div.set("id", range_id)

                    if end_idx < start_idx:

                        cond_elem.getparent().remove(cond_elem)
                    else:
                        for i in range(end_idx - start_idx + 1):
                            e = body[start_idx]
                            body.remove(e)
                            range_div.append(e)

                        body.insert(start_idx, range_div)
                        master_roots.append(range_div)

                        if final_range and EMIT_PAGE_TEMPLATES and ADD_FINAL_CONTENT:
                            temp_div = etree.Element("div")
                            temp_div.text = "\u200c"
                            self.add_style(temp_div, {
                                "margin-top": "0", "margin-bottom": "0", "margin-left": "0", "margin-right": "0",
                                "padding-top": "0", "padding-bottom": "0", "padding-left": "0", "padding-right": "0"})
                            temp_div.set("id", "extra-content-to-prevent-kpr-failure")
                            body.insert(start_idx + 1, temp_div)
                            final_range = False

                for id in anchor_ids:
                    e = find_by_id(body, id)
                    for root in master_roots:
                        if is_in_tree(root, e):
                            break
                    else:
                        log.error("Conditional anchor id %s not within a master range in %s" % (id, book_part.filename))

    def create_conditional_page_templates(self):
        if not self.has_conditional_content:
            return

        for book_part in self.book_parts:
            css_lines = []
            body = book_part.body()
            for template_elem in body.findall("div"):
                if "style" in template_elem.attrib:
                    template_style = self.get_style(template_elem)
                    amzn_condition = template_style.pop("-kfx-amzn-condition", None)

                    if amzn_condition:

                        inline_content = False
                        pe_lines = []

                        cond_oper, target_id = amzn_condition.split()
                        template_style.pop("-kfx-style-name", None)
                        template_style.pop("-kfx-attrib-epub-type", None)

                        if template_style.get("height", "") == "100%" and template_style.get("width", "") == "100%":
                            template_style.pop("height")
                            template_style.pop("width")

                        base_style = template_style.partition(
                            property_names={"-amzn-page-align", "-kfx-collision"})

                        extra_style = template_style.partition(
                            property_names={"-amzn-page-header", "-amzn-page-footer", "background-color", "color"},
                            keep=True)

                        if extra_style:
                            log.error("Conditional file=%s cond=%s has extra style: %s" % (
                                    book_part.filename, amzn_condition, extra_style.tostring()))
                            log.info("base_style: %s" % base_style.tostring())
                            log.info("template_style: %s" % template_style.tostring())

                        template_children = template_elem.findall("*")
                        for i, template_child in enumerate(template_children):
                            idx = i + 1
                            context = "file=%s cond=%s idx=%d/%d" % (book_part.filename, amzn_condition, idx, len(template_children))

                            if template_child.tag == "div" and len(template_child) > 0:
                                if len(template_child) != 1 or template_child.text or template_child.tail:
                                    log.error("Conditional container %s has incorrect length %d or content" % (
                                            context, len(template_child)))

                                template_child_style = self.get_style(template_child)
                                template_child_style.pop("-kfx-style-name", None)
                                position = template_child_style.pop("position", "")
                                width = template_child_style.pop("width", "")
                                height = template_child_style.pop("height", "")

                                page_align = template_child_style.pop("-amzn-page-align", "")
                                if page_align:
                                    base_style["-amzn-page-align"] = page_align

                                if len(template_child_style) > 0 or position != "fixed" or width != "100%" or height != "100%":
                                    log.error("Conditional container %s has incorrect style: %s" % (
                                            context, template_child.get("style")))

                                pp = template_child.getparent()
                                new_template_child = template_child[0]
                                template_child.remove(new_template_child)
                                pp.insert(pp.index(template_child), new_template_child)
                                pp.remove(template_child)
                                template_child = new_template_child

                            orig_cond_style = self.get_style(template_child)
                            template_child_style = base_style.copy().update(orig_cond_style, replace=True)
                            template_child_style.pop("-kfx-style-name", None)

                            if template_child.tag in ["img", "video"] or (template_child.tag == "div" and "background-color" in template_child_style):
                                remove_child = False
                                position = template_child_style.pop("position", None)
                                if position == "fixed":
                                    for pos, prop_name in [
                                            ("left", "float"), ("right", "float"),
                                            ("top", "-amzn-float"), ("bottom", "-amzn-float")]:
                                        if pos in template_child_style:
                                            val = template_child_style.pop(pos, None)
                                            if val != "0":
                                                log.error("Conditional element %s has non-zero position style: %s" % (
                                                        context, orig_cond_style.tostring()))

                                            if prop_name in template_child_style:
                                                if prop_name == "-amzn-float":
                                                    pos = ",".join([template_child_style[prop_name], pos])
                                                else:
                                                    log.error("Conditional element %s has conflicting position styles: %s" % (
                                                        context, orig_cond_style.tostring()))

                                            template_child_style[prop_name] = pos

                                if template_child_style.get("-amzn-page-align", "") == "none":
                                    template_child_style.pop("-amzn-page-align")

                                is_float = "float" in template_child_style or "-amzn-float" in template_child_style
                                collision = template_child_style.pop("-kfx-collision", "")
                                epub_types = set(template_child_style.pop("-kfx-attrib-epub-type", "").split())

                                if EMIT_PAGE_TEMPLATES:
                                    if ((not is_float) and collision == "queue" and len(template_children) == 1 and cond_oper == "anchor-id"):
                                        inline_content = True

                                        epub_types.add("amzn:full-page")

                                        epub_types.add("amzn:kindle-illustrated")
                                    elif not (is_float and collision in ["", "always queue"]):
                                        log.error("Conditional element %s has conflicting float/collision styles: %s" % (
                                            context, orig_cond_style.tostring()))

                                    if "amzn:decorative" in epub_types:
                                        epub_types.discard("amzn:decorative")
                                        epub_types.discard("amzn:kindle-illustrated")
                                    else:
                                        epub_types.add("amzn:non-decorative")
                                else:
                                    if template_child.tag == "div" or (template_child.tag == "img" and "-amzn-shape-outside" not in template_child_style):
                                        remove_child = True

                                        if template_child.tag == "img":
                                            img_filename = get_url_filename(urlabspath(template_child.get("src"), ref_from=book_part.filename))
                                            self.unreference_resource(img_filename)
                                    else:
                                        template_child_style.pop("-amzn-shape-outside")
                                        template_child_style.pop("-amzn-float")
                                        epub_types.discard("amzn:decorative")
                                        epub_types.discard("amzn:kindle-illustrated")

                                epub_types = " ".join(list(epub_types))
                                if epub_types:
                                    template_child_style["-kfx-attrib-epub-type"] = epub_types

                                if template_child.tag == "div":
                                    template_child_style["display"] = "inline"
                                    template_child.text = ""

                                if remove_child:
                                    template_elem.remove(template_child)

                                elif inline_content:
                                    template_child_style = template_style.update(template_child_style)
                                    template_style = None
                                    self.set_style(template_child, template_child_style)

                                elif template_child_style or EMIT_EMPTY_CONDITIONS:
                                    if EMIT_PAGE_TEMPLATES:
                                        element_id = template_child.get("id", "")
                                        if not element_id:
                                            id_index = 0
                                            while True:
                                                element_id = "%s_element_%d" % (target_id, id_index)
                                                id_index += 1
                                                if find_by_id(body, element_id, required=False) is None:
                                                    break

                                            template_child.set("id", element_id)

                                        target_style = template_child_style.partition(property_names={"-kfx-attrib-epub-type", "background-color", "display"})
                                        self.set_style(template_child, target_style)

                                        pe_lines.append("    @-amzn-page-element %s {" % element_id)

                                        if template_child_style:
                                            self.inventory_style(template_child_style)
                                            pe_lines.append("      %s" % template_child_style.tostring())

                                        pe_lines.append("    }")
                                    else:
                                        self.set_style(template_child, template_child_style)

                            elif (idx == len(template_children) and template_child.tag == "div" and
                                    template_child_style.pop("-amzn-page-align", "") == "none" and
                                    template_child_style.pop("position", "") == "fixed" and
                                    template_child_style.pop("-kfx-collision", "") in ["", "always queue", "queue"] and
                                    len(template_child_style) == 0):

                                story_id = template_child.get("id", "")
                                if story_id:
                                    id_div = etree.Element("div")
                                    id_div.set("id", story_id)
                                    body.insert(0, id_div)

                                template_elem.remove(template_child)

                            else:
                                log.error("Unexpected template_child %s tag=%s style=%s" % (
                                        context, template_child.tag, orig_cond_style.tostring()))

                        target = find_by_id(body, target_id)
                        template_elem.getparent().remove(template_elem)

                        if len(template_elem) == 0:
                            pass
                        elif inline_content:
                            template_elem.tag = "span"
                            template_elem.attrib.pop("style", None)

                            while target.tag not in ["div", "li", "td", "span", "a"]:
                                target = target.getparent()

                            target.insert(0, template_elem)

                        elif not EMIT_PAGE_TEMPLATES:
                            if template_style:
                                self.set_style(template_elem, template_style)
                            else:
                                template_elem.attrib.pop("style", None)

                            while target.tag not in ["div", "li", "td"]:
                                target = target.getparent()

                            if len(template_elem) > 0 or len(template_elem.attrib) > 0 or template_elem.text or EMIT_EMPTY_CONDITIONS:
                                target.insert(0, template_elem)

                        elif pe_lines or template_style or EMIT_EMPTY_CONDITIONS:
                            css_lines.append("@-amzn-master-page {")
                            css_lines.append("  @-amzn-condition(%s) {" % amzn_condition)

                            if template_style:
                                self.inventory_style(template_style)
                                css_lines.append("    %s;" % template_style)

                            css_lines.extend(pe_lines)
                            css_lines.append("  }")
                            css_lines.append("}")

                            template_elem.attrib.pop("style", None)

                            while target.tag not in ["div", "figure", "h1", "h2", "h3", "h4", "h5", "h6", "p"]:
                                target = target.getparent()
                                if target.tag == "body":
                                    raise Exception("Missing block element parent of %s in %s" % (target_id, book_part.filename))

                            if len(template_elem) > 0 or len(template_elem.attrib) > 0 or template_elem.text or EMIT_EMPTY_CONDITIONS:
                                template_elem.set("style", "-kfx-media-query: not amzn-mobi; display: none")

                                target.insert(0, template_elem)

            if css_lines:
                css_file = self.LAYOUT_CSS_FILEPATH % book_part.part_index

                self.link_css_file(book_part, css_file, css_type="text/amzn+css")
                self.manifest_resource(css_file, data="\n".join(css_lines).encode("utf-8"), mimetype="text/amzn+css")


def find_by_id(root, search_id, required=True):
    result = root.xpath(".//*[@id=\"%s\"]" % search_id)
    if len(result) > 0:
        return result[0]

    if not required:
        return None

    raise Exception("could not locate id %s" % search_id)


def positions_in_tree(root):
    count = len(root.text or "") + len(root.tail or "")

    for e in root.iterfind(".//*"):
        if e.tag in ["img", "video"]:
            count += 1
        else:
            count += len(e.text or "") + len(e.tail or "")

    return count


def is_in_tree(root, elem):
    while True:
        if elem is None:
            return False
        if elem is root:
            return True

        elem = elem.getparent()
