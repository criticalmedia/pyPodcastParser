# -*- coding: utf-8 -*-
import datetime
import os
import unittest

from pyPodcastParser import Podcast

# py.test test_pyPodcastParser.py

#######
# coverage run --source pyPodcastParser -m py.test
#######
# py.test --cov=pyPodcastParser tests/
#######
# py.test -v   --capture=sys tests/test_pyPodcastParser.py


class Test_Test(unittest.TestCase):

    def test_loading_sample_data(self):
        self.assertEqual(True, True)

class Test_Valid_RSS_Check(unittest.TestCase):
    def setUp(self):
        test_dir = os.path.dirname(__file__)
        test_feeds_dir = os.path.join(test_dir, 'test_feeds')
        basic_podcast_path = os.path.join(test_feeds_dir, 'itunes_block_podcast.rss')
        basic_podcast_file = open(basic_podcast_path, "r")
        self.basic_podcast = basic_podcast_file.read()
        self.podcast = Podcast.Podcast(self.basic_podcast)

    def test_is_valid_rss(self):
        self.assertEqual(self.podcast.is_valid_rss, True)

    def test_is_podcast(self):
        self.assertEqual(self.podcast.is_valid_podcast, True)

class Test_Invalid_RSS_Check(unittest.TestCase):
    def setUp(self):
        test_dir = os.path.dirname(__file__)
        test_feeds_dir = os.path.join(test_dir, 'test_feeds')
        basic_podcast_path = os.path.join(test_feeds_dir, 'missing_info_podcast.rss')
        basic_podcast_file = open(basic_podcast_path, "r")
        self.basic_podcast = basic_podcast_file.read()
        self.podcast = Podcast.Podcast(self.basic_podcast)

    def test_is_valid_rss(self):
        self.assertEqual(self.podcast.is_valid_rss, False)

    def test_is_podcast(self):
        self.assertEqual(self.podcast.is_valid_podcast, False)

class Test_Basic_Feed_Item_Blocked(unittest.TestCase):
    def setUp(self):
        test_dir = os.path.dirname(__file__)
        test_feeds_dir = os.path.join(test_dir, 'test_feeds')
        basic_podcast_path = os.path.join(test_feeds_dir, 'itunes_block_podcast.rss')
        basic_podcast_file = open(basic_podcast_path, "r")
        self.basic_podcast = basic_podcast_file.read()
        self.podcast = Podcast.Podcast(self.basic_podcast)

    def test_item_itunes_block(self):
        self.assertEqual(self.podcast.itunes_block, True)

    def test_item_itunes_explicit(self):
        self.assertEqual(self.podcast.items[0].itunes_explicit, "yes")
        self.assertEqual(self.podcast.items[1].itunes_explicit, "highly offensive")

