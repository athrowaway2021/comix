import copy
import io
import os
from PIL import Image

from third_party.kfxlib.ion import IonAnnotation, IonList, IonSExp, IonString, IonStruct, IonSymbol, ion_type
from third_party.kfxlib.yj_book import YJ_Book
from third_party.kfxlib.yj_to_epub import FRAGMENT_NAME_SYMBOL, RETAIN_USED_FRAGMENTS

MIN_JPEG_QUALITY = 95
MAX_JPEG_QUALITY = 100

class KFX_CBZ(YJ_Book):
    def __init__(self, file, ignore_hdv=False, hdv_png=False):
        super().__init__(file)
        self.book_symbols = set()
        self.used_fragments = {}
        self.processed_images = {}
        self.ignore_hdv = ignore_hdv
        self.hdv_png = hdv_png

        self.decode_book()
        
    def get_fragment(self, ftype=None, fid=None, delete=True):
        if ion_type(fid) not in [IonString, IonSymbol]:
            return fid

        if ftype in self.book_data:
            fragment_container = self.book_data[ftype]
        elif ftype == "$393" and "$394" in self.book_data:
            fragment_container = self.book_data["$394"]
        else:
            fragment_container = {}

        data = fragment_container.pop(fid, None) if delete else fragment_container.get(fid)
        if data is None:
            used_data = self.used_fragments.get((ftype, fid))
            if used_data is not None:
                if RETAIN_USED_FRAGMENTS:
                    data = used_data
                else:
                    data = IonStruct()
            else:
                data = IonStruct()
        else:
            self.used_fragments[(ftype, fid)] = copy.deepcopy(data) if RETAIN_USED_FRAGMENTS else True

        return data

    def get_named_fragment(self, structure, ftype=None, delete=True, name_symbol=None):
        return self.get_fragment(ftype=ftype, fid=structure.pop(name_symbol or FRAGMENT_NAME_SYMBOL[ftype]), delete=delete)

    def get_fragment_name(self, fragment_data, ftype, delete=True):
        return self.get_structure_name(fragment_data, FRAGMENT_NAME_SYMBOL[ftype], delete)

    def get_structure_name(self, structure, name_key, delete=True):
        return structure.pop(name_key, None) if delete else structure.get(name_key, None)

    def replace_ion_data(self, f):
        data_type = ion_type(f)

        if data_type is IonAnnotation:
            return self.replace_ion_data(f.value)

        if data_type is IonList:
            return [self.replace_ion_data(fc) for fc in f]

        if data_type is IonSExp:
            return IonSExp([self.replace_ion_data(fc) for fc in f])

        if data_type is IonStruct:
            newf = IonStruct()
            for fk, fv in f.items():
                newf[self.replace_ion_data(fk)] = self.replace_ion_data(fv)

            return newf

        if data_type is IonSymbol:
            self.book_symbols.add(f)

        return f

    def organize_fragments_by_type(self, fragment_list):
        font_count = 0
        categorized_data = {}
        last_container_id = None

        for fragment in fragment_list:
            id = fragment.fid
            self.book_symbols.add(id)

            if fragment.ftype == "$270":
                id = last_container_id = IonSymbol("%s:%s" % (fragment.value.get("$161", ""), fragment.value.get("$409", "")))
            elif fragment.ftype == "$593":
                id = last_container_id
            elif fragment.ftype == "$262":
                id = IonSymbol("%s-font-%03d" % (id, font_count))
                font_count += 1
            elif fragment.ftype == "$387":
                id = IonSymbol("%s:%s" % (id, fragment.value["$215"]))

            dt = categorized_data.setdefault(fragment.ftype, {})

            if id not in dt:
                dt[id] = self.replace_ion_data(fragment.value)

        for category, ids in categorized_data.items():
            if len(ids) == 1:
                id = list(ids)[0]
                if id == category:
                    categorized_data[category] = categorized_data[category][id]

        return categorized_data

    def process_content_list(self, content, num=[0]):
        if "$146" in content:
            contents = content.pop("$146", [])
            for _content in contents:
                self.process_content(_content, num)

    def process_content(self, content, num=[0]):
        if ion_type(content) is IonSymbol:
            self.process_content(self.get_fragment(ftype="$608", fid=content), num)
        
        if "$165" in content:
            resource = content
        else:
            if "$176" in content:
                story = self.get_named_fragment(content, ftype="$259")
                self.process_content_list(story, num)
                
            self.process_content_list(content, num)

            data_type = content.pop("$159", None)

            if not data_type or (data_type != "$270" and data_type != "$271"):
                return
            
            if "$175" in content:
                resource_name = content["$175"]
            elif "$164" in content:
                resource_name = self.get_fragment_name(content, "$164")
            else: 
                return
            resource = self.get_fragment(ftype="$164", fid=resource_name)
            name = resource_name

            if "$635" in resource and not self.ignore_hdv:
                resource_name = resource.pop("$635", [])[0]
                resource = self.get_fragment(ftype="$164", fid=resource_name)

        if name in self.processed_images and (self.ignore_hdv or self.processed_images[name] == "hdv"):
            return

        filename = os.path.join(self.output_path, self.filename_prefix + str(num[0]).zfill(3))

        fixed_height = resource.pop("$67", None)
        fixed_width = resource.pop("$66", None)

        resource_height = resource.pop("$423", None) or fixed_height
        resource_width = resource.pop("$422", None) or fixed_width

        if "$636" in resource and not self.ignore_hdv:
            tile_height = resource.pop("$638")
            tile_width = resource.pop("$637")
            tile_padding = resource.pop("$797", 0)

            full_image = Image.new("RGB", (resource_width, resource_height))
            separate_tiles_size = tile_count = 0

            col = resource.pop("$636")
            for y, row in enumerate(col):
                top_padding = 0 if y == 0 else tile_padding

                for x, location in enumerate(row):
                    left_padding = 0 if x == 0 else tile_padding
                    tile_raw_media = self.book_data["$417"][location]

                    if tile_raw_media is not None:
                        tile_count += 1
                        separate_tiles_size += len(tile_raw_media)
                        tile = Image.open(io.BytesIO(tile_raw_media))

                        crop = (left_padding, top_padding, tile_width + left_padding, tile_height + top_padding)
                        tile = tile.crop(crop)
                        full_image.paste(tile, (x * tile_width, y * tile_height))
                        tile.close()

            if self.hdv_png:
                full_image.save(filename + ".png", "png", optimize=True)
            else:
                min_quality = MIN_JPEG_QUALITY
                max_quality = MAX_JPEG_QUALITY
                best_size_diff = raw_media = None
                while True:
                    quality = (max_quality + min_quality) // 2
                    outfile = io.BytesIO()
                    full_image.save(outfile, "jpeg", quality=quality, subsampling=0, optimize=True)
                    test_raw_media = outfile.getvalue()
                    outfile.close()

                    size_diff = abs(separate_tiles_size - len(test_raw_media))
                    if best_size_diff is None or size_diff < best_size_diff:
                        best_size_diff = size_diff
                        raw_media = test_raw_media

                    if separate_tiles_size > len(test_raw_media):
                        min_quality = quality + 1
                    else:
                        max_quality = quality - 1

                    if max_quality < min_quality:
                        break

                with open(filename + ".jpg", "wb") as f:
                    f.write(raw_media)
            
            self.processed_images[name] = "hdv"
        else:
            raw_media = self.book_data["$417"][resource["$165"]]

            mime = resource.pop("$162", None)
            extension = "." + mime.split("/")[1]

            with open(filename + extension, "wb") as f:
                f.write(raw_media)
            self.processed_images[name] = "normal"
        
        num[0] += 1


    def extract_to_folder(self, output_path, filename_prefix=""):
        self.output_path = output_path
        self.filename_prefix = filename_prefix

        #metadata = self.get_metadata()
        #cover_path = os.path.join(self.output_path, ".cover." + metadata.cover_image_data[0].replace("jpeg","jpg"))
        #with open(cover_path, "wb") as f:
            #f.write(metadata.cover_image_data[1])

        self.book_data = self.organize_fragments_by_type(self.fragments)

        #for content in self.book_data["$259"].items():
            #self.process_content(content[1])
        
        document_data = self.book_data.pop("$538", {})
        reading_orders = document_data.pop("$169", [])
        for reading_order in reading_orders:
            for section_ in reading_order["$170"]:
                section = self.get_fragment(ftype="$260", fid=section_)
                page_templates = section.pop("$141")
                self.process_content(self.get_fragment(ftype="$608", fid=page_templates[0]))
