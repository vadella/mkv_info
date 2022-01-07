# %%

from __future__ import annotations


import dataclasses
import datetime
import re
import typing
import xml.etree.ElementTree as ET


@dataclasses.dataclass
class StreamDetails:
    videos: typing.Tuple[VideoStream, ...] = ()
    audios: typing.Tuple[AudioStream, ...] = ()
    subs: typing.Tuple[SubStream, ...] = ()

    @classmethod
    def from_data(cls, data: typing.Optional[ET.Element]) -> StreamDetails:

        if data is None:
            return cls()
        streaminfo = data.find("streamdetails")
        if streaminfo is None:
            return cls()
        videos = tuple(
            VideoStream.from_data(stream) for stream in streaminfo.findall("video")
        )
        audios = tuple(
            AudioStream.from_data(stream) for stream in streaminfo.findall("audio")
        )
        subs = tuple(
            SubStream.from_data(stream) for stream in streaminfo.findall("subtitle")
        )
        return cls(videos=videos, audios=audios, subs=subs)


@dataclasses.dataclass
class VideoStream:
    codec: typing.Optional[str] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None

    @classmethod
    def from_data(cls, stream: ET.Element) -> VideoStream:
        codec = get_text(stream, "codec")
        height = get_int(stream, "height")
        width = get_int(stream, "width")

        return cls(codec=codec, width=width, height=height,)


@dataclasses.dataclass
class AudioStream:
    codec: typing.Optional[str] = None
    language: typing.Optional[str] = None
    channels: typing.Optional[int] = None

    @classmethod
    def from_data(cls, stream: ET.Element) -> AudioStream:
        codec: typing.Optional[str] = get_text(stream, "codec")
        language: typing.Optional[str] = get_text(stream, "language")
        channels: typing.Optional[int] = get_int(stream, "channels")
        return cls(codec=codec, language=language, channels=channels,)


@dataclasses.dataclass
class SubStream:
    language: typing.Optional[str] = None

    @classmethod
    def from_data(cls, stream: ET.Element) -> SubStream:
        language: typing.Optional[str] = get_text(stream, "language")
        return cls(language=language)


def get_text(element: ET.Element, tag: str) -> typing.Optional[str]:
    data = element.find(tag)
    if data is None:
        return None
    return data.text


def get_int(element: ET.Element, tag: str) -> typing.Optional[int]:
    data = element.find(tag)
    if data is None or data.text is None or not data.text.isalnum():
        return None
    return int(data.text)


def get_duration(element: ET.Element, tag: str) -> typing.Optional[datetime.timedelta]:
    data = element.find(tag)
    if data is None or data.text is None:
        return None
    if data.text.isalnum():
        return datetime.timedelta(minutes=int(data.text))
    pat = re.compile(r"(?P<minutes>\d+) min")
    if (match := pat.match(data.text)) is None:
        print(repr(data.text))
        return None
    return datetime.timedelta(minutes=int(match.group("minutes")))


@dataclasses.dataclass
class Movie:
    title: typing.Optional[str] = None
    year: typing.Optional[int] = None
    duration: typing.Optional[datetime.timedelta] = None
    streams: StreamDetails = dataclasses.field(default_factory=lambda: StreamDetails())

    @classmethod
    def from_data(cls, data: ET.Element) -> Movie:
        title = get_text(data, "title")
        year = get_int(data, "year")
        duration = get_duration(data, "runtime")
        streams = StreamDetails.from_data(data.find("fileinfo"))
        return cls(title=title, year=year, duration=duration, streams=streams)

    @property
    def video_streams(self) -> typing.Iterator[VideoStream]:
        yield from self.streams.videos

    @property
    def audio_streams(self) -> typing.Iterator[AudioStream]:
        yield from self.streams.audios

    @property
    def sub_streams(self) -> typing.Iterator[SubStream]:
        yield from self.streams.subs

    @property
    def streams_iterator(
        self,
    ) -> typing.Iterator[typing.Union[VideoStream, AudioStream, SubStream]]:
        yield from self.video_streams
        yield from self.audio_streams
        yield from self.sub_streams

    def __str__(self):
        repr = f"""Movie(title=<{self.title}>, year=<{self.year}>, duration=<{self.duration}>)"""
        stream_str = "\n\t".join(str(s) for s in self.streams_iterator)
        return repr + "\n\t" + stream_str


@dataclasses.dataclass
class Episode:
    title: typing.Optional[str] = None
    year: typing.Optional[int] = None
    duration: typing.Optional[datetime.timedelta] = None
    season: typing.Optional[int] = None
    episode: typing.Optional[int] = None
    streams: StreamDetails = dataclasses.field(default_factory=lambda: StreamDetails())

    @classmethod
    def from_data(cls, data: ET.Element) -> Episode:
        title = get_text(data, "title")
        year = get_int(data, "year")
        duration = get_duration(data, "runtime")
        season = get_int(data, "season")
        episode = get_int(data, "episode")
        streams = StreamDetails.from_data(data.find("fileinfo"))
        return cls(
            title=title,
            year=year,
            duration=duration,
            season=season,
            episode=episode,
            streams=streams,
        )

    @property
    def video_streams(self) -> typing.Iterator[VideoStream]:
        yield from self.streams.videos

    @property
    def audio_streams(self) -> typing.Iterator[AudioStream]:
        yield from self.streams.audios

    @property
    def sub_streams(self) -> typing.Iterator[SubStream]:
        yield from self.streams.subs

    @property
    def streams_iterator(
        self,
    ) -> typing.Iterator[typing.Union[VideoStream, AudioStream, SubStream]]:
        yield from self.video_streams
        yield from self.audio_streams
        yield from self.sub_streams


@dataclasses.dataclass
class Series:

    title: typing.Optional[str] = None
    year: typing.Optional[int] = None
    season: typing.Optional[int] = None
    episode: typing.Optional[int] = None
    episodes: typing.List[Episode] = dataclasses.field(default_factory=list)

    @classmethod
    def from_data(cls, data: ET.Element) -> Series:
        title = get_text(data, "title")
        year = get_int(data, "year")
        season = get_int(data, "season")
        episode = get_int(data, "episode")
        episodes = [Episode.from_data(tag) for tag in data.iter("episodedetails")]
        return cls(
            title=title, year=year, season=season, episode=episode, episodes=episodes,
        )


@dataclasses.dataclass
class VideoDatabase:
    movies: typing.List[Movie]
    series: typing.List[Series]

    @classmethod
    def from_data(cls, data: ET.Element) -> VideoDatabase:
        return cls(
            movies=[Movie.from_data(tag) for tag in data.iter("movie")],
            series=[Series.from_data(tag) for tag in data.iter("tvshow")],
        )