class Test_Basic_Feed_Items(unittest.TestCase):

    def setUp(self):
        test_dir = os.path.dirname(__file__)
        test_feeds_dir = os.path.join(test_dir, 'test_feeds')
        basic_podcast_path = os.path.join(test_feeds_dir, 'basic_podcast.rss')
        basic_podcast_file = open(basic_podcast_path, "r")
        self.basic_podcast = basic_podcast_file.read()
        self.podcast = Podcast.Podcast(self.basic_podcast)

    def test_item_count(self):
        number_of_items = len(self.podcast.items)
        self.assertEqual(number_of_items, 4)

    def test_item_comments(self):
        self.assertEqual(self.podcast.items[0].comments, "http://comments.com/entry/0")
        self.assertEqual(self.podcast.items[1].comments, "http://comments.com/entry/1")
        self.assertEqual(self.podcast.items[2].comments, "http://comments.com/entry/2")

    def test_item_creative_commons(self):
        self.assertEqual(self.podcast.items[0].creative_commons, "http://www.creativecommons.org/licenses/by-nc/1.0")
        self.assertEqual(self.podcast.items[1].creative_commons, None)

    def test_item_categories(self):
        self.assertTrue("Grateful Dead" in self.podcast.items[0].categories)
        self.assertTrue("Dead and Grateful" in self.podcast.items[1].categories)
        self.assertTrue("Dead and Grateful" in self.podcast.items[2].categories)

    def test_item_multi_categories(self):
        self.assertTrue("Grateful Dead" in self.podcast.items[0].categories)
        self.assertTrue("Stones" in self.podcast.items[0].categories)

    def test_item_categories_fail(self):
        self.assertFalse("x" in self.podcast.items[0].categories)
        self.assertFalse("x" in self.podcast.items[1].categories)


    def test_item_description(self):
        self.assertEqual(self.podcast.items[0].description, "basic item description")
        self.assertEqual(self.podcast.items[1].description, "another basic item description")
        self.assertEqual(self.podcast.items[2].description, "another basic item description")
        self.assertEqual(self.podcast.items[3].description, 'this is <a href="https://foo.bar">another basic item description</a>')

    def test_item_description_text(self):
        self.assertEqual(self.podcast.items[0].description_text, "basic item description")
        self.assertEqual(self.podcast.items[1].description_text, "another basic item description")
        self.assertEqual(self.podcast.items[2].description_text, "another basic item description")
        self.assertEqual(self.podcast.items[3].description_text, "this is another basic item description")

    def test_item_itunes_title(self):
        self.assertEqual(self.podcast.items[0].itunes_title, "basic itunes title")
        self.assertEqual(self.podcast.items[1].itunes_title, None)
        self.assertEqual(self.podcast.items[2].itunes_title, "A title with lots of whitespace")
        self.assertEqual(self.podcast.items[3].itunes_title, "<h1>A title with html</h1>")

    def test_item_itunes_title_text(self):
        self.assertEqual(self.podcast.items[0].itunes_title_text, "basic itunes title")
        self.assertEqual(self.podcast.items[1].itunes_title_text, None)
        self.assertEqual(self.podcast.items[2].itunes_title_text, "A title with lots of whitespace")
        self.assertEqual(self.podcast.items[3].itunes_title_text, "A title with html")

    def test_item_author(self):
        self.assertEqual(self.podcast.items[0].author, "lawyer@boyer.net")
        self.assertEqual(self.podcast.items[1].author, "lawyer@boyer.net (Lawyer Boyer)")
        self.assertEqual(self.podcast.items[2].author, "lawyer@boyer.net (Lawyer Boyer)")

    def test_item_itunes_author(self):
        self.assertEqual(self.podcast.items[0].itunes_author_name, "basic item itunes author")
        self.assertEqual(self.podcast.items[1].itunes_author_name, "another basic item itunes author")
        self.assertEqual(self.podcast.items[2].itunes_author_name, "another basic item itunes author")

    def test_item_itunes_block(self):
        self.assertEqual(self.podcast.itunes_block, False)

    def test_item_itunes_duration(self):
        self.assertEqual(self.podcast.items[0].itunes_duration, "1:05")
        self.assertEqual(self.podcast.items[1].itunes_duration, "1:11:05")
        self.assertEqual(self.podcast.items[2].itunes_duration, "1:11:05")

    def test_item_itunes_closed_captioned(self):
        self.assertEqual(self.podcast.items[0].itunes_closed_captioned, "yes")
        self.assertEqual(self.podcast.items[1].itunes_closed_captioned, None)

    def test_item_itunes_explicit(self):
        self.assertEqual(self.podcast.items[0].itunes_explicit, "no")
        self.assertEqual(self.podcast.items[1].itunes_explicit, "clean")
        self.assertEqual(self.podcast.items[2].itunes_explicit, "clean")

    def test_item_itunes_image(self):
        self.assertEqual(self.podcast.items[0].itune_image, "http://poo.poo/gif.jpg")
        self.assertEqual(self.podcast.items[1].itune_image, "http://poo.poo/gif.jpg")
        self.assertEqual(self.podcast.items[2].itune_image, "http://poo.poo/gif.jpg")

    def test_item_itunes_keywords(self):
        self.assertEqual(self.podcast.items[0].itunes_keywords, ['One keyword', 'a second keyword', '3rd keyword'])
        self.assertEqual(self.podcast.items[1].itunes_keywords, None)

    def test_item_itunes_order(self):
        self.assertEqual(self.podcast.items[0].itunes_order, "2")
        self.assertEqual(self.podcast.items[1].itunes_order, "1")
        self.assertEqual(self.podcast.items[2].itunes_order, "1")

    def test_item_itunes_subtitle(self):
        self.assertEqual(self.podcast.items[0].itunes_subtitle, "The Subtitle")
        self.assertEqual(self.podcast.items[1].itunes_subtitle, "Another Subtitle")
        self.assertEqual(self.podcast.items[2].itunes_subtitle, "Subtitle with whitespace")
        self.assertEqual(self.podcast.items[3].itunes_subtitle, '<a href="https://foo.bar">Subtitle with html</a>')

    def test_item_itunes_subtitle_text(self):
        self.assertEqual(self.podcast.items[0].itunes_subtitle_text, "The Subtitle")
        self.assertEqual(self.podcast.items[1].itunes_subtitle_text, "Another Subtitle")
        self.assertEqual(self.podcast.items[2].itunes_subtitle_text, "Subtitle with whitespace")
        self.assertEqual(self.podcast.items[3].itunes_subtitle_text, "Subtitle with html")

    def test_item_itunes_summary(self):
        self.assertEqual(self.podcast.items[0].itunes_summary, "The Summary")
        self.assertEqual(self.podcast.items[1].itunes_summary, "Another Summary")
        self.assertEqual(self.podcast.items[2].itunes_summary, "Summary with whitespace")
        self.assertEqual(self.podcast.items[3].itunes_summary, "<div><div><table><tr><th>Summary with html</th><th>In a table</th></tr></table></div></div>")

    def test_item_itunes_summary_text(self):
        self.assertEqual(self.podcast.items[0].itunes_summary_text, "The Summary")
        self.assertEqual(self.podcast.items[1].itunes_summary_text, "Another Summary")
        self.assertEqual(self.podcast.items[2].itunes_summary_text, "Summary with whitespace")
        self.assertEqual(self.podcast.items[3].itunes_summary_text, "Summary with html In a table")

    def test_item_itunes_season(self):
        self.assertEqual(self.podcast.items[0].itunes_season, 0)

    def test_item_itunes_episode(self):
        self.assertEqual(self.podcast.items[0].itunes_episode, 42)

    def test_item_itunes_episode_type(self):
        self.assertEqual(self.podcast.items[0].itunes_episode_type, 'bonus')

    def test_item_enclosure_url(self):
        self.assertEqual(self.podcast.items[0].enclosure_url, 'https://github.com/jrigden/pyPodcastParser.mp3')

    def test_item_enclosure_type(self):
        self.assertEqual(self.podcast.items[0].enclosure_type, 'audio/mpeg')

    def test_item_enclosure_length(self):
        self.assertEqual(self.podcast.items[0].enclosure_length, 123456)

    def test_item_guid(self):
        self.assertEqual(self.podcast.items[0].guid, 'basic item guid')
        self.assertEqual(self.podcast.items[1].guid, 'another basic item guid')
        self.assertEqual(self.podcast.items[2].guid, 'another basic item guid')

    def test_item_link(self):
        self.assertEqual(self.podcast.items[0].link, "http://google.com/0")
        self.assertEqual(self.podcast.items[1].link, "http://google.com/1")
        self.assertEqual(self.podcast.items[2].link, "http://google.com/2")

    def test_item_published_date(self):
        self.assertTrue(isinstance(self.podcast.items[1].date_time, datetime.datetime))
        self.assertTrue(isinstance(self.podcast.items[2].date_time, datetime.datetime))

    def test_content_encoded(self):
        self.assertEqual(self.podcast.items[0].content_encoded, '<p>March 18, 2020</p>')
        self.assertEqual(self.podcast.items[1].content_encoded, None)

    def test_item_title(self):
        self.assertEqual(self.podcast.items[0].title, "basic item title")
        self.assertEqual(self.podcast.items[1].title, "another basic item title")
        self.assertEqual(self.podcast.items[2].title, "A title with lots of whitespace")
        self.assertEqual(self.podcast.items[3].title, "<h1>A title with html</h1>")

    def test_item_title_text(self):
        self.assertEqual(self.podcast.items[0].title_text, "basic item title")
        self.assertEqual(self.podcast.items[1].title_text, "another basic item title")
        self.assertEqual(self.podcast.items[2].title_text, "A title with lots of whitespace")
        self.assertEqual(self.podcast.items[3].title_text, "A title with html")

    def test_item_time_published(self):
        self.assertEqual(self.podcast.items[0].time_published, 1206107460)
        self.assertEqual(self.podcast.items[1].time_published, 1206107400)
        self.assertEqual(self.podcast.items[2].time_published, 1206107400)

