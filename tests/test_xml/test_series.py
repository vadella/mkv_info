import datetime
import xml.etree.ElementTree as ET

import mkv_info.media_library
import mkv_info.library_xml


def test_episode() -> None:
    data = ET.fromstring(
        r"""
        <episodedetails>
            <title>Mhysa</title>
            <season>3</season>
            <episode>10</episode>
            <runtime>63 min</runtime>
            <fileinfo>
                <streamdetails>
                    <video>
                        <codec>h264</codec>
                        <aspect>1.65</aspect>
                        <width>1920</width>
                        <height>1168</height>
                        <durationinseconds>3764</durationinseconds>
                    </video>
                    <audio>
                        <codec>dts</codec>
                        <language>eng</language>
                        <channels>6</channels>
                    </audio>
                    <audio>
                        <codec>AAC</codec>
                        <language>eng</language>
                        <channels>2</channels>
                    </audio>
                    <subtitle>
                        <language>eng</language>
                        <primary>False</primary>
                    </subtitle>
                    <subtitle>
                        <language>eng</language>
                        <primary>False</primary>
                    </subtitle>
                    <subtitle>
                        <language>dut</language>
                        <primary>False</primary>
                    </subtitle>
                </streamdetails>
            </fileinfo>
        </episodedetails>
    """
    )
    episode = mkv_info.library_xml.XML_Parser.parse_episode(data)
    assert episode == mkv_info.media_library.Episode(
        title="Mhysa",
        duration=datetime.timedelta(minutes=63),
        season=3,
        episode=10,
        streams=mkv_info.media_library.StreamDetails(
            videos=(
                mkv_info.media_library.VideoStream(
                    codec="h264", width=1920, height=1168,
                ),
            ),
            audios=(
                mkv_info.media_library.AudioStream(
                    codec="dts", language="eng", channels=6,
                ),
                mkv_info.media_library.AudioStream(
                    codec="AAC", language="eng", channels=2,
                ),
            ),
            subs=(
                mkv_info.media_library.SubStream(language="eng",),
                mkv_info.media_library.SubStream(language="eng",),
                mkv_info.media_library.SubStream(language="dut",),
            ),
        ),
    )
    assert episode.title == "Mhysa"
    assert episode.duration == datetime.timedelta(minutes=63)
    assert episode.season == 3
    assert episode.episode == 10
    assert episode.streams == mkv_info.media_library.StreamDetails(
        videos=(
            mkv_info.media_library.VideoStream(
                codec="h264", width=1920, height=1168,
            ),
        ),
        audios=(
            mkv_info.media_library.AudioStream(
                codec="dts", language="eng", channels=6,
            ),
            mkv_info.media_library.AudioStream(
                codec="AAC", language="eng", channels=2,
            ),
        ),
        subs=(
            mkv_info.media_library.SubStream(language="eng",),
            mkv_info.media_library.SubStream(language="eng",),
            mkv_info.media_library.SubStream(language="dut",),
        ),
    )


def test_series() -> None:
    data = ET.fromstring(
        """
        <tvshow>
            <title>Game of Thrones</title>
            <season>3</season>
            <episode>60</episode>
            <year>2011</year>
            <episodedetails>
                <title>Mhysa</title>
                <season>3</season>
                <episode>10</episode>
                <runtime>63 min</runtime>
                <year></year>
                <fileinfo>
                    <streamdetails>
                        <video>
                            <codec>h264</codec>
                            <width>1920</width>
                            <height>1168</height>
                        </video>
                        <audio>
                            <codec>dts</codec>
                            <language>eng</language>
                            <channels>6</channels>
                        </audio>
                        <audio>
                            <codec>AAC</codec>
                            <language>eng</language>
                            <channels>2</channels>
                        </audio>
                        <subtitle>
                            <language>eng</language>
                            <primary>False</primary>
                        </subtitle>
                        <subtitle>
                            <language>eng</language>
                            <primary>False</primary>
                        </subtitle>
                        <subtitle>
                            <language>dut</language>
                            <primary>False</primary>
                        </subtitle>
                    </streamdetails>
                </fileinfo>
            </episodedetails>
        </tvshow>
        """
    )
    series = mkv_info.library_xml.XML_Parser.parse_series(data)

    assert series == mkv_info.media_library.Series(
        title="Game of Thrones",
        season=3,
        episode=60,
        year=2011,
        episodes=[
            mkv_info.media_library.Episode(
                title="Mhysa",
                duration=datetime.timedelta(minutes=63),
                season=3,
                episode=10,
                streams=mkv_info.media_library.StreamDetails(
                    videos=(
                        mkv_info.media_library.VideoStream(
                            codec="h264", width=1920, height=1168,
                        ),
                    ),
                    audios=(
                        mkv_info.media_library.AudioStream(
                            codec="dts", language="eng", channels=6,
                        ),
                        mkv_info.media_library.AudioStream(
                            codec="AAC", language="eng", channels=2,
                        ),
                    ),
                    subs=(
                        mkv_info.media_library.SubStream(language="eng",),
                        mkv_info.media_library.SubStream(language="eng",),
                        mkv_info.media_library.SubStream(language="dut",),
                    ),
                ),
            )
        ],
    )
    assert series.title == "Game of Thrones"
    assert series.season == 3
    assert series.episode == 60
    assert series.year == 2011
    assert series.episodes[0] == mkv_info.media_library.Episode(
        title="Mhysa",
        duration=datetime.timedelta(minutes=63),
        season=3,
        episode=10,
        streams=mkv_info.media_library.StreamDetails(
            videos=(
                mkv_info.media_library.VideoStream(
                    codec="h264", width=1920, height=1168,
                ),
            ),
            audios=(
                mkv_info.media_library.AudioStream(
                    codec="dts", language="eng", channels=6,
                ),
                mkv_info.media_library.AudioStream(
                    codec="AAC", language="eng", channels=2,
                ),
            ),
            subs=(
                mkv_info.media_library.SubStream(language="eng",),
                mkv_info.media_library.SubStream(language="eng",),
                mkv_info.media_library.SubStream(language="dut",),
            ),
        ),
    )
