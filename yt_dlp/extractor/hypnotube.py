
from .common import InfoExtractor


class HypnotubeIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?hypnotube\.com/video/(.+)\.html'
    _TEST = {
        'url': 'https://hypnotube.com/video/feminine-energy-vr-sbs-82117.html',
        # 'md5': 'TODO: md5 sum of the first 10241 bytes of the video file (use --test)',
        'info_dict': {
            'id': 'feminine-energy-vr-sbs-82117',
            'ext': 'mp4',
            'title': 'Feminine Energy - VR SBS',
            'thumbnail': r're:^https?://.*\.jpg$',
            # * A value
            # * MD5 checksum; start the string with md5:
            # * A regular expression; start the string with re:
            # * Any Python type (for example int or float)
        },
    }

    def _real_extract(self, url):
        video_id = self._generic_id(url)
        webpage = self._download_webpage(url, video_id)

        self.write_debug(video_id)

        sources_str = self._html_search_regex(r'sources:\s*(\[\{.+?\}\]),', webpage, 'sources')
        sources = self._parse_json(sources_str, video_id)
        title = self._html_search_regex(r'title:\s*\'(.+?)\',', webpage, 'title')
        thumbnail = self._html_search_regex(r'poster:\s*\'(.+?)\',', webpage, 'thumbnail')

        return {
            'id': video_id,
            'title': title,
            'thumbnail': thumbnail,

            'formats': [{
                'url': source['src'],
                'format': source['type'],
                'height': source['size'],
            } for source in sources],
        }