class Test_Basic_Feed(unittest.TestCase):

    def setUp(self):
        test_dir = os.path.dirname(__file__)
        test_feeds_dir = os.path.join(test_dir, 'test_feeds')
        basic_podcast_path = os.path.join(test_feeds_dir, 'basic_podcast.rss')
        basic_podcast_file = open(basic_podcast_path, "r")
        self.basic_podcast = basic_podcast_file.read()
        self.podcast = Podcast.Podcast(self.basic_podcast)

    def test_loding_of_basic_podcast(self):
        self.assertIsNotNone(self.basic_podcast)

    def test_dict(self):
        feed_dict = self.podcast.to_dict()
        self.assertTrue(type(feed_dict) is dict)

    def test_title(self):
        self.assertEqual(self.podcast.title, 'basic title')

    def test_categories(self):
        self.assertTrue("Example category 2" in self.podcast.categories)

    def test_count_items(self):
        self.assertNotEqual(self.podcast.count_items(), "basic c")

    def test_copyright(self):
        self.assertEqual(self.podcast.copyright, "basic copyright")

    def test_description(self):
        self.assertEqual(self.podcast.description, "basic description")

    def test_generator(self):
        self.assertEqual(self.podcast.generator, "an infinite monkeys")

    def test_image(self):
        self.assertEqual(self.podcast.image_title, "Test Image")
        self.assertEqual(self.podcast.image_url, "https://test/giffy.jpg")
        self.assertEqual(self.podcast.image_link, "https://test")
        self.assertEqual(self.podcast.image_width, "1000")
        self.assertEqual(self.podcast.image_height, "5000")

    def test_itunes_author_name(self):
        self.assertEqual(self.podcast.itunes_author_name,
                         "basic itunes author")

    def test_itunes_block(self):
        self.assertEqual(self.podcast.itunes_block, False)

    def test_itunes_categories(self):
        self.assertTrue("News" in self.podcast.itunes_categories)
        self.assertTrue("Health" in self.podcast.itunes_categories)

    def test_itunes_explicit(self):
        self.assertEqual(self.podcast.itunes_explicit, "clean")

    def test_itunes_complete(self):
        self.assertEqual(self.podcast.itunes_complete, "yes")

    def test_itune_image(self):
        self.assertEqual(self.podcast.itune_image,
                         "https://github.com/jrigden/pyPodcastParser.jpg")

    def test_itunes_categories_length(self):
        number_of_categories = len(self.podcast.itunes_categories)
        self.assertEqual(number_of_categories, 2)

    def test_itunes_keyword_length(self):
        number_of_keywords = len(self.podcast.itunes_keywords)
        self.assertEqual(number_of_keywords, 2)

    def test_itunes_new_feed_url(self):
        self.assertEqual(self.podcast.itunes_new_feed_url, "http://newlocation.com/example.rss")

    def test_itunes_type(self):
        self.assertEqual(self.podcast.itunes_type, 'episodic')

    def test_language(self):
        self.assertEqual(self.podcast.language, "basic  language")

    def test_last_build_date(self):
        self.assertEqual(self.podcast.last_build_date,
                         "Mon, 24 Mar 2008 23:30:07 GMT")

    def test_link(self):
        self.assertEqual(self.podcast.link,
                         "https://github.com/jrigden/pyPodcastParser")

    def test_managing_editor(self):
        self.assertEqual(self.podcast.managing_editor, "nobody")

    def test_published_date(self):
        self.assertEqual(self.podcast.published_date,
                         "Mon, 24 Mar 2008 23:30:07 GMT")

    def test_pub_date(self):
        self.assertEqual(self.podcast.time_published, 1206401407)

    def test_pubsubhubbub(self):
        self.assertEqual(self.podcast.pubsubhubbub, "https://pubsubhubbub.appspot.com")

    def test_owner_name(self):
        self.assertEqual(self.podcast.owner_name, "basic itunes owner name")

    def test_owner_email(self):
        self.assertEqual(self.podcast.owner_email, "basic itunes owner email")

    def test_subtitle(self):
        self.assertEqual(self.podcast.subtitle, "basic itunes subtitle")

    def test_summary(self):
        self.assertEqual(self.podcast.summary, "basic itunes summary")

    def test_summary(self):
        self.assertEqual(self.podcast.summary, "basic itunes summary")

    def test_title(self):
        self.assertEqual(self.podcast.title, "basic title")

    def test_ttl(self):
        self.assertEqual(self.podcast.ttl, "60")

    def test_web_master(self):
        self.assertEqual(self.podcast.web_master, "webrobot")

    def test_time_published(self):
        self.assertTrue(isinstance(self.podcast.date_time, datetime.datetime))

