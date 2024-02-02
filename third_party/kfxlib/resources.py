from __future__ import (unicode_literals, division, absolute_import, print_function)


import io
import os
from PIL import Image
import time
import zipfile

try:
    import pypdf
except ImportError:
    try:
        from . import pypdf
    except ImportError:
        pypdf = None

from .jxr_container import JXRContainer
from .message_logging import log
from .utilities import (calibre_numeric_version, create_temp_dir, disable_debug_log, list_symbols, temp_filename)


MIN_JPEG_QUALITY = 80
MAX_JPEG_QUALITY = 100
COMBINED_TILE_SIZE_FACTOR = 1.2
TILE_SIZE_REPORT_PERCENTAGE = 20
DEBUG_TILES = False

IMAGE_COLOR_MODES = [
    "1",
    "L",
    "P",
    "RGB",
    ]

IMAGE_OPACITY_MODE = "A"


FORMAT_SYMBOLS = {
    "bmp": "$599",
    "gif": "$286",
    "jpg": "$285",
    "jxr": "$548",
    "pbm": "$420",
    "pdf": "$565",
    "png": "$284",
    "pobject": "$287",
    "tiff": "$600",
    "bpg": "$612",
    }

SYMBOL_FORMATS = {}
for k, v in FORMAT_SYMBOLS.items():
    SYMBOL_FORMATS[v] = k


MIMETYPE_OF_EXT = {
    ".apnx": "application/x-apnx-sidecar",
    ".bin": "application/octet-stream",
    ".bmp": "image/bmp",
    ".css": "text/css",
    ".eot": "application/vnd.ms-fontobject",
    ".dfont": "application/x-dfont",
    ".epub": "application/epub+zip",
    ".gif": "image/gif",
    ".htm": "text/html",
    ".html": "text/html",
    ".ico": "image/x-icon",
    ".jpeg": "image/jpeg",
    ".jpg": "image/jpeg",
    ".js": "text/javascript",
    ".jxr": "image/vnd.ms-photo",
    ".kvg": "image/kvg",
    ".mp3": "audio/mpeg",
    ".mp4": "video/mp4",
    ".mpg": "video/mpeg",
    ".ncx": "application/x-dtbncx+xml",
    ".opf": "application/oebps-package+xml",
    ".otf": "font/otf",
    ".pfb": "application/x-font-type1",
    ".png": "image/png",
    ".pdf": "application/pdf",
    ".pobject": "application/azn-plugin-object",
    ".svg": "image/svg+xml",
    ".tif": "image/tiff",
    ".tiff": "image/tiff",
    ".ttf": "font/ttf",
    ".txt": "text/plain",
    ".webp": "image/webp",
    ".woff": "application/font-woff",
    ".woff2": "font/woff2",
    ".xhtml": "application/xhtml+xml",
    ".xml": "application/xml",
    }

EPUB2_ALT_MIMETYPES = {
    "font/ttf": "application/x-font-truetype",
    "font/otf": "application/x-font-otf",
    }

RESOURCE_TYPE_OF_EXT = {
    ".bmp": "image",
    ".css": "styles",
    ".eot": "font",
    ".dfont": "font",
    ".gif": "image",
    ".htm": "text",
    ".html": "text",
    ".ico": "image",
    ".jpg": "image",
    ".js": "text",
    ".jxr": "image",
    ".kvg": "image",
    ".mp3": "audio",
    ".mp4": "video",
    ".otf": "font",
    ".pdf": "image",
    ".png": "image",
    ".svg": "image",
    ".tif": "image",
    ".tiff": "image",
    ".ttf": "font",
    ".txt": "text",
    ".webp": "video",
    ".woff": "font",
    }

