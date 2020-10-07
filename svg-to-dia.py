#!/usr/bin/env python3
# This is free and unencumbered software released into the public domain.

from argparse import ArgumentParser
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
import getpass
import re
import subprocess


@dataclass
class Sheet:
    name: str
    author: str
    description: str
    objects: dict


def build_sheet(sheet):
    xsheet = ET.Element(
        'sheet',
        attrib={'xmlns': 'http://www.lysator.liu.se/~alla/dia/dia-sheet-ns'}
    )
    if sheet.name:
        ET.SubElement(xsheet, 'name').text = sheet.name
    if sheet.author:
        ET.SubElement(xsheet, 'created_by').text = sheet.author
    if sheet.description:
        ET.SubElement(xsheet, 'description').text = sheet.description

    xcontents = ET.SubElement(xsheet, 'contents')
    for oname, odescription in sheet.objects.items():
        xobj = ET.SubElement(xcontents, 'object')
        xobj.attrib['name'] = oname
        ET.SubElement(xobj, 'description').text = odescription
    return xsheet


def get_float(s):
    return float(re.match(r'\d+([.]\d*)?', s)[0])


def build_shape(svg_path):
    orig_xsvg = ET.parse(str(svg_path)).getroot()

    xshape = ET.Element('shape', attrib={'xmlns': 'http://www.daa.com.au/~james/dia-shape-ns'})
    ET.SubElement(xshape, 'name').text = svg_path.stem
    ET.SubElement(xshape, 'icon').text = f"{svg_path.stem}.png"

    width = int(get_float(orig_xsvg.attrib['width']))
    height = int(get_float(orig_xsvg.attrib['height']))
    xconns = ET.SubElement(xshape, 'connections')
    points = [
        (0, 0),
        (0, width // 2),
        (0, width),
        (height // 2, 0),
        (height, 0),
    ]
    for x, y in points:
        ET.SubElement(xconns, 'point', attrib={'x': str(x), 'y': str(y)})

    ET.SubElement(xshape, 'aspectratio', attrib={'type': 'fixed'})
    xshape.append(orig_xsvg)

    return xshape


def main():
    aparser = ArgumentParser()
    aparser.add_argument('--name', default='TODO')
    aparser.add_argument('svg_file', nargs='+')
    args = aparser.parse_args()

    psheets = Path('sheets')
    psheets.mkdir(exist_ok=True)
    pshapes = Path('shapes')
    pshapes.mkdir(exist_ok=True)

    sheet = Sheet(
        name=args.name,
        author=getpass.getuser(),
        description=f"TODO: fill {args.name} description",
        objects={}
    )

    for svg_file in args.svg_file:
        svg_file = Path(svg_file)

        xshape = build_shape(svg_file)
        # ET.indent(xshape)
        tshape = ET.tostring(xshape, encoding='unicode')
        shape_path = pshapes.joinpath(f"{svg_file.stem}.shape")
        shape_path.write_text(tshape)
        print(f"wrote {shape_path}")

        png_file = f'{pshapes}/{svg_file.stem}.png'
        subprocess.check_call([
            'convert',
            str(svg_file),
            '-resize',
            '64x64',
            png_file,
        ])
        print(f"wrote {png_file}")

        sheet.objects[svg_file.stem] = f"TODO: fill description for {svg_file.stem}"

    xsheet = build_sheet(sheet)
    # ET.indent(xsheet)
    tsheet = ET.tostring(xsheet, encoding="unicode")
    sheet_path = psheets.joinpath(f"{args.name}.sheet")
    sheet_path.write_text(tsheet)
    print(f"wrote {sheet_path}")


if __name__ == '__main__':
    main()
