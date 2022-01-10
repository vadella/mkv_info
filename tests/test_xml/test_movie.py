import datetime
import xml.etree.ElementTree as ET

import mkv_info.library_xml
import mkv_info.media_library


def test_movie() -> None:
    data = ET.fromstring(
        """
        <movie>
            <title>2001: A Space Odyssey</title>
            <runtime>149</runtime>
            <year>1968</year>
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
        </movie>
        """
    )
    movie = mkv_info.library_xml.XML_Parser.parse_movie(data)
    assert movie == mkv_info.media_library.Movie(
        title="2001: A Space Odyssey",
        duration=datetime.timedelta(minutes=149),
        year=1968,
        streams=mkv_info.media_library.StreamDetails(
            videos=(
                mkv_info.media_library.VideoStream(
                    codec="h264", width=1920, height=864,
                ),
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
        ),
    )