EXTS_OF_MIMETYPE = {
    "application/azn-plugin-object": [".pobject"],
    "application/epub+zip": [".epub"],
    "application/font-sfnt": [".ttf", ".otf"],
    "application/font-woff": [".woff"],
    "application/font-woff2": [".woff2"],
    "application/javascript": [".js", ".jsonp", ".json"],
    "application/json": [".json"],
    "application/json+ea": [".json"],
    "application/json+xray": [".json"],
    "application/ocsp-response": [".ocsp"],
    "application/octet-stream": [".bin"],
    "application/oebps-package+xml": [".opf"],
    "application/pdf": [".pdf"],
    "application/protobuf": [".bin"],
    "application/sql+xray": [".db"],
    "application/vnd.adobe-page-template+xml": [".xpgt"],
    "application/vnd.amazon.ebook": [".azw"],
    "application/vnd.ms-fontobject": [".eot"],
    "application/vnd.ms-opentype": [".otf", ".ttf"],
    "application/vnd.ms-sync.wbxml": [".xml"],
    "application/x-amz-json-1.1": [".json"],
    "application/x-amzn-ion": [".ion"],
    "application/x-apnx-sidecar": [".apnx"],
    "application/x-bzip": [".bz"],
    "application/x-bzip2": [".bz2"],
    "application/x-dfont": [".dfont"],
    "application/x-dtbncx+xml": [".ncx"],
    "application/x-font-otf": [".otf"],
    "application/x-font-truetype": [".ttf"],
    "application/x-font-ttf": [".ttf"],
    "application/x-font-woff": [".woff"],
    "application/x-javascript": [".js"],
    "application/x-kfx-ebook": [".kfx", ".azw8", ".azw9"],
    "application/x-kfx-magazine": [".kfx"],
    "application/x-mobi8-ebook": [".azw3"],
    "application/x-mobi8-images": [".azw6"],
    "application/x-mobipocket-ebook-mop": [".azw4"],
    "application/x-font-type1": [".pfb"],
    "application/x-rar-compressed": [".rar"],
    "application/x-protobuf": [".bin"],
    "application/x-tar": [".tar"],
    "application/x-x509-ca-cert": [".der"],
    "application/xhtml+xml": [".xhtml", ".html", ".htm"],
    "application/xml": [".xml"],
    "application/xml+phl": [".xml"],
    "application/xml-dtd": [".dtd"],
    "application/xslt+xml": [".xslt"],
    "application/zip": [".zip"],
    "application/zip+mpub": [".zip"],
    "audio": [".mp3"],
    "audio/mp3": [".mp4"],
    "audio/mp4": [".mp4"],
    "audio/mpeg": [".mp3"],
    "figure": [".figure"],
    "font/otf": [".otf"],
    "font/ttf": [".ttf"],
    "font/woff": [".woff"],
    "font/woff2": [".woff2"],
    "image/bmp": [".bmp"],
    "image/gif": [".gif"],
    "image/jpeg": [".jpg", ".jpeg"],
    "image/jpg": [".jpg", ".jpeg"],
    "image/jxr": [".jxr"],
    "image/png": [".png"],
    "image/svg+xml": [".svg"],
    "image/tiff": [".tif", ".tiff"],
    "image/vnd.djvu": [".djvu"],
    "image/vnd.ms-photo": [".jxr"],
    "image/vnd.jxr": [".jxr"],
    "image/webp": [".webp"],
    "image/x-icon": [".ico"],
    "plugin/kfx-html-article": [".html"],
    "res/bin": [".bin"],
    "res/img": [".png"],
    "res/kvg": [".kvg"],
    "text/css": [".css"],
    "text/csv": [".csv"],
    "text/html": [".html", ".htm"],
    "text/json": [".json"],
    "text/javascript": [".js"],
    "text/plain": [".txt"],
    "text/xml": [".xml"],
    "video": [".mp4"],
    "video/h264": [".mp4"],
    "video/mp4": [".mp4"],
    "video/mpeg": [".mpg"],
    "video/ogg": [".ogg"],
    "video/webm": [".webm"],
    }


class ImageResource(object):
    def __init__(self, format, location, raw_media, height=None, width=None, png_from_jpg=False):
        self.format = format
        self.location = location
        self.raw_media = raw_media
        self.height = height
        self.width = width
        self.png_from_jpg = png_from_jpg


class PdfImageResource(ImageResource):
    def __init__(self, location, raw_media, page_index, total_pages, png_from_jpg=False):
        ImageResource.__init__(self, "$565", location, raw_media, png_from_jpg=png_from_jpg)
        self.page_nums = [page_index + 1]
        self.total_pages = total_pages

    def entire_resource_used(self):
        return self.page_nums == list(range(1, self.total_pages + 1))


