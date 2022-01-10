import xml.etree.ElementTree as ET
from pathlib import Path

import mkv_info.library_xml
import mkv_info.media_library

DATA_DIR = Path("data")


def test_empty() -> None:
    data = ET.fromstring("""<empty/>""")
    assert (
        mkv_info.library_xml.XML_Parser.parse_stream_details(data)
        == mkv_info.media_library.StreamDetails()
    )
    assert (
        mkv_info.library_xml.XML_Parser.parse_movie(data)
        == mkv_info.media_library.Movie()
    )
    assert (
        mkv_info.library_xml.XML_Parser.parse_video_stream(data)
        == mkv_info.media_library.VideoStream()
    )
    assert (
        mkv_info.library_xml.XML_Parser.parse_audio_stream(data)
        == mkv_info.media_library.AudioStream()
    )
    assert (
        mkv_info.library_xml.XML_Parser.parse_sub_stream(data)
        == mkv_info.media_library.SubStream()
    )

    data = ET.fromstring("""<streamdetails></streamdetails>""")
    assert (
        mkv_info.library_xml.XML_Parser.parse_stream_details(data)
        == mkv_info.media_library.StreamDetails()
    )


def test_video_only_height() -> None:
    data = ET.fromstring(
        """
        <video>
            <height>864</height>
        </video>
        """
    )
    video_stream = mkv_info.library_xml.XML_Parser.parse_video_stream(data)
    assert video_stream == mkv_info.media_library.VideoStream(height=864)
    assert video_stream.codec is None
    assert video_stream.width is None
    assert video_stream.height == 864


def test_video_only_codec() -> None:
    data = ET.fromstring(
        """
        <video>
            <codec>h264</codec>
        </video>
        """
    )
    video_stream = mkv_info.library_xml.XML_Parser.parse_video_stream(data)
    assert video_stream == mkv_info.media_library.VideoStream(codec="h264")
    assert video_stream.codec == "h264"
    assert video_stream.width is None
    assert video_stream.height is None


def test_video_only_width() -> None:
    data = ET.fromstring(
        """
        <video>
            <width>1920</width>
        </video>
        """
    )
    video_stream = mkv_info.library_xml.XML_Parser.parse_video_stream(data)
    assert video_stream == mkv_info.media_library.VideoStream(width=1920)
    assert video_stream.codec is None
    assert video_stream.width == 1920
    assert video_stream.height is None


def test_video() -> None:
    data = ET.fromstring(
        """
        <video>
            <codec>h264</codec>
            <aspect>2.220000</aspect>
            <width>1920</width>
            <height>864</height>
            <durationinseconds>8932</durationinseconds>
            <stereomode></stereomode>
        </video>
        """
    )
    video_stream = mkv_info.library_xml.XML_Parser.parse_video_stream(data)
    assert video_stream == mkv_info.media_library.VideoStream(
        codec="h264", width=1920, height=864,
    )
    assert video_stream.codec == "h264"
    assert video_stream.width == 1920
    assert video_stream.height == 864


def test_audio_only_codec() -> None:
    data = ET.fromstring(
        """
        <audio>
            <codec>ac-3</codec>
        </audio>
        """
    )
    audio_stream = mkv_info.library_xml.XML_Parser.parse_audio_stream(data)
    assert audio_stream == mkv_info.media_library.AudioStream(codec="ac-3",)
    assert audio_stream.codec == "ac-3"
    assert audio_stream.language is None
    assert audio_stream.channels is None


def test_audio_only_language() -> None:
    data = ET.fromstring(
        """
        <audio>
            <language>eng</language>
        </audio>
        """
    )
    audio_stream = mkv_info.library_xml.XML_Parser.parse_audio_stream(data)
    assert audio_stream == mkv_info.media_library.AudioStream(language="eng",)
    assert audio_stream.codec is None
    assert audio_stream.language == "eng"
    assert audio_stream.channels is None


