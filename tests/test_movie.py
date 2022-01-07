import datetime
import xml.etree.ElementTree as ET

import mkv_info.library_xml as library_xml


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
    movie = library_xml.Movie.from_data(data)
    assert movie == library_xml.Movie(
        title="2001: A Space Odyssey",
        duration=datetime.timedelta(minutes=149),
        year=1968,
        streams=library_xml.StreamDetails(
            videos=(
                library_xml.VideoStream(codec="h264", width=1920, height=864,),
            ),
            audios=(
                library_xml.AudioStream(
                    codec="ac-3", language="eng", channels=6,
                ),
            ),
            subs=(
                library_xml.SubStream(language="eng",),
                library_xml.SubStream(language="dut",),
            ),
        ),
    )