class Test_Unicode_Feed(unittest.TestCase):

    def setUp(self):
        self.unicodeish_text = u"ℐℑℒℓ℔✕✖✗✘⨒⨓ㄏㄐ㐆㐇㐈㐉蘿螺ﻛﻜﻝﻞ𝀏𝀐𝀑𝀒𝀓ǫǬǭǮǯǰΑΒΓΔΕΖΗΘɥɦɧखगڙښڛ"
        test_dir = os.path.dirname(__file__)
        test_feeds_dir = os.path.join(test_dir, 'test_feeds')
        basic_podcast_path = os.path.join(test_feeds_dir, 'unicode_podcast.rss')
        basic_podcast_file = open(basic_podcast_path, "r")
        self.basic_podcast = basic_podcast_file.read()
        self.podcast = Podcast.Podcast(self.basic_podcast)

    def test_loding_of_basic_podcast(self):
        self.assertIsNotNone(self.basic_podcast)

    def test_copyright(self):
        self.assertEqual(self.podcast.copyright, self.unicodeish_text)

    def test_description(self):
        self.assertEqual(self.podcast.description, self.unicodeish_text)

    def test_generator(self):
        self.assertEqual(self.podcast.generator, self.unicodeish_text)

    def test_itunes_author_name(self):
        self.assertEqual(self.podcast.itunes_author_name, self.unicodeish_text)

    def test_itunes_block(self):
        self.assertEqual(self.podcast.itunes_block, False)

    def test_itunes_categories(self):
        self.assertTrue(self.unicodeish_text in self.podcast.itunes_categories)
        self.assertTrue(self.unicodeish_text in self.podcast.itunes_categories)


    def test_itune_image(self):
        self.assertEqual(self.podcast.itune_image, self.unicodeish_text)

    def test_itunes_categories_length(self):
        number_of_categories = len(self.podcast.itunes_categories)
        self.assertEqual(number_of_categories, 2)

    def test_itunes_keyword_length(self):
        number_of_keywords = len(self.podcast.itunes_keywords)
        self.assertEqual(number_of_keywords, 1)

    def test_itunes_new_feed_url(self):
        self.assertEqual(self.podcast.itunes_new_feed_url, self.unicodeish_text)

    def test_language(self):
        self.assertEqual(self.podcast.language, self.unicodeish_text)

    def test_last_build_date(self):
        self.assertEqual(self.podcast.last_build_date, self.unicodeish_text)

    def test_link(self):
        self.assertEqual(self.podcast.link, self.unicodeish_text)

    def test_managing_editor(self):
        self.assertEqual(self.podcast.managing_editor, self.unicodeish_text)


    def test_owner_name(self):
        self.assertEqual(self.podcast.owner_name, self.unicodeish_text)

    def test_owner_email(self):
        self.assertEqual(self.podcast.owner_email, self.unicodeish_text)

    def test_subtitle(self):
        self.assertEqual(self.podcast.subtitle, self.unicodeish_text)

    def test_summary(self):
        self.assertEqual(self.podcast.summary, self.unicodeish_text)

    def test_summary(self):
        self.assertEqual(self.podcast.summary, self.unicodeish_text)

    def test_title(self):
        self.assertEqual(self.podcast.title, self.unicodeish_text)

    def test_web_master(self):
        self.assertEqual(self.podcast.web_master, self.unicodeish_text)