def test_audio_only_channels() -> None:
    data = ET.fromstring(
        """
        <audio>
            <channels>6</channels>
        </audio>
        """
    )
    audio_stream = mkv_info.library_xml.XML_Parser.parse_audio_stream(data)
    assert audio_stream == mkv_info.media_library.AudioStream(channels=6,)
    assert audio_stream.codec is None
    assert audio_stream.language is None
    assert audio_stream.channels == 6


def test_audio() -> None:
    data = ET.fromstring(
        """
        <audio>
            <codec>ac-3</codec>
            <language>eng</language>
            <channels>6</channels>
        </audio>
        """
    )
    audio_stream = mkv_info.library_xml.XML_Parser.parse_audio_stream(data)
    assert audio_stream == mkv_info.media_library.AudioStream(
        codec="ac-3", language="eng", channels=6,
    )
    assert audio_stream.codec == "ac-3"
    assert audio_stream.language == "eng"
    assert audio_stream.channels == 6


def test_sub() -> None:
    data = ET.fromstring(
        """
        <subtitle>
            <language>eng</language>
            <primary>True</primary>
        </subtitle>
        """
    )
    sub_stream = mkv_info.library_xml.XML_Parser.parse_sub_stream(data)
    assert sub_stream == mkv_info.media_library.SubStream(language="eng")
    assert sub_stream.language == "eng"


def test_streams() -> None:
    data = ET.fromstring(
        """
        <fileinfo>
            <streamdetails>
                <video>
                    <codec>h264</codec>
                    <aspect>2.220000</aspect>
                    <width>1920</width>
                    <height>864</height>
                    <durationinseconds>8932</durationinseconds>
                    <stereomode></stereomode>
                </video>
                <audio>
                    <codec>ac-3</codec>
                    <language>eng</language>
                    <channels>6</channels>
                </audio>
                <subtitle>
                    <language>eng</language>
                    <primary>True</primary>
                </subtitle>
                <subtitle>
                    <language>dut</language>
                    <primary>False</primary>
                </subtitle>
            </streamdetails>
        </fileinfo>
        """
    )
    stream_info = mkv_info.library_xml.XML_Parser.parse_stream_details(data)
    assert stream_info == mkv_info.media_library.StreamDetails(
        videos=(
            mkv_info.media_library.VideoStream(codec="h264", width=1920, height=864,),
        ),
        audios=(
            mkv_info.media_library.AudioStream(
                codec="ac-3", language="eng", channels=6,
            ),
        ),
        subs=(
            mkv_info.media_library.SubStream(language="eng",),
            mkv_info.media_library.SubStream(language="dut",),
        ),
    )
    assert len(stream_info.videos) == 1
    assert len(stream_info.audios) == 1
    assert len(stream_info.subs) == 2


def test_streams_only_video() -> None:
    data = ET.fromstring(
        """
        <fileinfo>
            <streamdetails>
                <video>
                    <codec>h264</codec>
                    <aspect>2.220000</aspect>
                    <width>1920</width>
                    <height>864</height>
                    <durationinseconds>8932</durationinseconds>
                    <stereomode></stereomode>
                </video>
            </streamdetails>
        </fileinfo>
        """
    )
    stream_info = mkv_info.library_xml.XML_Parser.parse_stream_details(data)
    assert stream_info == mkv_info.media_library.StreamDetails(
        videos=(
            mkv_info.media_library.VideoStream(codec="h264", width=1920, height=864,),
        ),
    )
    assert len(stream_info.videos) == 1
    assert len(stream_info.audios) == 0
    assert len(stream_info.subs) == 0
    data = ET.fromstring(
        """
        <fileinfo>
            <streamdetails>
                <video>
                    <codec>h264</codec>
                    <aspect>2.220000</aspect>
                    <width>1920</width>
                    <height>864</height>
                    <durationinseconds>8932</durationinseconds>
                    <stereomode></stereomode>
                </video>
                <video>
                    <codec>h265</codec>
                    <aspect>2.220000</aspect>
                    <width>1921</width>
                    <height>865</height>
                    <durationinseconds>8932</durationinseconds>
                    <stereomode></stereomode>
                </video>
            </streamdetails>
        </fileinfo>
        """
    )
    stream_info = mkv_info.library_xml.XML_Parser.parse_stream_details(data)
    assert stream_info == mkv_info.media_library.StreamDetails(
        videos=(
            mkv_info.media_library.VideoStream(codec="h264", width=1920, height=864,),
            mkv_info.media_library.VideoStream(codec="h265", width=1921, height=865,),
        ),
    )
    assert len(stream_info.videos) == 2
    assert len(stream_info.audios) == 0
    assert len(stream_info.subs) == 0


