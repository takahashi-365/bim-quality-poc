# -*- coding: utf-8 -*-
# pyrevit_scripts/export_selected_element_metadata.py
# Phase 3C MVP:
# Export selected Revit element metadata to CSV.
#
# GitHub storage path:
#   pyrevit_scripts/export_selected_element_metadata.py
#
# Actual pyRevit button execution path may differ:
#   extension/tab/panel/pushbutton/script.py

from __future__ import print_function

import csv
import os
import codecs

from pyrevit import revit, forms
from Autodesk.Revit.DB import ElementId


doc = revit.doc
uidoc = revit.uidoc


# ------------------------------------------------------------
# Output path
# ------------------------------------------------------------
# NOTE:
# Revit / pyRevit execution current directory can be environment-dependent.
# For MVP, output to Desktop first so the user can find the file easily.
# After confirming output, manually copy it to:
#   03_input_csv/pyrevit_element_metadata_sample_v001.csv

desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")
output_path = os.path.join(desktop_dir, "pyrevit_element_metadata_sample_v001.csv")


# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------
def safe_text(value):
    if value is None:
        return ""
    try:
        return str(value)
    except Exception:
        try:
            return value.ToString()
        except Exception:
            return ""


def get_category_name(element):
    try:
        if element.Category:
            return safe_text(element.Category.Name)
    except Exception:
        pass
    return ""


def get_type_element(element):
    try:
        type_id = element.GetTypeId()
        if type_id and type_id != ElementId.InvalidElementId:
            return doc.GetElement(type_id)
    except Exception:
        pass
    return None


def get_family_name(element, type_element):
    # FamilyInstance such as Door usually has Symbol.Family.Name
    try:
        if hasattr(element, "Symbol") and element.Symbol and element.Symbol.Family:
            return safe_text(element.Symbol.Family.Name)
    except Exception:
        pass

    # Some type elements may expose FamilyName
    try:
        if type_element and hasattr(type_element, "FamilyName"):
            return safe_text(type_element.FamilyName)
    except Exception:
        pass

    return ""


def get_type_name(element, type_element):
    try:
        if type_element:
            return safe_text(type_element.Name)
    except Exception:
        pass

    try:
        return safe_text(element.Name)
    except Exception:
        pass

    return ""


def get_element_name(element):
    try:
        return safe_text(element.Name)
    except Exception:
        return ""


def get_level_name(element):
    try:
        level_id = element.LevelId
        if level_id and level_id != ElementId.InvalidElementId:
            level = doc.GetElement(level_id)
            if level:
                return safe_text(level.Name)
    except Exception:
        pass

    # Some Room-like elements may have Level property
    try:
        if hasattr(element, "Level") and element.Level:
            return safe_text(element.Level.Name)
    except Exception:
        pass

    return ""


def get_room_name_number_if_room(element):
    # Initial MVP:
    # RoomName / RoomNumber are optional.
    # Only fill them when the selected element itself is a Room.
    # Do not infer RoomName / RoomNumber from Door or other elements.

    category_name = get_category_name(element)

    is_room = category_name in ["Rooms", "Room", "部屋", "ルーム"]

    if not is_room:
        return "", ""

    room_name = ""
    room_number = ""

    try:
        room_name = safe_text(element.Name)
    except Exception:
        pass

    try:
        room_number = safe_text(element.Number)
    except Exception:
        pass

    return room_name, room_number


def collect_metadata(element):
    type_element = get_type_element(element)
    room_name, room_number = get_room_name_number_if_room(element)

    return {
        "ElementId": safe_text(element.Id.IntegerValue),
        "UniqueId": safe_text(element.UniqueId),
        "Category": get_category_name(element),
        "FamilyName": get_family_name(element, type_element),
        "TypeName": get_type_name(element, type_element),
        "Name": get_element_name(element),
        "LevelName": get_level_name(element),
        "RoomName": room_name,
        "RoomNumber": room_number,
    }


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
selected_ids = list(uidoc.Selection.GetElementIds())

if not selected_ids:
    forms.alert(
        "要素が選択されていません。\nRevit上で要素を選択してから再実行してください。\nCSVは出力しません。",
        title="Phase 3C pyRevit Metadata Export",
        warn_icon=True,
    )
else:
    rows = []

    for element_id in selected_ids:
        element = doc.GetElement(element_id)
        if element:
            rows.append(collect_metadata(element))

    if not rows:
        forms.alert(
            "選択要素からメタデータを取得できませんでした。\nCSVは出力しません。",
            title="Phase 3C pyRevit Metadata Export",
            warn_icon=True,
        )
    else:
        fieldnames = [
            "ElementId",
            "UniqueId",
            "Category",
            "FamilyName",
            "TypeName",
            "Name",
            "LevelName",
            "RoomName",
            "RoomNumber",
        ]

        # UTF-8 with BOM for easier Excel confirmation with Japanese text.
        with codecs.open(output_path, "w", "utf-8-sig") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator="\n")
            writer.writeheader()
            for row in rows:
                writer.writerow(row)

        forms.alert(
            "選択要素のメタデータをCSV出力しました。\n\n{}".format(output_path),
            title="Phase 3C pyRevit Metadata Export",
            warn_icon=False,
        )