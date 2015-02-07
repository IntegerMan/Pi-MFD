# coding=utf-8

"""
Handles the "shop" tag
"""
from PiMFD.Applications.Navigation.Tags.TagHandling import TagHandler

__author__ = 'Matt Eland'


class ShopTagHandler(TagHandler):
    """
    Provides information relating to nodes tagged with the 'shop' tag
    """

    def get_color(self, entity, value, cs):

        """

        :type cs: PiMFD.UI.ColorScheme.ColorScheme
        :type entity: MapEntity
        :type value: string
        :rtype : tuple
        """
        if value in ('car', 'car_repair', 'car_parts', 'motorcycle', 'tyres', 'tires'):
            return cs.map_automotive
        elif value in ('alcohol', 'beverages', 'coffee', 'tea', 'wine'):
            return cs.map_commercial
        elif value in ('bakery', 'butcher', 'cheese', 'chocolate', 'confectionery', 'confectionary', 'deli', 'dairy',
                       'farm', 'greengrocer', 'organic', 'pasta', 'pastry', 'seafood', 'supermarket'):
            return cs.map_commercial
        elif value in ('department_store', 'general', 'convenience', 'kiosk', 'mall'):
            return cs.map_commercial
        elif value in ('baby_goods', 'bag', 'botique', 'clothes', 'fabric', 'fashion', 'jewelry', 'leather', 'shoes',
                       'tailor', 'charity', 'second_hand', 'variety_store', 'beauty', 'chemist', 'cosmetics', 'erotic',
                       'games', 'music', 'musical_instrument', 'video_games', 'anime', 'books', 'gift', 'newsagent',
                       'news', 'stationery', 'stationary', 'e-cigarette', 'pet', 'pyrotechnics', 'religion', 'tobacco',
                       'toys', 'weapons'):
            return cs.map_commercial
        elif value in ('drugstore', 'hearing_aids', 'herbalist', 'massage', 'medical_supply', 'optician'):
            return cs.map_health
        elif value in ('hairdresser', 'tattoo', 'locksmith', 'ticket', 'copyshop', 'dry_cleaning', 'funeral_directors',
                       'laundry', 'money_lender', 'pawnbroker', 'travel_agency'):
            return cs.map_service
        elif value in ('energy', 'gas'):
            return cs.map_infrastructure
        elif value in ('vacant', 'abandoned'):
            return cs.map_structural
        elif value in ('florist', 'garden_centre'):
            return cs.map_vegetation
        elif value in ('bathroom_furnishing', 'doityourself', 'furnace', 'garden_furniture', 'glaziery', 'hardware',
                       'houseware', 'paint', 'trade', 'antiques', 'bed', 'candles', 'carpet', 'curtain', 'furniture',
                       'interior_decoration', 'kitchen', 'window_blind', 'craft', 'frame'):
            return cs.map_commercial
        elif value in ('computer', 'electronics', 'hifi', 'mobile_phone', 'radiotechnics', 'vacuum_cleaner'):
            return cs.map_commercial
        elif value in ('bicycle', 'fishing', 'free_flying', 'hunting', 'outdoor', 'scuba_diving', 'water_sports',
                       'sports'):
            return cs.map_commercial
        elif value in ('art', 'photo'):
            return cs.map_commercial

        return super(ShopTagHandler, self).get_color(entity, value, cs)

    def get_description_text(self, entity, value):
        """
        :type entity: MapEntity
        :type value: string
        :rtype: string
        """

        shops = {
            'alcohol': 'Liquor Store',
            'bakery': 'Bakery',
            'beverages': 'Beverage Shop',
            'butcher': 'Butcher\'s Shop',
            'cheese': 'Cheese Shop',
            'chocolate': 'Chocolate Shop',
            'coffee': 'Coffee Shop',
            'confectionery': 'Confectionery',
            'convenience': 'Convenience Store',
            'deli': 'Deli',
            'dairy': 'Dairy',
            'farm': 'Farm Store',
            'greengrocer': 'Vegetable / Fruit Store',
            'organic': 'Organic Foods Store',
            'pasta': 'Pasta Store',
            'seafood': 'Seafood Store',
            'tea': 'Tea Shop',
            'wine': 'Wine Store',
            'department_store': 'Department Store',
            'general': 'General Store',
            'kiosk': 'Kiosk',
            'mall': 'Mall',
            'supermarket': 'Supermarket',
            'baby_goods': 'Baby Store',
            'bag': 'Handbag Store',
            'botique': 'Botique',
            'clothes': 'Clothes Store',
            'fabric': 'Fabric Shop',
            'fashion': 'Fashion Shop',
            'jewelry': 'Jewelry Shop',
            'leather': 'Leather Goods Store',
            'shoes': 'Shoe Store',
            'tailor': 'Tailor',
            'charity': 'Charity Shop',
            'second_hand': 'Thrift Store',
            'variety_store': 'Variety Store',
            'beauty': 'Beauty Shop',
            'chemist': 'Chemist',
            'cosmetics': 'Cosmetics Shop',
            'drugstore': 'Pharmacy',
            'erotic': 'Adult Store',
            'hairdresser': 'Hairdresser',
            'hearing_aids': 'Hearing Aid Shop',
            'herbalist': 'Herbalist',
            'massage': 'Massage Parlor',
            'medical_supply': 'Medical Supply Shop',
            'optician': 'Optitian',
            'tattoo': 'Tattoo Parlor',
            'bathroom_furnishing': 'Bathroom Furnishing Shop',
            'doityourself': 'Home Improvement / DIY Store',
            'energy': 'Energy Vendor',
            'florist': 'Florist',
            'furnace': 'Oven / Furnace Shop',
            'garden_centre': 'Garden Shop',
            'garden_furniture': 'Garden Furniture Shop',
            'gas': 'Gas Vendor',
            'glaziery': 'Glazing Shop',
            'hardware': 'Hardware Shop',
            'houseware': 'Home Goods Store',
            'locksmith': 'Locksmith',
            'paint': 'Paint Shop',
            'trade': 'Trade Shop',
            'antiques': 'Antique Shop',
            'bed': 'Bed / Mattress Store',
            'candles': 'Candle Shop',
            'carpet': 'Carpet Store',
            'curtain': 'Curtain / Drapes Store',
            'furniture': 'Furniture Store',
            'interior_decoration': 'Interior Decoration Store',
            'kitchen': 'Kitchen Goods Store',
            'window_blind': 'Window Blinds Store',
            'computer': 'Computer Store',
            'electronics': 'Electronics Store',
            'hifi': 'Audio Equipment Store',
            'mobile_phone': 'Phone Store',
            'radiotechnics': 'Radio Electronics Store',
            'bicycle': 'Bicycle Shop',
            'car': 'Car Dealership',
            'car_repair': 'Car Repair Shop',
            'car_parts': 'Car Parts',
            'fishing': 'Fishing / Bait Store',
            'free_flying': 'Free Flying Store',
            'hunting': 'Hunting Store',
            'motorcycle': 'Motorcycle Shop',
            'outdoor': 'Outdoor Equipment Store',
            'scuba_diving': 'Scuba Diving Shop',
            'sports': 'Sports Shop',
            'tyres': 'Tire Shop',
            'water_sports': 'Water Sports Shop',
            'art': 'Art Store',
            'craft': 'Craft Shop',
            'frame': 'Frame Shop',
            'games': 'Games Store',
            'music': 'Music Shop',
            'musical_instrument': 'Musical Instrument Store',
            'photo': 'Photography Shop',
            'video': 'Movie / DVD Store',
            'video_games': 'Video Games Store',
            'anime': 'Anime / Comic Store',
            'books': 'Book Store',
            'gift': 'Souveniers / Gift Shop',
            'newsagent': 'Newspaper Shop',
            'stationery': 'Stationery Store',
            'ticket': 'Ticket Vendor',
            'copyshop': 'Copy Shop',
            'dry_cleaning': 'Dry Cleaners',
            'e-cigarette': 'E-Cigarette Vendor',
            'funeral_director': 'Funeral Director',
            'laundry': 'Laundrymat',
            'money_lender': 'Loan Shark',
            'pawnbroker': 'Pawn Shop',
            'pet': 'Pet Shop',
            'pyrotechnics': 'Fireworks Store',
            'religion': 'Religious Store',
            'tobacco': 'Tobacco Vendor',
            'toys': 'Toy Store',
            'travel_agency': 'Travel Agency',
            'vacant': 'Vacant Shop',
            'abandoned': 'Abandoned Shop',
            'weapons': 'Gun / Knife Shop'
        }

        if value in shops:
            return shops[value]

        return super(ShopTagHandler, self).get_description_text(entity, value)