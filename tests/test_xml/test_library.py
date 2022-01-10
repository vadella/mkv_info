import datetime
import xml.etree.ElementTree as ET
from pathlib import Path

import mkv_info

import mkv_info.media_library
import mkv_info.library_xml

DATA_DIR = Path("data")


def test_library() -> None:
    data_file = DATA_DIR / "videodb_min.xml"
    tree = ET.parse(data_file)
    root = tree.getroot()
    library = mkv_info.library_xml.XML_Parser.parse_video_database(root)
    assert len(library.movies) == 4
    assert library.movies[0] == mkv_info.media_library.Movie(
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
