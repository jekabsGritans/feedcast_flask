from feedgen.feed import FeedGenerator

class PodcastFeed:
    fg = FeedGenerator()
    fg.load_extension('podcast')

    def __init__(self, podcast):
        self.podcast = podcast
        self.fg.title(podcast.title)
        self.fg.link(podcast.link)
        self.fg.description(podcast.description)
        self.fg.language(podcast.language)
        self.fg.author({'name': podcast.author_name, 'email': podcast.author_name})
        self.fg.image(podcast.image)
        self.fg.itunes_explicit('yes' if podcast.explicit else 'no')
        cats = podcast.categories.split()
        self.fg.itunes_category([
            {'cat':cats[0], 'sub':subc} for subc in cats[1:]])
        self.fg.itunes_type('episodic' if podcast.series_episodic else 'serial')
        self.fg.media_restriction(podcast.allowed_regions)
        self.fg.spotify_country_of_origin(podcast.origin)

        if podcast.spotify_limit:
            self.fg.spotify_limit(podcast.spotify_limit)

        for episode in podcast.episodes:
            fe = self.fg.add_entry()
            fe.title(episode.title)
            fe.guid(episode.id)
            fe.enclosure(url=podcast.audio,type=podcast.audio_type,length=podcast.audio_bytes)
            fe.description(podcast.description)
            fe.pubDate(episode.pubdate)
            fe.media_restriction(episode.allowed_regions)
            fe.itunes_duration(episode.duration)
            fe.itunes_order(episode.itunes_oreder)
            fe.itunes_explicit(episode.explicit)
            fe.itunes_image(episode.image)
            fe.itunes_keywords(episode.keywords)
            fe.itunes_episode_type(episode.episode_type)


    def to_str(self):
        return self.fg.rss_str(pretty=True)