class Test_Missing_Info_Feed_Items(unittest.TestCase):

    def setUp(self):
        test_dir = os.path.dirname(__file__)
        test_feeds_dir = os.path.join(test_dir, 'test_feeds')
        basic_podcast_path = os.path.join(test_feeds_dir, 'missing_info_podcast.rss')
        basic_podcast_file = open(basic_podcast_path, "r")
        self.basic_podcast = basic_podcast_file.read()
        self.podcast = Podcast.Podcast(self.basic_podcast)


    def test_item_itunes_season(self):
        self.assertEqual(self.podcast.items[0].itunes_season, None)

    def test_item_itunes_episode(self):
        self.assertEqual(self.podcast.items[0].itunes_episode, None)
        self.assertEqual(self.podcast.items[1].itunes_episode, None)

    def test_item_itunes_episode_type(self):
        self.assertEqual(self.podcast.items[0].itunes_episode_type, None)
        self.assertEqual(self.podcast.items[1].itunes_episode_type, None)

    def test_item_time_published(self):
        self.assertEqual(self.podcast.items[0].time_published, None)
        self.assertEqual(self.podcast.items[1].time_published, None)

class Test_Missing_Info_Feed(unittest.TestCase):

    def setUp(self):
        test_dir = os.path.dirname(__file__)
        test_feeds_dir = os.path.join(test_dir, 'test_feeds')
        basic_podcast_path = os.path.join(test_feeds_dir, 'missing_info_podcast.rss')
        basic_podcast_file = open(basic_podcast_path, "r")
        self.basic_podcast = basic_podcast_file.read()
        self.podcast = Podcast.Podcast(self.basic_podcast)

    def test_loding_of_basic_podcast(self):
        self.assertIsNotNone(self.basic_podcast)

    def test_categories(self):
        self.assertFalse("Example category 2" in self.podcast.categories)

    def test_count_items(self):
        self.assertNotEqual(self.podcast.count_items(), "basic c")

    def test_copyright(self):
        self.assertEqual(self.podcast.copyright, None)

    def test_creative_commons(self):
        self.assertEqual(self.podcast.creative_commons, None)

    def test_description(self):
        self.assertEqual(self.podcast.description, None)

    def test_generator(self):
        self.assertEqual(self.podcast.generator, None)

    def test_image(self):
        self.assertEqual(self.podcast.image_title, None)
        self.assertEqual(self.podcast.image_url, None)
        self.assertEqual(self.podcast.image_link, None)
        self.assertEqual(self.podcast.image_width, None)
        self.assertEqual(self.podcast.image_height, None)

    def test_itunes_author_name(self):
        self.assertEqual(self.podcast.itunes_author_name, None)

    def test_itunes_block(self):
        self.assertEqual(self.podcast.itunes_block, False)

    def test_itunes_categories(self):
        self.assertFalse("News" in self.podcast.itunes_categories)
        self.assertFalse("Health" in self.podcast.itunes_categories)

    def test_itunes_explicit(self):
        self.assertEqual(self.podcast.itunes_explicit, None)

    def test_itunes_complete(self):
        self.assertEqual(self.podcast.itunes_complete, None)

    def test_itune_image(self):
        self.assertEqual(self.podcast.itune_image, None)

    def test_itunes_categories_length(self):
        number_of_categories = len(self.podcast.itunes_categories)
        self.assertEqual(number_of_categories, 0)

    def test_itunes_keyword_length(self):
        number_of_keywords = len(self.podcast.itunes_keywords)
        self.assertEqual(number_of_keywords, 0)

    def test_itunes_new_feed_url(self):
        self.assertEqual(self.podcast.itunes_new_feed_url, None)

    def test_itunes_type(self):
        self.assertEqual(self.podcast.itunes_type, None)

    def test_language(self):
        self.assertEqual(self.podcast.language, None)

    def test_last_build_date(self):
        self.assertEqual(self.podcast.last_build_date, None)

    def test_link(self):
        self.assertEqual(self.podcast.link, None)

    def test_managing_editor(self):
        self.assertEqual(self.podcast.managing_editor, None)

    def test_published_date(self):
        self.assertEqual(self.podcast.published_date, None)

    def test_owner_name(self):
        self.assertEqual(self.podcast.owner_name, None)

    def test_owner_email(self):
        self.assertEqual(self.podcast.owner_email, None)

    def test_pubsubhubbub(self):
        self.assertEqual(self.podcast.pubsubhubbub, None)

    def test_subtitle(self):
        self.assertEqual(self.podcast.subtitle, None)

    def test_summary(self):
        self.assertEqual(self.podcast.summary, None)

    def test_summary(self):
        self.assertEqual(self.podcast.summary, None)

    def test_title(self):
        self.assertEqual(self.podcast.title, None)

    def test_ttl(self):
        self.assertEqual(self.podcast.ttl, None)

    def test_web_master(self):
        self.assertEqual(self.podcast.web_master, None)

    def test_time_published(self):
        self.assertIsNone(self.podcast.date_time)