def test_streams_only_audio() -> None:
    data = ET.fromstring(
        """
        <fileinfo>
            <streamdetails>
                <audio>
                    <codec>ac-3</codec>
                    <language>eng</language>
                    <channels>6</channels>
                </audio>
            </streamdetails>
        </fileinfo>
        """
    )
    stream_info = mkv_info.library_xml.XML_Parser.parse_stream_details(data)
    assert stream_info == mkv_info.media_library.StreamDetails(
        audios=(
            mkv_info.media_library.AudioStream(
                codec="ac-3", language="eng", channels=6,
            ),
        ),
    )
    assert len(stream_info.videos) == 0
    assert len(stream_info.audios) == 1
    assert len(stream_info.subs) == 0
    data = ET.fromstring(
        """
        <fileinfo>
            <streamdetails>
                <audio>
                    <codec>ac-3</codec>
                    <language>eng</language>
                    <channels>6</channels>
                </audio>
                <audio>
                    <codec>ac-4</codec>
                    <language>dut</language>
                    <channels>7</channels>
                </audio>
            </streamdetails>
        </fileinfo>
        """
    )
    stream_info = mkv_info.library_xml.XML_Parser.parse_stream_details(data)
    assert stream_info == mkv_info.media_library.StreamDetails(
        audios=(
            mkv_info.media_library.AudioStream(
                codec="ac-3", language="eng", channels=6,
            ),
            mkv_info.media_library.AudioStream(
                codec="ac-4", language="dut", channels=7,
            ),
        ),
    )
    assert len(stream_info.videos) == 0
    assert len(stream_info.audios) == 2
    assert len(stream_info.subs) == 0


def test_streams_only_subs() -> None:
    data = ET.fromstring(
        """
        <fileinfo>
            <streamdetails>
                <subtitle>
                    <language>dut</language>
                    <primary>False</primary>
                </subtitle>
            </streamdetails>
        </fileinfo>
        """
    )
    stream_info = mkv_info.library_xml.XML_Parser.parse_stream_details(data)
    assert stream_info == mkv_info.media_library.StreamDetails(
        subs=(mkv_info.media_library.SubStream(language="dut",),),
    )
    assert len(stream_info.videos) == 0
    assert len(stream_info.audios) == 0
    assert len(stream_info.subs) == 1

    data = ET.fromstring(
        """
        <fileinfo>
            <streamdetails>
                <subtitle>
                    <language>eng</language>
                    <primary>True</primary>
                </subtitle>
                <subtitle>
                    <language>dut</language>
                    <primary>False</primary>
                </subtitle>
            </streamdetails>
        </fileinfo>
        """
    )
    stream_info = mkv_info.library_xml.XML_Parser.parse_stream_details(data)
    assert stream_info == mkv_info.media_library.StreamDetails(
        subs=(
            mkv_info.media_library.SubStream(language="eng",),
            mkv_info.media_library.SubStream(language="dut",),
        ),
    )
    assert len(stream_info.videos) == 0
    assert len(stream_info.audios) == 0
    assert len(stream_info.subs) == 2
