# %%

from __future__ import annotations


import dataclasses
import datetime
import re
import typing
import xml.etree.ElementTree as ET
from . import media_library

data: typing.TypeAlias = typing.Optional[ET.Element]


class XML_Parser(media_library.LibraryFactory):
    @classmethod
    def parse_stream_details(cls, data) -> media_library.StreamDetails:

        if data is None:
            return media_library.StreamDetails()
        streaminfo = data.find("streamdetails")
        if streaminfo is None:
            return media_library.StreamDetails()
        videos = tuple(
            cls.parse_video_stream(stream) for stream in streaminfo.findall("video")
        )
        audios = tuple(
            cls.parse_audio_stream(stream) for stream in streaminfo.findall("audio")
        )
        subs = tuple(
            cls.parse_sub_stream(stream) for stream in streaminfo.findall("subtitle")
        )
        return media_library.StreamDetails(videos=videos, audios=audios, subs=subs)

    @classmethod
    def parse_video_stream(cls, stream: ET.Element) -> media_library.VideoStream:
        codec = get_text(stream, "codec")
        height = get_int(stream, "height")
        width = get_int(stream, "width")

        return media_library.VideoStream(codec=codec, width=width, height=height,)

    @classmethod
    def parse_audio_stream(cls, stream: ET.Element) -> media_library.AudioStream:
        codec: typing.Optional[str] = get_text(stream, "codec")
        language: typing.Optional[str] = get_text(stream, "language")
        channels: typing.Optional[int] = get_int(stream, "channels")
        return media_library.AudioStream(
            codec=codec, language=language, channels=channels,
        )

    @classmethod
    def parse_sub_stream(cls, stream: ET.Element) -> media_library.SubStream:
        language: typing.Optional[str] = get_text(stream, "language")
        return media_library.SubStream(language=language)

    @classmethod
    def parse_movie(cls, data: ET.Element) -> media_library.Movie:
        title = get_text(data, "title")
        year = get_int(data, "year")
        duration = get_duration(data, "runtime")
        streams = cls.parse_stream_details(data.find("fileinfo"))
        return media_library.Movie(
            title=title, year=year, duration=duration, streams=streams
        )

    @classmethod
    def parse_episode(cls, data: ET.Element) -> media_library.Episode:
        title = get_text(data, "title")
        year = get_int(data, "year")
        duration = get_duration(data, "runtime")
        season = get_int(data, "season")
        episode = get_int(data, "episode")
        streams = cls.parse_stream_details(data.find("fileinfo"))
        return media_library.Episode(
            title=title,
            year=year,
            duration=duration,
            season=season,
            episode=episode,
            streams=streams,
        )

    @classmethod
    def parse_series(cls, data: ET.Element) -> media_library.Series:
        title = get_text(data, "title")
        year = get_int(data, "year")
        season = get_int(data, "season")
        episode = get_int(data, "episode")
        episodes = [cls.parse_episode(tag) for tag in data.iter("episodedetails")]
        return media_library.Series(
            title=title, year=year, season=season, episode=episode, episodes=episodes,
        )

    @classmethod
    def parse_video_database(cls, data: ET.Element) -> media_library.VideoDatabase:
        return media_library.VideoDatabase(
            movies=[cls.parse_movie(tag) for tag in data.iter("movie")],
            series=[cls.parse_series(tag) for tag in data.iter("tvshow")],
        )


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
