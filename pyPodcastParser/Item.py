from bs4 import BeautifulSoup
from datetime import datetime
import email.utils
from time import mktime

class Item(object):
    """Parses an xml rss feed

    RSS Specs http://cyber.law.harvard.edu/rss/rss.html
    iTunes Podcast Specs http://www.apple.com/itunes/podcasts/specs.html

    Args:
        soup (bs4.BeautifulSoup): BeautifulSoup object representing a rss item

    Note:
        All attributes with empty or nonexistent element will have a value of None

    Attributes:
        author (str): The author of the item
        comments (str): URL of comments
        creative_commons (str): creative commons license for this item
        description (str): Description of the item.
        description_text (str): Description of the item without html tags.
        enclosure_url (str): URL of enclosure
        enclosure_type (str): File MIME type
        enclosure_length (int): File size in bytes
        guid (str): globally unique identifier
        itunes_title (str): Title name given to iTunes
        itunes_title_text (str): Title name given to iTunes without html tags
        itunes_author_name (str): Author name given to iTunes
        itunes_season (int): Season number given to iTunes
        itunes_episode (int): Episode number given to iTunes
        itunes_episode_type (str): Episode type given to iTunes
        itunes_block (bool): It this Item blocked from itunes
        itunes_closed_captioned: (str): It is this item have closed captions
        itunes_duration (str): Duration of enclosure
        itunes_explicit (str): Is this item explicit. Should only be yes or clean.
        itune_image (str): URL of item cover art
        itunes_order (str): Override published_date order
        itunes_subtitle (str): The item subtitle
        itunes_subtitle_text (str): The item subtitle without html tags
        itunes_summary (str): The summary of the item
        itunes_summary_text (str): The summary of the item without html tags
        itunes_keywords (list): List of strings for keywords
        link (str): The URL of item.
        published_date (str): Date item was published
        title (str): The title of item.
        title_text (str): The title of item without html tags.
        date_time (datetime): When published
    """

    def __init__(self, soup):
        #super(Item, self).__init__()

        self.soup = soup
        self.set_rss_element()
        self.set_itunes_element()

        self.set_time_published()
        self.set_dates_published()

    def set_time_published(self):
        if self.published_date is None:
            self.time_published = None
            return
        time_tuple = email.utils.parsedate_tz(self.published_date)
        try:
            self.time_published = email.utils.mktime_tz(time_tuple)
        except TypeError:
            self.time_published = None

    def set_dates_published(self):
        if self.published_date is None:
            self.date_time = None
            return
        time_tuple = email.utils.parsedate(self.published_date)
        try:
            temp_datetime = datetime(time_tuple[0], time_tuple[1], time_tuple[2])
        except TypeError:
            self.date_time = None
            return
        self.date_time = temp_datetime

    def to_dict(self):
        item = {}
        item['author'] = self.author
        item['comments'] = self.comments
        item['creative_commons'] = self.creative_commons
        item['enclosure_url'] = self.enclosure_url
        item['enclosure_type'] = self.enclosure_type
        item['enclosure_length'] = self.enclosure_length
        item['enclosure_type'] = self.enclosure_type
        item['guid'] = self.guid
        item['itunes_title'] = self.itunes_title
        item['itunes_title_text'] = self.itunes_title_text
        item['itunes_author_name'] = self.itunes_author_name
        item['itunes_block'] = self.itunes_block
        item['itunes_closed_captioned'] = self.itunes_closed_captioned
        item['itunes_duration'] = self.itunes_duration
        item['itunes_explicit'] = self.itunes_explicit
        item['itunes_episode'] = self.itunes_episode
        item['itunes_season'] = self.itunes_season
        item['itunes_episode_type'] = self.itunes_episode_type
        item['itune_image'] = self.itune_image
        item['itunes_order'] = self.itunes_order
        item['itunes_subtitle'] = self.itunes_subtitle
        item['itunes_subtitle_text'] = self.itunes_subtitle_text
        item['itunes_summary'] = self.itunes_summary
        item['itunes_summary_text'] = self.itunes_summary_text
        item['itunes_keywords'] = self.itunes_keywords
        item['content_encoded'] = self.content_encoded
        item['description'] = self.description
        item['description_text'] = self.description_text
        item['link'] = self.link
        item['published_date'] = self.published_date
        item['title'] = self.title
        item['title_text'] = self.title_text
        return item

    def set_rss_element(self):
        """Set each of the basic rss elements."""
        self.set_author()
        self.set_categories()
        self.set_comments()
        self.set_creative_commons()
        self.set_description()
        self.set_content_encoded()
        self.set_enclosure()
        self.set_guid()
        self.set_link()
        self.set_published_date()
        self.set_title()

    def set_author(self):
        """Parses author and set value."""
        try:
            self.author = self.soup.find('author').string.strip()
        except AttributeError:
            self.author = None

    def set_categories(self):
        """Parses and set categories"""
        self.categories = []
        temp_categories = self.soup.findAll('category')
        for category in temp_categories:
            category_text = category.string.strip()
            self.categories.append(category_text)

    def set_comments(self):
        """Parses comments and set value."""
        try:
            self.comments = self.soup.find('comments').string.strip()
        except AttributeError:
            self.comments = None

    def set_creative_commons(self):
        """Parses creative commons for item and sets value"""
        try:
            self.creative_commons = self.soup.find('license').string.strip()
        except AttributeError:
            self.creative_commons = None

    def set_description(self):
        """Parses description and set value."""
        try:
            description = self.soup.find('description')
            self.description = description.string.strip()
        except AttributeError:
            self.description = None
        try:
            description_soup = BeautifulSoup(self.description, "html.parser")
            self.description_text = description_soup.get_text(" ", strip=True)
        except:
            self.description_text = None

    def set_content_encoded(self):
        """Parses content_encoded and set value."""
        try:
            self.content_encoded = self.soup.find('encoded').string.strip()
        except AttributeError:
            self.content_encoded = None

    def set_enclosure(self):
        """Parses enclosure_url, enclosure_type then set values."""
        try:
            self.enclosure_url = self.soup.find('enclosure')['url']
        except:
            self.enclosure_url = None
        try:
            self.enclosure_type = self.soup.find('enclosure')['type']
        except:
            self.enclosure_type = None
        try:
            self.enclosure_length = self.soup.find('enclosure')['length']
            self.enclosure_length = int(self.enclosure_length)
        except:
            self.enclosure_length = None

    def set_guid(self):
        """Parses guid and set value"""
        try:
            self.guid = self.soup.find('guid').string.strip()
        except AttributeError:
            self.guid = None

    def set_link(self):
        """Parses link and set value."""
        try:
            self.link = self.soup.find('link').string.strip()
        except AttributeError:
            self.link = None

    def set_published_date(self):
        """Parses published date and set value."""
        try:
            self.published_date = self.soup.find('pubDate').string.strip()
        except AttributeError:
            self.published_date = None

    def set_title(self):
        """Parses title and set value."""
        try:
            title = self.soup.find('title')
            self.title = title.string.strip()
        except AttributeError:
            self.title = None
        try:
            title_soup = BeautifulSoup(self.title, "html.parser")
            self.title_text = title_soup.get_text(" ", strip=True)
        except:
            self.title_text = None

    def set_itunes_element(self):
        """Set each of the itunes elements."""
        self.set_itunes_title()
        self.set_itunes_author_name()
        self.set_itunes_episode()
        self.set_itunes_season()
        self.set_itunes_episode_type()
        self.set_itunes_block()
        self.set_itunes_closed_captioned()
        self.set_itunes_duration()
        self.set_itunes_explicit()
        self.set_itune_image()
        self.set_itunes_order()
        self.set_itunes_subtitle()
        self.set_itunes_summary()
        self.set_itunes_keywords()

    def set_itunes_title(self):
        """Parses title from itunes tags and sets value"""
        try:
            title = self.soup.find('itunes:title')
            self.itunes_title = title.string.strip()
        except AttributeError:
            self.itunes_title = None
        try:
            title_soup = BeautifulSoup(self.itunes_title, "html.parser")
            self.itunes_title_text = title_soup.get_text(" ", strip=True)
        except:
            self.itunes_title_text = None

    def set_itunes_author_name(self):
        """Parses author name from itunes tags and sets value"""
        try:
            self.itunes_author_name = self.soup.find('itunes:author').string.strip()
        except AttributeError:
            self.itunes_author_name = None

    def set_itunes_episode(self):
        """Parses the episode number and sets value"""
        try:
            self.itunes_episode = int(self.soup.find('itunes:episode').string)
        except:
            self.itunes_episode = None

    def set_itunes_season(self):
        """Parses the episode season and sets value"""
        try:
            self.itunes_season = int(self.soup.find('itunes:season').string)
        except:
            self.itunes_season = None

    def set_itunes_episode_type(self):
        """Parses the episode type and sets value"""
        try:
            self.itunes_episode_type = self.soup.find('itunes:episodeType').string.strip()
        except AttributeError:
            self.itunes_episode_type = None

    def set_itunes_block(self):
        """Check and see if item is blocked from iTunes and sets value"""
        try:
            block = self.soup.find('itunes:block').string.lower()
        except AttributeError:
            block = ""
        if block == "yes":
            self.itunes_block = True
        else:
            self.itunes_block = False

    def set_itunes_closed_captioned(self):
        """Parses isClosedCaptioned from itunes tags and sets value"""
        try:
            self.itunes_closed_captioned = self.soup.find(
                'itunes:isClosedCaptioned').string.strip()
            self.itunes_closed_captioned = self.itunes_closed_captioned.lower()
        except AttributeError:
            self.itunes_closed_captioned = None

    def set_itunes_duration(self):
        """Parses duration from itunes tags and sets value"""
        try:
            self.itunes_duration = self.soup.find('itunes:duration').string.strip()
        except AttributeError:
            self.itunes_duration = None

    def set_itunes_explicit(self):
        """Parses explicit from itunes item tags and sets value"""
        try:
            self.itunes_explicit = self.soup.find('itunes:explicit').string.strip()
            self.itunes_explicit = self.itunes_explicit.lower()
        except AttributeError:
            self.itunes_explicit = None

    def set_itune_image(self):
        """Parses itunes item images and set url as value"""
        try:
            self.itune_image = self.soup.find('itunes:image').get('href')
        except AttributeError:
            self.itune_image = None

    def set_itunes_order(self):
        """Parses episode order and set url as value"""
        try:
            self.itunes_order = self.soup.find('itunes:order').string.strip()
            self.itunes_order = self.itunes_order.lower()
        except AttributeError:
            self.itunes_order = None

    def set_itunes_subtitle(self):
        """Parses subtitle from itunes tags and sets value"""
        try:
            subtitle = self.soup.find('itunes:subtitle')
            self.itunes_subtitle = subtitle.string.strip()
        except AttributeError:
            self.itunes_subtitle = None
        try:
            subtitle_soup = BeautifulSoup(self.itunes_subtitle, "html.parser")
            self.itunes_subtitle_text = subtitle_soup.get_text(" ", strip=True)
        except:
            self.itunes_subtitle_text = None

    def set_itunes_summary(self):
        """Parses summary from itunes tags and sets value"""
        try:
            summary = self.soup.find('itunes:summary')
            self.itunes_summary = summary.string.strip()
        except AttributeError:
            self.itunes_summary = None
        try:
            summary_soup = BeautifulSoup(self.itunes_summary, "html.parser")
            self.itunes_summary_text = summary_soup.get_text(" ", strip=True)
        except:
            self.itunes_summary_text = None

    def set_itunes_keywords(self):
        """ Parse keywrods from itunes tags and set value"""
        try:
            words = self.soup.find('itunes:keywords').string
            self.itunes_keywords = [keyword.strip() for keyword in words.split(",")]
        except AttributeError:
            self.itunes_keywords = None


