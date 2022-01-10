# %%

from __future__ import annotations


import dataclasses
import datetime
import re
import typing

T = typing.TypeVar("T")


class LibraryFactory(typing.Protocol):
    @classmethod
    def parse_sub_stream(cls, T) -> SubStream:
        raise NotImplementedError
    @classmethod
    def parse_video_stream(cls, T) -> VideoStream:
        raise NotImplementedError
    @classmethod
    def parse_audio_stream(cls, T) -> AudioStream:
        raise NotImplementedError

    @classmethod
    def parse_stream_details(cls, T) -> StreamDetails:
        raise NotImplementedError

    @classmethod
    def parse_movie(cls, T) -> Movie:
        raise NotImplementedError

    @classmethod
    def parse_episode(cls, T) -> Episode:
        raise NotImplementedError

    @classmethod
    def parse_series(cls, T) -> Series:
        raise NotImplementedError

    @classmethod
    def parse_video_database(cls, T) -> VideoDatabase:
        raise NotImplementedError


@dataclasses.dataclass
class StreamDetails:
    videos: typing.Tuple[VideoStream, ...] = ()
    audios: typing.Tuple[AudioStream, ...] = ()
    subs: typing.Tuple[SubStream, ...] = ()


@dataclasses.dataclass
class VideoStream:
    codec: typing.Optional[str] = None
    width: typing.Optional[int] = None
    height: typing.Optional[int] = None


@dataclasses.dataclass
class AudioStream:
    codec: typing.Optional[str] = None
    language: typing.Optional[str] = None
    channels: typing.Optional[int] = None


@dataclasses.dataclass
class SubStream:
    language: typing.Optional[str] = None


@dataclasses.dataclass
class Movie:
    title: typing.Optional[str] = None
    year: typing.Optional[int] = None
    duration: typing.Optional[datetime.timedelta] = None
    streams: StreamDetails = dataclasses.field(default_factory=lambda: StreamDetails())

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


@dataclasses.dataclass
class VideoDatabase:
    movies: typing.List[Movie]
    series: typing.List[Series]
