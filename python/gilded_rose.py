# -*- coding: utf-8 -*-

SULFURAS = "Sulfuras, Hand of Ragnaros"
BACKSTAGE_PASSES = "Backstage passes to a TAFKAL80ETC concert"
AGED_BRIE = "Aged Brie"
CONJURED = "Conjured"
min_quality = 0
max_quality = 50


class GildedRose(object):

    def __init__(self, items):
        self.items = items

    @staticmethod
    def is_conjured(item):
        """
        Check whether an item is conjured
        :type item: Item
        """
        return item.name.split(" ")[0] == CONJURED

    @staticmethod
    def get_pass_quality_change(item):
        """
        Process the quality change in an aging backstage pass, according to
        - Quality increases by 2 when there are 10 days or less
        - Increases by 3 when there are 5 days or less
        - Quality drops to 0 after the concert
        :param item: Item
        :return the numerical change in backstage pass quality
        """
        if item.sell_in > 10:
            return 1
        elif item.sell_in > 5:
            return 2
        elif item.sell_in >= 0:
            return 3
        else:
            return -item.quality

    def update_quality(self):
        """
        Iterate over all available items and modify their qualities and sell dates according to the following
            - Once the sell by date has passed, Quality degrades twice as fast
            - The Quality of an item is never negative
            - "Aged Brie" actually increases in Quality the older it gets
            - The Quality of an item is never more than 50
            - "Sulfuras", being a legendary item, never has to be sold or decreases in Quality
            - "Backstage passes", like aged brie, increases in Quality as its SellIn value approaches;
            Quality increases by 2 when there are 10 days or less and by 3 when there are 5 days or less but
            Quality drops to 0 after the concert
            - "Conjured" items degrade in Quality twice as fast as normal items
        :return: none
        """
        for item in self.items:
            # We don't need to do anything with the legendary Hand of Ragnaros
            # Side note: I was taught in school that "break" and "continue" were a sin and could always be replicated
            # with normal boolean logic in the loop, or with b i g "if" statements. This could be done this way, but
            # it would sure be ugly and pointless, since it can be kept right at the top.
            if item.name == SULFURAS:
                continue

            # Default items lose one quality each day
            quality_delta = -1

            # If the item has special rules on its quality, get the special number
            if item.name == BACKSTAGE_PASSES:
                quality_delta = GildedRose.get_pass_quality_change(item)
            elif item.name == AGED_BRIE:
                quality_delta = 1
            elif GildedRose.is_conjured(item):
                quality_delta = -2

            # If the item is expired, quality change is doubled
            if item.sell_in < 0:
                quality_delta *= 2

            # Apply the sell_by and quality changes and check that we haven't walked out of bounds
            item.sell_in -= 1
            item.quality += quality_delta
            item.quality = max(item.quality, 0)
            item.quality = min(item.quality, 50)

        # for item in self.items:
        #     if item.name != "Aged Brie" and item.name != "Backstage passes to a TAFKAL80ETC concert":
        #         if item.quality > 0:
        #             if item.name != "Sulfuras, Hand of Ragnaros":
        #                 item.quality = item.quality - 1
        #     else:
        #         if item.quality < 50:
        #             item.quality = item.quality + 1
        #             if item.name == "Backstage passes to a TAFKAL80ETC concert":
        #                 if item.sell_in < 11:
        #                     if item.quality < 50:
        #                         item.quality = item.quality + 1
        #                 if item.sell_in < 6:
        #                     if item.quality < 50:
        #                         item.quality = item.quality + 1
        #     if item.name != "Sulfuras, Hand of Ragnaros":
        #         item.sell_in = item.sell_in - 1
        #     if item.sell_in < 0:
        #         if item.name != "Aged Brie":
        #             if item.name != "Backstage passes to a TAFKAL80ETC concert":
        #                 if item.quality > 0:
        #                     if item.name != "Sulfuras, Hand of Ragnaros":
        #                         item.quality = item.quality - 1
        #             else:
        #                 item.quality = item.quality - item.quality
        #         else:
        #             if item.quality < 50:
        #                 item.quality = item.quality + 1


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