def convert_jxr_to_tiff(jxr_data, resource_name):

    if calibre_numeric_version is not None:

        try:
            from calibre.utils.img import (load_jxr_data, image_to_data)
            img = load_jxr_data(jxr_data)
            tiff_data = image_to_data(img, fmt="TIFF")

            if tiff_data:
                return tiff_data
        except Exception as e:
            log.warning("Conversion of JPEG-XR resource failed: %s" % repr(e))

        log.info("Using fallback JPEG-XR conversion for %s" % resource_name)

    start_time = time.time()

    im = JXRContainer(jxr_data).unpack_image()

    duration = time.time() - start_time
    if duration >= 5.0:
        log.info("JPEG-XR to TIFF conversion took %0.1f sec" % duration)

    outfile = io.BytesIO()
    with disable_debug_log():
        im.save(outfile, "TIFF")
        im.close()
        del im

    return outfile.getvalue()


def convert_pdf_to_jpeg(pdf_data, page_num, dpi=150, reported_errors=None):
    pdf_file = temp_filename("pdf", pdf_data)
    jpeg_dir = create_temp_dir()

    if calibre_numeric_version is not None:

        if dpi != 150:
            raise Exception("calibre PDF page_images supports only default 150dpi")

        from calibre.ebooks.metadata.pdf import page_images
        page_images(pdf_file, jpeg_dir, first=page_num, last=page_num)

    for dirpath, dirnames, filenames in os.walk(jpeg_dir):
        if len(filenames) != 1:
            raise Exception("pdftoppm created %d files" % len(filenames))

        if not (filenames[0].endswith(".jpg") or filenames[0].endswith(".jpeg")):
            raise Exception("pdftoppm created unexpected file: %s" % filenames[0])

        with io.open(os.path.join(dirpath, filenames[0]), "rb") as of:
            jpeg_data = of.read()

        break
    else:
        raise Exception("pdftoppm created no files")

    return jpeg_data


def convert_image_to_pdf(image_resource):
    if image_resource.format == "$565":
        return image_resource

    image_data = image_resource.raw_media

    if image_resource.format == "$548":
        try:
            image_data = convert_jxr_to_tiff(image_data, image_resource.location)
        except Exception as e:
            raise Exception("Exception during conversion of JPEG-XR '%s' to TIFF: %s" % (
                image_resource.location, repr(e)))

    pdf_file = io.BytesIO()

    with disable_debug_log():
        image = Image.open(io.BytesIO(image_data))
        image = image.convert("RGB")
        image.save(pdf_file, "pdf", save_all=True)
        image.close()

    pdf_data = pdf_file.getvalue()
    pdf_file.close()

    return PdfImageResource(image_resource.location, pdf_data, 0, 1)


def combine_images_into_pdf(ordered_images):
    if len(ordered_images) == 0:
        return None

    if pypdf is None:
        log.error("pypdf package is missing. Unable to create PDF")
        return None

    image_resource_formats = set()
    combined_pdf_images = []
    for image_resource in ordered_images:
        image_resource_formats.add(SYMBOL_FORMATS[image_resource.format].upper())
        if image_resource.format == "$565":
            if (combined_pdf_images and combined_pdf_images[-1].format == "$565" and combined_pdf_images[-1].location == image_resource.location
                    and len(set(image_resource.page_nums) & set(combined_pdf_images[-1].page_nums)) == 0):
                combined_pdf_images[-1].page_nums.extend(image_resource.page_nums)
            else:
                raw_media_file = io.BytesIO(image_resource.raw_media)
                pdf = pypdf.PdfReader(raw_media_file)
                image_resource.total_pages = len(pdf.pages)
                combined_pdf_images.append(image_resource)
        else:
            combined_pdf_images.append(convert_image_to_pdf(image_resource))

    if len(combined_pdf_images) == 1 and combined_pdf_images[0].entire_resource_used():
        return combined_pdf_images[0].raw_media

    try:
        merger = pypdf.PdfMerger()

        for image_resource in combined_pdf_images:
            if not image_resource.entire_resource_used():
                log.warning("Using PDF %s pages %s of %d" % (
                    image_resource.location, image_resource.page_nums, image_resource.total_pages))

            merger.append(fileobj=io.BytesIO(image_resource.raw_media), pages=None if image_resource.entire_resource_used() else image_resource.page_nums)

        merged_file = io.BytesIO()
        merger.write(merged_file)
        pdf_data = merged_file.getvalue()
        merged_file.close()
    except Exception as e:
        log.error("PdfMerger error: %s" % repr(e))
        pdf_data = None

    if pdf_data is not None:
        log.info("Combined %d %s resources into a %d page PDF file" % (
            len(combined_pdf_images), list_symbols(list(image_resource_formats)), len(ordered_images)))

    return pdf_data