class Test_Itunes_Block_Feed(unittest.TestCase):

    def setUp(self):
        test_dir = os.path.dirname(__file__)
        test_feeds_dir = os.path.join(test_dir, 'test_feeds')
        basic_podcast_path = os.path.join(
            test_feeds_dir, 'itunes_block_podcast.rss')
        basic_podcast_file = open(basic_podcast_path, "r")
        self.basic_podcast = basic_podcast_file.read()
        self.podcast = Podcast.Podcast(self.basic_podcast)

    def test_itunes_block(self):
        self.assertEqual(self.podcast.itunes_block, True)

    def test_itunes_explicit(self):
        self.assertEqual(self.podcast.itunes_explicit, "yes")

class Test_Basic_Feed_Items_Generator(unittest.TestCase):
    def setUp(self):
        test_dir = os.path.dirname(__file__)
        test_feeds_dir = os.path.join(test_dir, 'test_feeds')
        basic_podcast_path = os.path.join(test_feeds_dir, 'basic_podcast.rss')
        basic_podcast_file = open(basic_podcast_path, "r")
        self.basic_podcast = basic_podcast_file.read()
        self.podcast = Podcast.Podcast(self.basic_podcast, False)

    def test_item_comments(self):
        comments = [
          "http://comments.com/entry/0",
          "http://comments.com/entry/1",
          "http://comments.com/entry/2",
          "http://comments.com/entry/3"
        ]
        for index, item in enumerate(self.podcast.get_items(), start=0):
            self.assertEqual(item.comments, comments[index])
        self.assertEqual(index, len(comments)-1)

