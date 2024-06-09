from enum import Enum
from io import TextIOWrapper
import os
from typing import Union, List
import yaml
import json


class MetadataFormat(Enum):
    yaml = "yaml"
    json = "json"


def get_metadata_format(filename: str):
    """
    filename:str name of the file with the extension

    determines the supported format of the metadata files.
    """
    _, ext = os.path.splitext(filename)
    try:
        ext = MetadataFormat(ext[1:])
        return ext
    except Exception:
        return None


def load_format(f: TextIOWrapper, format: MetadataFormat):
    """
    f: TextIOWrapper        file stream from an open command
    format: MetadataFormat  metadata format

    reads the filestream using the correct library to parse the file format type
    """
    if format == MetadataFormat.yaml:
        data = yaml.safe_load(f)
    elif format == MetadataFormat.json:
        data = json.load(f)
    return data

