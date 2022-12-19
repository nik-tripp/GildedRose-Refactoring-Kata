# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose, SULFURAS, BACKSTAGE_PASSES, AGED_BRIE, CONJURED

CONJURED_PREFIX = CONJURED + " "
TEST_QUALITY = 25


class GildedRoseTest(unittest.TestCase):
    def test_boundaries(self):
        """
        Test that no items (except the Hand of Ragnaros) can have quality not between 0 and 50
        """
        items = [Item("Slime Essence", 1, 0), Item(SULFURAS, 1, 80), Item(BACKSTAGE_PASSES, 1, 50),
                 Item(AGED_BRIE, 1, 50), Item(CONJURED_PREFIX + "Cauldron", 1, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEquals(items[0].quality, 0)
        self.assertEquals(items[1].quality, 80)
        self.assertEquals(items[2].quality, 50)
        self.assertEquals(items[3].quality, 50)
        self.assertEquals(items[4].quality, 0)

    def test_sulfuras(self):
        """
        Test that the Hand of Ragnaros never changes
        """
        item = Item(SULFURAS, 1, 80)
        gilded_rose = GildedRose([item])

        # Updating should change nothing
        gilded_rose.update_quality()
        self.assertEquals(item.sell_in, 1)
        self.assertEquals(item.quality, 80)

    # Wrote this one last because the logic here will take so much extra time to test
    def test_backstage_passes(self):
        """
        Test that backstage passes abide by the following
            - Quality increases by 2 when there are 10 days or less
            - Increases by 3 when there are 5 days or less
            - Quality drops to 0 after the concert
        """
        items = [Item(BACKSTAGE_PASSES, 11, TEST_QUALITY), Item(BACKSTAGE_PASSES, 6, TEST_QUALITY),
                 Item(BACKSTAGE_PASSES, 0, TEST_QUALITY)]
        expected_quality_1 = TEST_QUALITY
        expected_quality_2 = TEST_QUALITY
        expected_quality_3 = TEST_QUALITY
        gilded_rose = GildedRose(items)

        # First item should appreciate by 1, second by 2, third by 3
        gilded_rose.update_quality()
        expected_quality_1 += 1
        expected_quality_2 += 2
        expected_quality_3 += 3
        self.assertEquals(items[0].quality, expected_quality_1)
        self.assertEquals(items[1].quality, expected_quality_2)
        self.assertEquals(items[2].quality, expected_quality_3)

        # Expectations should change on the "breakpoint days"
        self.assertEquals(items[0].sell_in, 10)
        self.assertEquals(items[1].sell_in, 5)
        self.assertEquals(items[2].sell_in, -1)
        gilded_rose.update_quality()
        expected_quality_1 += 2
        expected_quality_2 += 3
        expected_quality_3 = 0
        self.assertEquals(items[0].quality, expected_quality_1)
        self.assertEquals(items[1].quality, expected_quality_2)
        self.assertEquals(items[2].quality, expected_quality_3)

    def test_basics(self):
        """
        Test that basic items lose 1 quality per day until expiring, 2 thereafter
        """
        item = Item("Slime Essence", 1, TEST_QUALITY)
        self.check_standard_progression_and_expiration(item, -1)

    def test_aged_brie(self):
        """
        Test that Aged Brie gains 1 quality each day before sell-by, two thereafter
        """
        item = Item(AGED_BRIE, 1, TEST_QUALITY)
        self.check_standard_progression_and_expiration(item, 1)

    def test_conjured(self):
        """
        Test that conjured items lose two quality each day before sell-by, four thereafter
        """
        item = Item(CONJURED_PREFIX + "Cauldron", 1, TEST_QUALITY)
        self.check_standard_progression_and_expiration(item, -2)

    def check_standard_progression_and_expiration(self, item, daily_change):
        self.assertEquals(item.sell_in, 1)
        expected_quality = item.quality
        gilded_rose = GildedRose([item])

        # One day, daily change
        gilded_rose.update_quality()
        expected_quality += daily_change
        self.assertEquals(item.quality, expected_quality)

        # Should change normally on expiration date
        self.assertEquals(item.sell_in, 0)
        gilded_rose.update_quality()
        expected_quality += daily_change
        self.assertEquals(item.quality, expected_quality)

        # Should have a doubled change after expiring
        self.assertEquals(item.sell_in, -1)
        gilded_rose.update_quality()
        expected_quality += daily_change * 2
        self.assertEquals(item.quality, expected_quality)

    # Love getting a free passing test
    def test_foo(self):
        items = [Item("foo", 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEquals("foo", items[0].name)

        
if __name__ == '__main__':
    unittest.main()
