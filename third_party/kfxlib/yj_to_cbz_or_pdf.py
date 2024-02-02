from __future__ import (unicode_literals, division, absolute_import, print_function)


from .ion import (ion_type, IonAnnotation, IonList, IonSExp, IonString, IonStruct, IonSymbol)
from .message_logging import log
from .resources import (SYMBOL_FORMATS, combine_images_into_cbz, combine_images_into_pdf, combine_image_tiles, ImageResource, PdfImageResource)
from .yj_container import YJFragmentKey

__license__ = "GPL v3"
__copyright__ = "2016-2023, John Howell <jhowell@acm.org>"

IMAGE_FORMATS = {"$286", "$285", "$548", "$565", "$284"}
USE_HIGHEST_RESOLUTION_IMAGE_VARIANT = True
DEBUG_VARIANTS = False


class KFX_CBZ_OR_PDF(object):
    def __init__(self, book):
        self.book = book

    def convert_book_to_cbz(self, lossless=False):
        return combine_images_into_cbz(self.get_ordered_images(lossless), lossless)

    def convert_book_to_pdf(self, lossless=False):
        return combine_images_into_pdf(self.get_ordered_images(lossless))

    def get_ordered_images(self, lossless=False):

        referenced_resources = self.collect_ordered_image_references()

        unreferenced_resources = set()
        for fragment in self.book.fragments.get_all("$164"):
            resource = fragment.value
            resource_format = resource.get("$161")
            if (resource_format == "$565" and fragment.fid not in referenced_resources and
                    fragment.fid not in unreferenced_resources):
                log.error("Found unreferenced PDF resource: %s" % fragment.fid)
                unreferenced_resources.add(fragment.fid)

        ordered_images = []
        for fid in referenced_resources:
            image_resource = self.get_resource_image(fid, lossless=lossless)
            if image_resource is not None:
                ordered_images.append(image_resource)

        num_pages = self.book.get_page_count()

        if num_pages and len(ordered_images) < num_pages:
            log.warning("Expected %d pages but found only %d page images in book" % (num_pages, len(ordered_images)))

        return ordered_images

    def collect_ordered_image_references(self):
        processed_story_names = set()
        ordered_image_resources = []

        def collect_section_info(section_name):
            pending_story_names = []
            section_image_resources = set()
            section_image_types = set()

            def add_section_resource(resource_name, image_type):
                if resource_name is not None and resource_name not in section_image_resources:
                    fragment = self.book.fragments.get(ftype="$164", fid=resource_name)
                    if fragment is not None:
                        resource = fragment.value
                        if resource.get("$161") in IMAGE_FORMATS:
                            section_image_resources.add(resource_name)
                            section_image_types.add(image_type)
                            ordered_image_resources.append(resource_name)

            def walk_content(data, content_key):
                data_type = ion_type(data)

                if data_type is IonAnnotation:
                    walk_content(data.value, content_key)

                elif data_type is IonList:
                    for i, fc in enumerate(data):
                        if content_key in {"$146", "$274"} and self.book.is_kpf_prepub and ion_type(fc) is IonSymbol:
                            fc = self.book.fragments[YJFragmentKey(ftype="$608", fid=fc)]

                        walk_content(fc, content_key)

                elif data_type is IonSExp:
                    for fc in data:
                        walk_content(fc, content_key)

                elif data_type is IonStruct:
                    annot_type = data.get("$687")
                    typ = data.get("$159")

                    if typ == "$271":
                        add_section_resource(data.get("$175"), "foreground")

                    if "$479" in data:
                        add_section_resource(data["$479"], "background")

                    if "$141" in data:
                        for pt in data["$141"]:
                            if isinstance(pt, IonAnnotation):
                                pt = pt.value

                            walk_content(pt, "$141")

                    if "$683" in data:
                        walk_content(data["$683"], "$683")

                    if "$749" in data:
                        walk_content(self.book.fragments[YJFragmentKey(ftype="$259", fid=data["$749"])], "$259")

                    if "$146" in data:
                        walk_content(data["$146"], "$274" if typ == "$274" else "$146")

                    if "$145" in data and annot_type not in ["$584", "$690"]:
                        fv = data["$145"]
                        if ion_type(fv) is not IonStruct:
                            walk_content(fv, "$145")

                    if "$176" in data and content_key != "$259":
                        fv = data["$176"]

                        if self.book.has_illustrated_layout_conditional_page_template:
                            if fv not in pending_story_names:
                                pending_story_names.append(fv)
                        else:
                            if fv not in processed_story_names:
                                walk_content(self.book.fragments[YJFragmentKey(ftype="$259", fid=fv)], "$259")
                                processed_story_names.add(fv)

                    if "$157" in data:
                        walk_content(self.book.fragments[YJFragmentKey(ftype="$157", fid=data["$157"])], "$157")

                    for fk, fv in data.items():
                        if ion_type(fv) != IonString and fk not in {
                                "$749", "$584", "$683", "$145",
                                "$146", "$141", "$702", "$250", "$176",
                                "yj.dictionary.term", "yj.dictionary.unnormalized_term"}:
                            walk_content(fv, fk)

            walk_content(self.book.fragments[YJFragmentKey(ftype="$260", fid=section_name)], "$260")

            for story_name in pending_story_names:
                if story_name not in processed_story_names:
                    walk_content(self.book.fragments[YJFragmentKey(ftype="$259", fid=story_name)], "$259")
                    processed_story_names.add(story_name)

            if len(section_image_resources) > 2:
                log.error("Section %s contains more than two images", section_name)

            if len(section_image_types) > 1:
                log.error("Section %s contains both background and foreground images", section_name)

        for section_name in self.book.ordered_section_names():
            collect_section_info(section_name)

        return ordered_image_resources

    def get_resource_image(self, resource_name, ignore_variants=False, lossless=False):
        fragment = self.book.fragments.get(ftype="$164", fid=resource_name)
        if fragment is None:
            return None

        resource = fragment.value
        resource_format = resource.get("$161")
        resource_height = resource.get("$423", None) or resource.get("$67", None)
        resource_width = resource.get("$422", None) or resource.get("$66", None)
        page_index = resource.get("$564", 0)

        if "$636" in resource:
            yj_tiles = resource.get("$636")
            tile_height = resource.get("$638")
            tile_width = resource.get("$637")
            tile_padding = resource.get("$797", 0)
            location = yj_tiles[0][0].partition("-tile")[0]

            tiles_raw_media = []
            for row in yj_tiles:
                for tile_location in row:
                    tile_raw_media_frag = self.book.fragments.get(ftype="$417", fid=tile_location)
                    tiles_raw_media.append(None if tile_raw_media_frag is None else tile_raw_media_frag.value)

            raw_media = combine_image_tiles(
                resource_name, resource_height, resource_width, resource_format, tile_height, tile_width, tile_padding,
                yj_tiles, tiles_raw_media, ignore_variants, lossless)
        else:
            location = resource.get("$165")
            if location is not None:
                raw_media = self.book.fragments.get(ftype="$417", fid=location)
                if raw_media is not None:
                    raw_media = raw_media.value
            else:
                raw_media = None

        if resource_format != "$565" and not ignore_variants:
            for rr in resource.get("$635", []):
                variant = self.get_resource_image(rr, ignore_variants=True, lossless=lossless)

                if (USE_HIGHEST_RESOLUTION_IMAGE_VARIANT and variant is not None and
                        variant.width > resource_width and variant.height > resource_height):
                    if DEBUG_VARIANTS:
                        log.info("Replacing image %s (%dx%d) with variant %s (%dx%d)" % (
                                location, resource_width, resource_height, variant.location, variant.width, variant.height))

                    location, raw_media, resource_width, resource_height = variant.location, variant.raw_media, variant.width, variant.height

        if raw_media is None:
            return None

        is_png_from_jpg = bool(SYMBOL_FORMATS[resource_format] == "jpg" and lossless)
        if resource_format == "$565":
            return PdfImageResource(location, raw_media, page_index, None, is_png_from_jpg)

        return ImageResource(resource_format, location, raw_media, resource_height, resource_width, is_png_from_jpg)
