from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Identity

class HouseLoader(ItemLoader):
    default_output_processor = TakeFirst()

    # Ensure the data_frame field processes a list of dictionaries correctly
    data_frame_in = MapCompose(lambda x: x)
    data_frame_out = Identity()