class Test_Invalid_Feed_Items(unittest.TestCase):
    def setUp(self):
        test_dir = os.path.dirname(__file__)
        test_feeds_dir = os.path.join(test_dir, 'test_feeds')
        basic_podcast_path = os.path.join(test_feeds_dir, 'invalid_podcast.rss')
        basic_podcast_file = open(basic_podcast_path, "r")
        self.basic_podcast = basic_podcast_file.read()
        self.podcast = Podcast.Podcast(self.basic_podcast)

    def test_item_itunes_season(self):
        self.assertEqual(self.podcast.items[0].itunes_season, None)

    def test_item_itunes_episode(self):
        self.assertEqual(self.podcast.items[0].itunes_episode, None)

    def test_item_itunes_episode_type(self):
        self.assertEqual(self.podcast.items[0].itunes_episode_type, None)

class Test_Invalid_Feed(unittest.TestCase):
    def setUp(self):
        test_dir = os.path.dirname(__file__)
        test_feeds_dir = os.path.join(test_dir, 'test_feeds')
        basic_podcast_path = os.path.join(test_feeds_dir, 'invalid_podcast.rss')
        basic_podcast_file = open(basic_podcast_path, "r")
        self.basic_podcast = basic_podcast_file.read()
        self.podcast = Podcast.Podcast(self.basic_podcast, False)

    def test_pub_date(self):
        self.assertEqual(self.podcast.time_published, None)

    def test_time_published(self):
        self.assertEqual(self.podcast.published_date, 'Mon, 24 Mar 2008')

if __name__ == '__main__':
    unittest.main()