def combine_images_into_cbz(ordered_images, lossless):
    if len(ordered_images) == 0:
        return None

    image_resource_formats = set()
    page_images = []
    for image_resource in ordered_images:
        image_resource_formats.add(SYMBOL_FORMATS[image_resource.format].upper())
        if image_resource.format in {"$286", "$285", "$284"}:
            page_images.append(image_resource)
        elif image_resource.format == "$565":
            for page_num in image_resource.page_nums:
                jpeg_data = convert_pdf_to_jpeg(image_resource.raw_media, page_num)
                page_images.append(ImageResource("$285", None, jpeg_data))
        elif image_resource.png_from_jpg:
            page_images.append(ImageResource("$284", None, image_resource.raw_media))
        else:
            image_data = image_resource.raw_media
            if image_resource.format == "$548":
                try:
                    image_data = convert_jxr_to_tiff(image_data, image_resource.location)
                except Exception as e:
                    raise Exception("Exception during conversion of JPEG-XR '%s' to TIFF: %s" % (
                        image_resource.location, repr(e)))

            image = Image.open(io.BytesIO(image_data))
            outfile = io.BytesIO()
            save_format = "png" if lossless else "jpeg"
            image.save(outfile, save_format, optimize=True)
            jpeg_data = outfile.getvalue()
            outfile.close()
            page_images.append(ImageResource("$285", None, jpeg_data))

    cbz_file = io.BytesIO()

    with zipfile.ZipFile(cbz_file, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for i, image_resource in enumerate(page_images):
            zf.writestr("%04d.%s" % (i + 1, SYMBOL_FORMATS[image_resource.format]), image_resource.raw_media)

    cbz_data = cbz_file.getvalue()
    cbz_file.close()

    log.info("Combined %s resources into a %d page CBZ file" % (
        list_symbols(list(image_resource_formats)), len(ordered_images)))

    return cbz_data


def combine_image_tiles(
        resource_name, resource_height, resource_width, resource_format, tile_height, tile_width, tile_padding,
        yj_tiles, tiles_raw_media, ignore_variants, lossless=False):

    if DEBUG_TILES:
        ncols = len(yj_tiles)
        nrows = len(yj_tiles[0])
        log.warning("tiled image %dx%d: %s" % (nrows, ncols, resource_name))

    with disable_debug_log():
        tile_images = []
        separate_tiles_size = tile_count = 0
        full_image_color_mode = IMAGE_COLOR_MODES[0]
        full_image_opacity_mode = ""

        tile_num = 0
        missing_tiles = []
        for y, row in enumerate(yj_tiles):
            for x, tile_location in enumerate(row):
                tile_raw_media = tiles_raw_media[tile_num]
                if tile_raw_media is not None:
                    tile_count += 1
                    separate_tiles_size += len(tile_raw_media)
                    tile = Image.open(io.BytesIO(tile_raw_media))

                    if tile.mode.endswith(IMAGE_OPACITY_MODE):
                        tile_color_mode = tile.mode[:-1]
                        full_image_opacity_mode = IMAGE_OPACITY_MODE
                    else:
                        tile_color_mode = tile.mode

                    if tile_color_mode not in IMAGE_COLOR_MODES:
                        log.error("Resource %s tile %s has unexpected image mode %s" % (resource_name, tile_location, tile.mode))
                    elif IMAGE_COLOR_MODES.index(tile_color_mode) > IMAGE_COLOR_MODES.index(full_image_color_mode):
                        full_image_color_mode = tile_color_mode
                else:
                    tile = None
                    missing_tiles.append((x, y))

                tile_images.append(tile)
                tile_num += 1

        if missing_tiles:
            log.error("Resource %s is missing tiles: %s" % (resource_name, repr(missing_tiles)))
            if ignore_variants:
                return None

        full_image = Image.new(full_image_color_mode + full_image_opacity_mode, (resource_width, resource_height))

        for y, row in enumerate(yj_tiles):
            top_padding = 0 if y == 0 else tile_padding
            bottom_padding = min(tile_padding, resource_height - tile_height * (y + 1))

            for x, tile_location in enumerate(row):
                left_padding = 0 if x == 0 else tile_padding
                right_padding = min(tile_padding, resource_width - tile_width * (x + 1))

                tile = tile_images.pop(0)
                if tile is not None:
                    twidth, theight = tile.size
                    if twidth != tile_width + left_padding + right_padding or theight != tile_height + top_padding + bottom_padding:
                        log.error("Resource %s tile %d, %d size (%d, %d) does not have padding %d of expected size (%d, %d)" % (
                            resource_name, x, y, twidth, theight, tile_padding, tile_width, tile_height))
                        log.info("tile padding ltrb: %d, %d, %d, %d" % (left_padding, top_padding, right_padding, bottom_padding))

                    crop = (left_padding, top_padding, tile_width + left_padding, tile_height + top_padding)
                    tile = tile.crop(crop)
                    full_image.paste(tile, (x * tile_width, y * tile_height))
                    tile.close()

        if full_image.size != (resource_width, resource_height):
            log.error("Resource %s combined tiled image size is (%d, %d) but should be (%d, %d)" % (
                    resource_name, full_image.size[0], full_image.size[1], resource_width, resource_height))

        fmt = SYMBOL_FORMATS[resource_format]

        if fmt == "jpg":
            desired_combined_size = max(int(separate_tiles_size * COMBINED_TILE_SIZE_FACTOR), 1024)
            min_quality = MIN_JPEG_QUALITY
            max_quality = MAX_JPEG_QUALITY
            best_size_diff = best_quality = raw_media = None

            if lossless:
                outfile = io.BytesIO()
                full_image.save(outfile, "png", optimize=True)
                raw_media = outfile.getvalue()
                outfile.close()

                if DEBUG_TILES:
                    log.warning("Image resource %s has %d tiles %d bytes combined into lossless PNG %d bytes" % (
                        resource_name, tile_count, separate_tiles_size, len(raw_media)))
            else:
                while max_quality >= min_quality:
                    quality = (max_quality + min_quality) // 2
                    outfile = io.BytesIO()
                    full_image.save(outfile, "jpeg", quality=quality, optimize=True)
                    test_raw_media = outfile.getvalue()
                    outfile.close()

                    size_diff = len(test_raw_media) - desired_combined_size

                    if best_size_diff is None or abs(size_diff) < abs(best_size_diff):
                        best_size_diff = size_diff
                        best_quality = quality
                        raw_media = test_raw_media

                    if len(test_raw_media) < desired_combined_size:
                        min_quality = quality + 1
                    else:
                        max_quality = quality - 1

                diff_percentage = (best_size_diff * 100) // desired_combined_size
                if DEBUG_TILES and abs(diff_percentage) > TILE_SIZE_REPORT_PERCENTAGE:
                    log.warning("Image resource %s has %d tiles %d bytes combined into quality %d %s JPEG %d bytes (%+d%%)" % (
                        resource_name, tile_count, separate_tiles_size, best_quality, full_image.mode, len(raw_media), diff_percentage))
        else:
            outfile = io.BytesIO()
            full_image.save(outfile, fmt, optimize=False)
            raw_media = outfile.getvalue()
            outfile.close()

    return raw_media


def get_pdf_page_crop_boxes(pdf_data, resource_name=""):
    page_crop_boxes = {}
    raw_media_file = io.BytesIO(pdf_data)
    pdf = pypdf.PdfReader(raw_media_file)

    for i in range(len(pdf.pages)):
        page_num = i + 1
        page = pdf.pages[i]

        if page.user_unit != 1:
            log.warning("PDF resource %s page %d, user_unit %f -- dimensions are not in points" % (
                resource_name, page_num, page.user_unit))

        page_crop_boxes[page_num] = box_tuple(page.cropbox)

    return page_crop_boxes


def get_pdf_page_size(pdf_data, resource_name, page_num):
    raw_media_file = io.BytesIO(pdf_data)
    pdf = pypdf.PdfReader(raw_media_file)
    page = pdf.pages[page_num - 1]

    if page.user_unit != 1:
        log.warning("PDF resource %s page %d, user_unit %f -- dimensions are not in points" % (
            resource_name, page_num, page.user_unit))

    crop_width, crop_height = box_size(page.cropbox)
    media_width, media_height = box_size(page.mediabox)

    return (crop_width, crop_height) if crop_width * crop_height <= media_width * media_height else (media_width, media_height)


def show_pdf_page_boxes(pdf_data, resource_name, page_num):
    raw_media_file = io.BytesIO(pdf_data)
    pdf = pypdf.PdfReader(raw_media_file)
    page = pdf.pages[page_num - 1]

    def box_repr(box):
        return "%s size %s" % (repr(box_tuple(box)), repr(box_size(box)))

    log.info("PDF resource %s page %d, user_unit %f" % (resource_name, page_num, page.user_unit))
    log.info("  artbox %s" % box_repr(page.artbox))
    log.info("  bleedbox %s" % box_repr(page.bleedbox))
    log.info("  cropbox %s" % box_repr(page.cropbox))
    log.info("  mediabox %s" % box_repr(page.mediabox))
    log.info("  trimbox %s" % box_repr(page.trimbox))


def box_tuple(box):
    return (box.lower_left[0], box.lower_left[1], box.upper_right[0], box.upper_right[1])


def box_size(box):
    return (box.upper_right[0] - box.lower_left[0], box.upper_right[1] - box.lower_left[1])


def jpeg_type(data, fmt="jpg"):

    if fmt not in ["jpg", "jpeg"]:
        return fmt.upper()

    if not data.startswith(b"\xff\xd8"):
        return "UNKNOWN(%s)" % data[:12].hex()

    if data[2:4] == b"\xff\xe0" and data[6:10] == b"JFIF":
        return "JPEG"

    if data[2:4] == b"\xff\xe1" and data[6:10] == b"Exif":
        return "JPEG/Exif"

    if data[2:4] == b"\xff\xe8":
        return "JPEG/SPIFF"

    if data[2:4] in [b"\xff\xed", b"\xff\xee"]:
        return "JPEG/Adobe"

    if data[2:4] in [b"\xff\xdb", b"\xff\xde"]:
        return "JPEG/no-app-marker"

    return "JPEG/UNKNOWN(%s)" % data[:12].hex()


def font_file_ext(data, default=""):
    if data[0:4] in {b"\x00\x01\x00\x00", b"true", b"typ1"}:
        return ".ttf"

    if data[0:4] == b"OTTO":
        return ".otf"

    if data[0:4] == b"wOFF":
        return ".woff"

    if data[34:36] == b"\x4c\x50" and data[8:12] in {b"\x00\x00\x01\x00", b"\x01\x00\x02\x00", b"\x02\x00\x02\x00"}:
        return ".eot"

    if data[0:4] == b"\x00\x00\x01\x00":
        return ".dfont"

    if data[0:2] == b"\x80\x01" and data[6:24] == b"%!PS-AdobeFont-1.0":
        return ".pfb"

    return default


def image_file_ext(data, default=""):
    if data.startswith(b"GIF87a") or data.startswith(b"GIF89a"):
        return ".gif"

    if data.startswith(b"\xff\xd8\xff"):
        return ".jpg"

    if data.startswith(b"\x49\x49\xbc\x01"):
        return ".jxr"

    if data.startswith(b"\x89PNG\x0d\x0a\x1a\x0a"):
        return ".png"

    if data.startswith(b"%PDF"):
        return ".pdf"

    if data.startswith(b"\x49\x49\x2a\x00") or data.startswith(b"\x4d\x4d\x00\x2a"):
        return ".tif"

    return default


def image_size(data):
    with disable_debug_log():
        cover_im = Image.open(io.BytesIO(data))
        width, height = cover_im.size
        cover_im.close()

    return (width, height)
