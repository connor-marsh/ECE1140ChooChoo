"""
Author: PJ Granieri
Date: 04-24-2025
Description:
"""

from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QMainWindow, QGraphicsPixmapItem, QVBoxLayout, QFileDialog, QMessageBox
from PyQt5.QtGui import QBrush, QPen, QColor, QPainter, QPixmap, QCloseEvent
from PyQt5.QtCore import Qt, QRectF, QTimer, pyqtSignal
from Track.TrackModel.track_model_ui import Ui_MainWindow
from Track.TrackModel.track_model_backend import TrackModel
from Track.TrackModel.track_model_enums import Occupancy
from Track.TrackModel.track_model_enums import Failures
import globals.global_clock as global_clock
import globals.track_data_class as track_data_class
import globals.signals as signals

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# HARDCODED LAYOUT DATA: (block_id, x, y, width, height) GREEN LINE
HARDCODED_LAYOUT_GREEN = [
    ("A1", 174, 7, 13, 14),
    ("A2", 181, 16, 13, 14),
    ("A3", 188, 25, 13, 14),
    ("B4", 197, 34, 17, 13),
    ("B5", 210, 40, 18, 12),
    ("B6", 226, 44, 17, 8),
    ("C7", 241, 39, 24, 14),
    ("C8", 258, 25, 15, 21),
    ("C9", 249, 16, 23, 15),
    ("C10", 232, 11, 22, 12),
    ("C11", 206, 7, 28, 12),
    ("C12", 173, 7, 34, 8),
    ("D13", 159, 5, 14, 8),
    ("D14", 145, 5, 14, 8),
    ("D15", 131, 5, 14, 8),
    ("D16", 117, 5, 14, 8),
    ("E17", 102, 4, 17, 13),
    ("E18", 92, 9, 14, 14),
    ("E19", 83, 18, 14, 15),
    ("E20", 79, 30, 10, 13),
    ("F21", 79, 43, 8, 7),
    ("F22", 79, 50, 8, 7),
    ("F23", 79, 57, 8, 7),
    ("F24", 79, 64, 8, 7),
    ("F25", 79, 71, 8, 7),
    ("F26", 79, 78, 8, 7),
    ("F27", 79, 85, 8, 7),
    ("F28", 79, 92, 8, 7),
    ("G29", 79, 99, 8, 8),
    ("G30", 79, 107, 8, 8),
    ("G31", 79, 115, 8, 8),
    ("G32", 79, 123, 8, 8),
    ("H33", 77, 130, 13, 17),
    ("H34", 84, 142, 16, 17),
    ("H35", 95, 152, 19, 9),
    ("I36", 108, 154, 7, 8),
    ("I37", 115, 154, 7, 8),
    ("I38", 122, 154, 7, 8),
    ("I39", 129, 154, 7, 8),
    ("I40", 136, 154, 7, 8),
    ("I41", 143, 154, 7, 8),
    ("I42", 150, 154, 7, 8),
    ("I43", 157, 154, 7, 8),
    ("I44", 164, 154, 7, 8),
    ("I45", 171, 154, 7, 8),
    ("I46", 178, 154, 7, 8),
    ("I47", 185, 154, 7, 8),
    ("I48", 192, 154, 7, 8),
    ("I49", 199, 154, 7, 8),
    ("I50", 206, 154, 7, 8),
    ("I51", 213, 154, 7, 8),
    ("I52", 220, 154, 7, 8),
    ("I53", 227, 154, 7, 8),
    ("I54", 234, 154, 7, 8),
    ("I55", 241, 154, 7, 8),
    ("I56", 248, 154, 7, 8),
    ("I57", 255, 154, 7, 8),
    ("J58", 259, 154, 21, 10),
    ("J59", 278, 156, 20, 12),
    ("J60", 294, 161, 20, 16),
    ("J61", 308, 171, 18, 18),
    ("J62", 321, 185, 10, 22),
    ("K63", 323, 206, 8, 16),
    ("K64", 323, 222, 8, 16),
    ("K65", 323, 238, 8, 16),
    ("K66", 323, 254, 8, 16),
    ("K67", 323, 270, 8, 16),
    ("K68", 323, 286, 8, 21), # Originally 8, 16
    ("L69", 323, 306, 8, 17),
    ("L70", 320, 322, 10, 17),
    ("L71", 310, 335, 15, 20),
    ("L72", 298, 345, 19, 18),
    ("L73", 279, 358, 24, 12),
    ("M74", 251, 363, 29, 8),
    ("M75", 222, 363, 29, 8),
    ("M76", 193, 363, 29, 8),
    ("N77", 184, 363, 9, 8),
    ("N78", 175, 363, 9, 8),
    ("N79", 166, 363, 9, 8),
    ("N80", 157, 363, 9, 8),
    ("N81", 148, 363, 9, 8),
    ("N82", 139, 363, 9, 8),
    ("N83", 130, 363, 9, 8),
    ("N84", 121, 363, 9, 8),
    ("N85", 112, 363, 9, 8),
    ("O86", 98, 363, 15, 8),
    ("O87", 83, 363, 15, 8),
    ("O88", 68, 363, 15, 8),
    ("P89", 49, 356, 22, 15),
    ("P90", 43, 343, 14, 19),
    ("P91", 43, 333, 8, 15),
    ("P92", 43, 319, 10, 16),
    ("P93", 45, 307, 15, 16),
    ("P94", 54, 303, 15, 12),
    ("P95", 64, 304, 15, 10),
    ("P96", 73, 308, 13, 16),
    ("P97", 78, 320, 10, 19),
    ("Q98", 80, 336, 13, 17),
    ("Q99", 86, 348, 15, 15),
    ("Q100", 93, 356, 12, 8), # Oirignally 15, 14
    ("R101", 187, 339, 25, 24), # Originally 29, 29
    ("S102", 211, 339, 14, 8),
    ("S103", 225, 339, 14, 8),
    ("S104", 239, 339, 14, 8),
    ("T105", 251, 336, 21, 11),
    ("T106", 268, 327, 20, 16),
    ("T107", 282, 315, 18, 19),
    ("T108", 294, 303, 13, 17),
    ("T109", 299, 286, 11, 20),
    ("U110", 302, 278, 8, 8),
    ("U111", 302, 270, 8, 8),
    ("U112", 302, 262, 8, 8),
    ("U113", 302, 254, 8, 8),
    ("U114", 302, 246, 8, 8),
    ("U115", 302, 238, 8, 8),
    ("U116", 302, 230, 8, 8),
    ("V117", 299, 213, 11, 18),
    ("V118", 294, 197, 13, 18),
    ("V119", 284, 186, 18, 18),
    ("V120", 268, 177, 21, 15),
    ("V121", 243, 173, 28, 11),
    ("W122", 237, 173, 7, 8),
    ("W123", 230, 173, 7, 8),
    ("W124", 223, 173, 7, 8),
    ("W125", 216, 173, 7, 8),
    ("W126", 209, 173, 7, 8),
    ("W127", 202, 173, 7, 8),
    ("W128", 195, 173, 7, 8),
    ("W129", 188, 173, 7, 8),
    ("W130", 181, 173, 7, 8),
    ("W131", 174, 173, 7, 8),
    ("W132", 167, 173, 7, 8),
    ("W133", 160, 173, 7, 8),
    ("W134", 153, 173, 7, 8),
    ("W135", 146, 173, 7, 8),
    ("W136", 139, 173, 7, 8),
    ("W137", 132, 173, 7, 8),
    ("W138", 125, 173, 7, 8),
    ("W139", 118, 173, 7, 8),
    ("W140", 111, 173, 7, 8),
    ("W141", 104, 173, 7, 8),
    ("W142", 97, 173, 7, 8),
    ("W143", 90, 173, 7, 8),
    ("X144", 76, 170, 16, 11),
    ("X145", 64, 164, 15, 13),
    ("X146", 57, 153, 13, 17),
    ("Y147", 56, 144, 8, 11),
    ("Y148", 56, 133, 8, 11),
    ("Y149", 56, 122, 8, 11),
    ("Z150", 56, 99, 25, 28),# Originally 27, 28
    ("y151", 324, 137, 8, 59), # Entrance block
    ("y152", 259, 148, 59, 8), # Originally 259, 141, 59, 21, DESPAWN block
]

# RED LINE
HARDCODED_LAYOUT_RED = [
    ("A1", 231, 91, 16, 10),
    ("A2", 244, 86, 16, 12),
    ("A3", 256, 78, 16, 14),
    ("B4", 264, 64, 12, 17),
    ("B5", 270, 55, 16, 15),
    ("B6", 282, 52, 16, 11),
    ("C7", 299, 52, 16, 10),
    ("C8", 313, 54, 18, 12),
    ("C9", 326, 61, 19, 16),
    ("D10", 325, 79, 20, 15),
    ("D11", 308, 88, 20, 13),
    ("D12", 286, 93, 24, 11),
    ("E13", 269, 96, 18, 8),
    ("E14", 251, 96, 18, 8),
    ("E15", 233, 96, 18, 8),
    ("F16", 227, 96, 6, 8),
    ("F17", 220, 96, 7, 8),
    ("F18", 213, 96, 7, 8),
    ("F19", 206, 96, 7, 8),
    ("F20", 199, 96, 7, 8),
    ("G21", 185, 96, 14, 10),
    ("G22", 170, 101, 16, 14),
    ("G23", 166, 106, 14, 16),
    ("H24", 166, 118, 8, 7),
    ("H25", 166, 125, 8, 7),
    ("H26", 166, 132, 8, 7),
    ("H27", 166, 139, 8, 7),
    ("H28", 166, 146, 8, 7),
    ("H29", 166, 153, 8, 7),
    ("H30", 166, 160, 8, 7),
    ("H31", 166, 167, 8, 7),
    ("H32", 166, 174, 8, 7),
    ("H33", 166, 181, 8, 7),
    ("H34", 166, 188, 8, 7),
    ("H35", 166, 195, 8, 7),
    ("H36", 166, 202, 8, 7),
    ("H37", 166, 209, 8, 7),
    ("H38", 166, 216, 8, 7),
    ("H39", 166, 223, 8, 7),
    ("H40", 166, 230, 8, 7),
    ("H41", 166, 237, 8, 7),
    ("H42", 166, 244, 8, 7),
    ("H43", 166, 251, 8, 6),
    ("H44", 166, 257, 8, 6),
    ("H45", 165, 263, 8, 6),
    ("I46", 156, 265, 14, 17),
    ("I47", 145, 276, 16, 13),
    ("I48", 130, 282, 18, 13),
    ("J49", 119, 287, 11, 8),
    ("J50", 108, 287, 11, 8),
    ("J51", 97, 287, 11, 8),
    ("J52", 86, 287, 11, 8),
    ("J53", 75, 287, 11, 8),
    ("J54", 64, 287, 11, 8),
    ("K55", 45, 280, 20, 15),
    ("K56", 30, 266, 20, 22),
    ("K57", 22, 246, 14, 25),
    ("L58", 23, 231, 10, 16),
    ("L59", 27, 217, 12, 17),
    ("L60", 34, 211, 20, 13),
    ("M61", 49, 211, 22, 22),
    ("M62", 64, 229, 12, 24),
    ("M63", 68, 252, 10, 21),
    ("N64", 69, 271, 12, 11),
    ("N65", 75, 278, 12, 11),
    ("N66", 82, 284, 12, 11),
    ("O67", 149, 233, 19, 13),
    ("P68", 145, 229, 8, 8),
    ("P69", 145, 219, 8, 10),
    ("P70", 145, 211, 8, 8),
    ("Q71", 148, 201, 19, 14),
    ("R72", 149, 163, 19, 11),
    ("S73", 144, 158, 8, 9),
    ("S74", 144, 149, 8, 9),
    ("S75", 144, 141, 8, 8),
    ("T76", 149, 134, 19, 12),
    ("y77", 327, 86, 16, 36),  # Yard block
]


# Icon file paths
ICON_PATHS = {
    "train": os.path.join(BASE_DIR, "Resources/train_icon.png"),
    "station": os.path.join(BASE_DIR, "Resources/station_icon.jpeg"),
    "switch": os.path.join(BASE_DIR, "Resources/switch_icon.png"),
    "traffic_light": os.path.join(BASE_DIR, "Resources/traffic_light_icon.png"),
    "railway_crossing": os.path.join(BASE_DIR, "Resources/railway_crossing_icon.png")
}

ICON_PATHS.update({
    "failure_track": os.path.join(BASE_DIR, "Resources/track_circuit_failure_icon.png"),
    "failure_rail": os.path.join(BASE_DIR, "Resources/broken_rail_icon.png"),
    "failure_power": os.path.join(BASE_DIR, "Resources/power_failure_icon.png")
})


class TrackMapCanvas(QGraphicsView):
    blockClicked = pyqtSignal(str)
    iconClicked = pyqtSignal(str, str)  # (icon_type, block_id)
    trainIconClicked = pyqtSignal(int)  # train_id

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.scale_factor = 1.0
        self.min_scale = 0.2
        self.max_scale = 5.0
        self.offset_x = 66

        # Start semi-scaled out - cover whole map layout
        self.scale(0.8, 0.8)

        self.scale_factor = 0.8

        self.block_items = {}
        self.block_lookup = {}
        self.backend = None

        self.infrastructure_icons = []
        self.train_icons = {}  # key: train_id, value: QGraphicsPixmapItem
        


    def wheelEvent(self, event):
        zoom_in_factor = 1.15
        zoom_out_factor = 1 / zoom_in_factor

        if event.angleDelta().y() > 0 and self.scale_factor < self.max_scale:
            self.scale(zoom_in_factor, zoom_in_factor)
            self.scale_factor *= zoom_in_factor
        elif event.angleDelta().y() < 0 and self.scale_factor > self.min_scale:
            self.scale(zoom_out_factor, zoom_out_factor)
            self.scale_factor *= zoom_out_factor

    def load_from_backend(self, backend, layout_data):
        self.backend = backend
        self.scene.clear()
        self.block_items.clear()
        self.block_lookup.clear()

        for label, x, y, w, h in layout_data:
            w = max(8, w)
            h = max(8, h)
            rect = QGraphicsRectItem(QRectF(self.offset_x + x, y, w, h))
            rect.setBrush(QBrush(QColor("gray")))
            rect.setPen(QPen(Qt.black, 0.5))
            rect.setFlag(QGraphicsRectItem.ItemIsSelectable)
            self.scene.addItem(rect)
            self.block_items[label] = rect
            self.block_lookup[rect] = label

        self.update_block_colors()
        self.add_infrastructure_icons()
        self.train_icons.clear()

    # Allows interaction with physical map
    def mousePressEvent(self, event):
        scene_pos = self.mapToScene(event.pos())
        item = self.scene.itemAt(scene_pos, self.transform())

        if isinstance(item, QGraphicsPixmapItem) and item.data(0):
            icon_type = item.data(0)
            if icon_type == "train":
                train_id = item.data(1)
                self.trainIconClicked.emit(train_id)
                return
            block_id = item.data(1)
            self.iconClicked.emit(icon_type, block_id)

        elif isinstance(item, QGraphicsRectItem) and item in self.block_lookup:
            block_id = self.block_lookup[item]
            self.blockClicked.emit(block_id)

        super().mousePressEvent(event)

    def update_block_colors(self):
        if not self.backend:
            return

        # Update block colors based on occupancy and general failure presence
        for block_id, item in self.block_items.items():
            occ = self.backend.dynamic_track.occupancies.get(block_id, Occupancy.UNOCCUPIED)
            fail = self.backend.dynamic_track.failures.get(block_id, Failures.NONE)

            if fail != Failures.NONE:
                item.setBrush(QBrush(QColor("yellow")))
            elif occ == Occupancy.OCCUPIED:
                item.setBrush(QBrush(QColor("green")))
            else:
                item.setBrush(QBrush(QColor("gray")))

        # --- Failure Icon Handling ---

        # Clear existing failure icons
        for item in self.infrastructure_icons[:]:
            try:
                if item is None or item.scene() is None:
                    self.infrastructure_icons.remove(item)
                    continue
                if item.data(0) in ("failure_track", "failure_rail", "failure_power"):
                    self.scene.removeItem(item)
                    self.infrastructure_icons.remove(item)
            except RuntimeError:
                if item in self.infrastructure_icons:
                    self.infrastructure_icons.remove(item)
                continue


        # Add new failure icons
        for block_id, failure in self.backend.dynamic_track.failures.items():
            if failure == Failures.NONE:
                continue

            rect = self.block_items.get(block_id)
            if not rect:
                continue

            rect_pos = rect.sceneBoundingRect()
            x, y = rect_pos.x(), rect_pos.y()

            icon_type = {
                Failures.TRACK_CIRCUIT_FAILURE: "failure_track",
                Failures.BROKEN_RAIL_FAILURE: "failure_rail",
                Failures.POWER_FAILURE: "failure_power"
            }.get(failure)

            if icon_type:
                pixmap = QPixmap(ICON_PATHS[icon_type]).scaled(14, 14, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                icon = QGraphicsPixmapItem(pixmap)
                icon.setZValue(9)  # Ensure it overlays above blocks
                icon.setData(0, icon_type)
                icon.setData(1, block_id)
                icon.setPos(x + 2, y + 2)
                self.scene.addItem(icon)
                self.infrastructure_icons.append(icon)


    def add_infrastructure_icons(self):
        self.infrastructure_icons.clear()
        for block in self.backend.track_data.blocks:
            block_id = block.id
            rect = self.block_items.get(block_id)
            if not rect:
                continue
            rect_pos = rect.sceneBoundingRect()
            x, y = rect_pos.x(), rect_pos.y()

            if getattr(block, "station", None):
                path = ICON_PATHS["station"]
                pixmap = QPixmap(path).scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                icon = QGraphicsPixmapItem(pixmap)
                icon.setData(0, "station")    # icon type
                icon.setData(1, block_id)     # block ID
                icon.setPos(x + 10, y - 20)
                icon.setAcceptedMouseButtons(Qt.LeftButton)
                icon.setFlag(QGraphicsPixmapItem.ItemIsSelectable, True)
                icon.setFlag(QGraphicsPixmapItem.ItemIsFocusable, True)
                self.scene.addItem(icon)
                self.infrastructure_icons.append(icon)

            if getattr(block, "switch", False):
                path = ICON_PATHS["switch"]
                pixmap = QPixmap(path).scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                icon = QGraphicsPixmapItem(pixmap)
                icon.setData(0, "switch")     # icon type
                icon.setData(1, block_id)     # block ID
                icon.setPos(x - 10, y - 10)
                icon.setAcceptedMouseButtons(Qt.LeftButton)
                icon.setFlag(QGraphicsPixmapItem.ItemIsSelectable, True)
                icon.setFlag(QGraphicsPixmapItem.ItemIsFocusable, True)
                self.scene.addItem(icon)
                self.infrastructure_icons.append(icon)


            if getattr(block, "light", False):
                path = ICON_PATHS["traffic_light"]
                pixmap = QPixmap(path).scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                icon = QGraphicsPixmapItem(pixmap)
                icon.setData(0, "traffic_light")    # icon type
                icon.setData(1, block_id)           # block ID
                icon.setPos(x + 5, y + 5)
                icon.setAcceptedMouseButtons(Qt.LeftButton)
                icon.setFlag(QGraphicsPixmapItem.ItemIsSelectable, True)
                icon.setFlag(QGraphicsPixmapItem.ItemIsFocusable, True)                
                self.scene.addItem(icon)
                self.infrastructure_icons.append(icon)

            if getattr(block, "crossing", False):
                path = ICON_PATHS["railway_crossing"]
                pixmap = QPixmap(path).scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                icon = QGraphicsPixmapItem(pixmap)
                icon.setData(0, "railway_crossing")     # icon type
                icon.setData(1, block_id)               # block ID
                icon.setPos(x - 20, y)
                icon.setAcceptedMouseButtons(Qt.LeftButton)
                icon.setFlag(QGraphicsPixmapItem.ItemIsSelectable, True)
                icon.setFlag(QGraphicsPixmapItem.ItemIsFocusable, True)  
                self.scene.addItem(icon)
                self.infrastructure_icons.append(icon)

            def zoom_in(self):
                if self.scale_factor < self.max_scale:
                    zoom_factor = 1.15
                    self.scale(zoom_factor, zoom_factor)
                    self.scale_factor *= zoom_factor

            def zoom_out(self):
                if self.scale_factor > self.min_scale:
                    zoom_factor = 1 / 1.15
                    self.scale(zoom_factor, zoom_factor)
                    self.scale_factor *= zoom_factor

    def update_train_icons(self, train_data):
        current_ids = set(train_data.keys())

        for train_id, block_id in train_data.items():
            if block_id not in self.block_items:
                continue

            block_rect = self.block_items[block_id].sceneBoundingRect()
            x = block_rect.x() + block_rect.width() / 2 - 8
            y = block_rect.y() + block_rect.height() / 2 - 8

            if train_id not in self.train_icons:
                path = ICON_PATHS["train"]
                pixmap = QPixmap(path).scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                icon = QGraphicsPixmapItem(pixmap)
                icon.setZValue(10)
                icon.setData(0, "train")
                icon.setData(1, train_id)
                icon.setAcceptedMouseButtons(Qt.LeftButton)
                icon.setFlag(QGraphicsPixmapItem.ItemIsSelectable, True)
                icon.setFlag(QGraphicsPixmapItem.ItemIsFocusable, True)
                self.scene.addItem(icon)
                self.train_icons[train_id] = icon

            self.train_icons[train_id].setPos(x, y)

        # Remove all existing train icons safely if not in train_data
        for tid in list(self.train_icons.keys()):
            icon = self.train_icons.get(tid)
            if tid not in current_ids and icon is not None and not icon.scene() is None:
                self.scene.removeItem(icon)
                del self.train_icons[tid]


###############################################################################
# Dynamic Infrastructure Display Class
###############################################################################

class InfrastructureDisplay(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(350, 130)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.name_text = None
        self.icon_item = None
        self.label_items = []
        self.value_items = []

        self.switch_graphics = {}
        self.init_display()

    def init_display(self):
        self.scene.clear()

        self.name_text = self.scene.addText("")
        self.name_text.setPos(5, 5)

        self.icon_item = QGraphicsPixmapItem()
        self.icon_item.setPos(5, 25)
        self.scene.addItem(self.icon_item)

        for i in range(5):
            y = 6 + i * 24
            label = self.scene.addText("")
            label.setPos(114, y)
            value = self.scene.addText("")
            value.setPos(279, y)
            self.label_items.append(label)
            self.value_items.append(value)

        self.switch_graphics = {
            "icon": QGraphicsPixmapItem(),
            "entrance_text": self.scene.addText(""),
            "exit_top_text": self.scene.addText(""),
            "exit_bottom_text": self.scene.addText("")
        }

        # Position switch image
        self.switch_graphics["icon"].setPos(120, 10)
        self.scene.addItem(self.switch_graphics["icon"])

        # Position labels (no rectangles, just text)
        self.switch_graphics["entrance_text"].setPos(65, 25)      # Entrance
        self.switch_graphics["exit_top_text"].setPos(260, 25)     # Top exit (horizontal)
        self.switch_graphics["exit_bottom_text"].setPos(260, 88)  # Bottom exit (vertical drop from top)

        # Initially hidden
        for item in self.switch_graphics.values():
            item.setVisible(False)

    def update_display(self, icon_type, data_dict):
        # Clear generic text/icons
        self.name_text.setPlainText("")
        self.icon_item.setPixmap(QPixmap())

        for label, value in zip(self.label_items, self.value_items):
            label.setPlainText("")
            value.setPlainText("")

        for item in self.switch_graphics.values():
            item.setVisible(False)

        # Non-switch display
        if icon_type != "switch":
            self.name_text.setPlainText(data_dict.get("name", ""))
            icon_path = data_dict.get("icon_path")
            if icon_path and os.path.exists(icon_path):
                pixmap = QPixmap(icon_path).scaled(96, 96, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.icon_item.setPixmap(pixmap)
            for i in range(5):
                line_key = f"line{i+1}"
                label, value = data_dict.get(line_key, ("", ""))
                self.label_items[i].setPlainText(label)
                self.value_items[i].setPlainText(value)
            return

        # Switch display logic
        icon_path = data_dict.get("icon_path")
        if icon_path and os.path.exists(icon_path):
            pixmap = QPixmap(icon_path).scaled(110, 110, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.switch_graphics["icon"].setPixmap(pixmap)
            self.switch_graphics["icon"].setVisible(True)

        # Strip section from entrance (e.g., I57 → 57)
        entrance_block = str(data_dict.get("entrance", ""))
        entrance_display = ''.join(filter(str.isdigit, entrance_block))

        # Exit blocks (use as-is)
        exit_top = str(data_dict.get("exit_top", ""))
        exit_bottom = str(data_dict.get("exit_bottom", ""))

        self.switch_graphics["entrance_text"].setPlainText(entrance_display)
        self.switch_graphics["exit_top_text"].setPlainText(exit_top)
        self.switch_graphics["exit_bottom_text"].setPlainText(exit_bottom)

        self.switch_graphics["entrance_text"].setVisible(True)
        self.switch_graphics["exit_top_text"].setVisible(True)
        self.switch_graphics["exit_bottom_text"].setVisible(True)




###############################################################################
# Track Frontend
###############################################################################

class TrackModelFrontEnd(QMainWindow):
    def __init__(self, wayside_integrated=True):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Track Model")

        self.track_models = {}
        self.current_line_name = None

        self.wayside_integrated = wayside_integrated
        self.initialize_models()


        self.global_clock = global_clock.clock
        self.ui.simulation_value.setText(str(self.global_clock.time_multiplier))

        signals.communication_track.track_temperature.connect(self.update_temperature_display)
        self.ui.track_temperature_value.editingFinished.connect(self.handle_temperature_input)

        # Create canvas and infrastructure displays
        self.map_canvas = TrackMapCanvas(self.ui.track_map_display)
        self.map_canvas.blockClicked.connect(self.on_block_selected)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.map_canvas)
        self.ui.track_map_display.setLayout(layout)

        # Dynamic Infrastructure Display
        self.infrastructure_display = InfrastructureDisplay()
        infra_layout = QVBoxLayout()
        infra_layout.setContentsMargins(0, 0, 0, 0)
        infra_layout.addWidget(self.infrastructure_display)


        # If group_infrasturcture has no layout, set one
        if not self.ui.group_infrasturcture.layout():
            self.ui.group_infrasturcture.setLayout(QVBoxLayout())

        self.ui.group_infrasturcture.layout().removeWidget(self.ui.infrastructure_view)
        self.ui.infrastructure_view.deleteLater()
        self.ui.group_infrasturcture.layout().addLayout(infra_layout)

        # Set up backend based on initial selection
        selected_text = self.ui.track_line_selected.currentText()
        self.setup_line(selected_text)

        # Hook combobox for changing track lines
        self.ui.track_line_selected.currentTextChanged.connect(self.setup_line)

        # Other button hooks
        self.ui.import_track_layout_button.clicked.connect(self.import_new_track_layout)
        self.ui.track_circuit_failure_toggle.clicked.connect(lambda: self.toggle_failure("track"))
        self.ui.broken_rail_failure_toggle.clicked.connect(lambda: self.toggle_failure("rail"))
        self.ui.power_failure_toggle.clicked.connect(lambda: self.toggle_failure("power"))
        self.ui.reset_errors_button.clicked.connect(self.reset_failures)

        self.ui.block_number_selected.currentTextChanged.connect(self.on_combobox_selected)

        # Signals for icons being clicked
        self.map_canvas.iconClicked.connect(self.on_icon_clicked)
        self.map_canvas.trainIconClicked.connect(self.on_train_icon_clicked)

        self.map_timer = QTimer(self)
        self.map_timer.timeout.connect(self.update_map)
        self.map_timer.start(100)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(500)

        self.block_coords = {
            block_id: (x, y)
            for (block_id, x, y, *_rest) in self.layout_data
        }

        # Set key icons for the map legend
        self.ui.train_icon.setPixmap(QPixmap(ICON_PATHS["train"]).scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.ui.station_icon.setPixmap(QPixmap(ICON_PATHS["station"]).scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.ui.switch_icon.setPixmap(QPixmap(ICON_PATHS["switch"]).scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.ui.traffic_signal_icon.setPixmap(QPixmap(ICON_PATHS["traffic_light"]).scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.ui.railway_crossing_icon.setPixmap(QPixmap(ICON_PATHS["railway_crossing"]).scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.ui.maintenance_icon.setPixmap(QPixmap(os.path.join(BASE_DIR, "Resources/maintenance_icon.png")).scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.ui.track_circuit_failure_icon.setPixmap(QPixmap(ICON_PATHS["failure_track"]).scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.ui.broken_rail_failure_icon.setPixmap(QPixmap(ICON_PATHS["failure_rail"]).scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.ui.power_failure_icon.setPixmap(QPixmap(ICON_PATHS["failure_power"]).scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation))



    def setup_line(self, selected_text):
        line_key = selected_text.strip().replace(" Line", "")
        layout = HARDCODED_LAYOUT_GREEN if line_key == "Green" else HARDCODED_LAYOUT_RED



        # Hide previous model's wayside UI if switching
        if self.current_line_name and self.current_line_name != line_key:
            prev_model = self.track_models[self.current_line_name]
            if hasattr(prev_model.wayside_collection, 'frontend'):
                prev_model.wayside_collection.frontend.closeEvent(event=QCloseEvent(),source=True)
            if hasattr(self.current_line.train_collection, 'train_model_ui'):
                prev_model.train_collection.train_model_ui.hide()
            if hasattr(self.current_line.train_collection, 'train_controller_ui'):
                prev_model.train_collection.train_controller_ui.hide()

        # Activate the new model
        line_key = selected_text.strip().replace(" Line", "")
        self.current_line = self.track_models[line_key]
        self.current_line_name = line_key


        # Show current line’s wayside UI
        if hasattr(self.current_line.wayside_collection, 'frontend'):
            self.current_line.wayside_collection.frontend.show()
        if hasattr(self.current_line.train_collection, 'train_model_ui'):
            self.current_line.train_collection.train_model_ui.show()
        if hasattr(self.current_line.train_collection, 'train_controller_ui'):
            self.current_line.train_collection.train_controller_ui.show()

        self.layout_data = layout
        self.map_canvas.load_from_backend(self.current_line, layout)

        self.block_number_to_id = {}
        self.block_id_to_number = {}
        for idx, (block_id, *_rest) in enumerate(layout, start=1):
            self.block_number_to_id[str(idx)] = block_id
            self.block_id_to_number[block_id] = str(idx)

        self.populate_block_combobox(layout)


    def initialize_models(self):
        from globals.track_data_class import lines
        for line_name in lines:
            self.track_models[line_name] = TrackModel(line_name, self.wayside_integrated)
            if line_name != "Green": # gonna default to hide any windows not for the green line
                if hasattr(self.track_models[line_name].wayside_collection, 'frontend'):
                    self.track_models[line_name].wayside_collection.frontend.closeEvent(event=QCloseEvent(),source=True)
                if hasattr(self.track_models[line_name].train_collection, 'train_model_ui'):
                    self.track_models[line_name].train_collection.train_model_ui.hide()
                if hasattr(self.track_models[line_name].train_collection, 'train_controller_ui'):
                    self.track_models[line_name].train_collection.train_controller_ui.hide()

    def update(self):
        try:
            simUpdateSpeed = int(self.ui.simulation_value.text())
        except ValueError:
            simUpdateSpeed = self.global_clock.time_multiplier
        if simUpdateSpeed >= 0 and simUpdateSpeed <= self.global_clock.MAX_MULTIPLIER:
            self.global_clock.time_multiplier = simUpdateSpeed

        # Update the global clock display
        self.ui.clock_display_value.display(self.global_clock.text)
        self.ui.clock_am_display.setText(self.global_clock.am_pm)


    # Displays the current block selected
    def on_block_selected(self, block_id):
        self.display_block_info(block_id)
        block_number = self.block_id_to_number.get(block_id)
        if block_number:
            self.ui.block_number_selected.blockSignals(True)
            self.ui.block_number_selected.setCurrentText(block_number)
            self.ui.block_number_selected.blockSignals(False)
        else:
            print(f"[WARNING] No block number found for block_id: {block_id}")

        # Update frontend display if selected block is shown
        block_id = self.ui.block_selected_value.text()
        if block_id:
            self.display_block_info(block_id)



        self.map_canvas.update_block_colors()

        selected_item = self.map_canvas.block_items.get(block_id)
        if selected_item:
            for item in self.map_canvas.block_items.values():
                item.setPen(QPen(Qt.black, 0.5))
            selected_item.setPen(QPen(Qt.red, 2))

    def display_block_info(self, block_id):
        block = next((b for b in self.current_line.track_data.blocks if b.id == block_id), None)
        if not block:
            print(f"Block {block_id} not found.")
            return

        occ = self.current_line.dynamic_track.occupancies.get(block_id, Occupancy.UNOCCUPIED)
        fail = self.current_line.dynamic_track.failures.get(block_id, Failures.NONE)
        temp = self.current_line.temperature
        heater = self.current_line.heater_status.get(block_id, False)



        self.ui.block_selected_value.setText(str(block_id))
        self.ui.block_length_value.setText(f"{float(block.length):.2f}")
        self.ui.speed_limit_value.setText(f"{float(block.speed_limit):.2f}")
        self.ui.underground_value.setText("Yes" if getattr(block, "underground", False) else "No")
        self.ui.elevation_value.setText(f"{block.grade:.2f}")
        self.ui.grade_value.setText(f"{block.grade:.2f}")

        # Wayside Authority
        authority = self.current_line.runtime_status.get(block_id, {}).get("wayside_authority", "N/A")
        self.ui.wayside_authority_value.setText(f"{authority}" if authority != "N/A" else "N/A")

        # Wayside Speed
        speed = self.current_line.runtime_status.get(block_id, {}).get("wayside_speed", "N/A")
        self.ui.wayside_speed_value.setText(f"{speed}" if speed != "N/A" else "N/A")

        # Travel Direction from Excel (section info)
        section_id = block_id[0]
        section = self.current_line.track_data.sections.get(section_id)
        if section:
            if section.increasing == 0:
                direction = "East"
            elif section.increasing == 1:
                direction = "West"
            elif section.increasing == 2:
                direction = "Both"
            else:
                direction = "Unknown"
        else:
            direction = "Unknown"
        self.ui.direction_of_travel_value.setText(direction)

        # Beacon Data
        beacon = self.current_line.track_data.beacons.get(block_id)
        self.ui.beacon_value.setText(beacon.data if beacon else "None")

        # Railway Crossing Status
        crossing_state = self.current_line.dynamic_track.crossing_states.get(block_id, False)
        self.ui.railway_crossing_value.setText("Active" if crossing_state else "Inactive")

        # Environmental Info
        self.ui.track_temperature_value.setText(f"{temp:.1f}")
        self.ui.track_heater_value.setText("Enabled" if heater else "Disabled")

        # Highlighting Occupancy/Failures
        if fail != Failures.NONE:
            self.ui.block_selected_value.setStyleSheet("color: orange;")
        elif occ == Occupancy.OCCUPIED:
            self.ui.block_selected_value.setStyleSheet("color: green;")
        else:
            self.ui.block_selected_value.setStyleSheet("color: black;")


    def toggle_failure(self, kind):
        block_id = self.ui.block_selected_value.text()
        current = self.current_line.dynamic_track.failures.get(block_id, Failures.NONE)

        if kind == "track":
            new_val = Failures.NONE if current == Failures.TRACK_CIRCUIT_FAILURE else Failures.TRACK_CIRCUIT_FAILURE
        elif kind == "power":
            new_val = Failures.NONE if current == Failures.POWER_FAILURE else Failures.POWER_FAILURE
        elif kind == "rail":
            new_val = Failures.NONE if current == Failures.BROKEN_RAIL_FAILURE else Failures.BROKEN_RAIL_FAILURE
        else:
            print(f"[ERROR] Unknown failure kind: {kind}")
            return

        self.current_line.dynamic_track.failures[block_id] = new_val

        self.map_canvas.update_block_colors()


    def reset_failures(self):
        # Clear all failures in backend
        for block_id in self.current_line.dynamic_track.failures:
            self.current_line.dynamic_track.failures[block_id] = Failures.NONE

        # Force recheck of occupancy states (especially for rail/power failures)
        self.current_line.update_occupancies_from_failures()

        # Refresh UI block colors
        self.map_canvas.update_block_colors()

        # Update info panel if block is selected
        selected_block_id = self.ui.block_selected_value.text


    def update_map(self):
        # Update block colors based on occupancy/failure
        self.map_canvas.update_block_colors()

        # Build a dict of train_id -> current block_id directly from backend
        train_data = {
            train.train_id: train.current_block.id
            for train in self.current_line.trains
            if train.current_block  # Ensure valid block
        }

        # Update train icons on the map
        self.map_canvas.update_train_icons(train_data)


    # Outlines physical selected block
    def on_combobox_selected(self, block_number):
        block_id = self.block_number_to_id.get(block_number)
        if block_id and block_id in self.map_canvas.block_items:
            self.display_block_info(block_id)
            self.map_canvas.update_block_colors()
            selected_item = self.map_canvas.block_items[block_id]
            for item in self.map_canvas.block_items.values():
                item.setPen(QPen(Qt.black, 0.5))
            selected_item.setPen(QPen(Qt.red, 2))


    # Populates the combobox to link with physical block
    def populate_block_combobox(self, layout_data):
        self.ui.block_number_selected.blockSignals(True)
        self.ui.block_number_selected.clear()
        self.ui.block_number_selected.addItems([str(i) for i in range(1, len(layout_data) + 1)])
        self.ui.block_number_selected.blockSignals(False)

        if layout_data:
            first_block = self.block_number_to_id["1"]
            self.ui.block_number_selected.setCurrentText("1")
            self.display_block_info(first_block)

    # Displays specific infrasturcture information
    def on_icon_clicked(self, icon_type, block_id):
        line = self.map_canvas.backend

        if icon_type == "station":
            station = line.track_data.stations.get(block_id)
            if station:
                boarding_side = (
                    "Left" if station.doors == 0 else
                    "Right" if station.doors == 1 else
                    "Both"
                )

                # Get live backend values from runtime_status
                status = line.runtime_status.get(block_id, {})
                ticket_sales = status.get("ticket_sales", "N/A")
                boarding = status.get("boarding", "N/A")
                departing = status.get("departing", "N/A")

                print(f"[STATION INFO]")
                print(f"  Block: {block_id}")
                print(f"  Name: {station.name}")
                print(f"  Boarding Side: {boarding_side}")
                print(f"  Ticket Sales: {ticket_sales}")
                print(f"  Passengers Boarding: {boarding}")
                print(f"  Passengers Departing: {departing}")
            else:
                print(f"[STATION CLICKED] No station found for block {block_id}")

        elif icon_type == "switch":
            switch = line.track_data.switches.get(block_id)
            state = line.dynamic_track.switch_states.get(block_id)
            if switch and state is not None:
                route = switch.positions[1 if state else 0]
                print(f"[SWITCH INFO]")
                print(f"  Block: {block_id}")
                print(f"  Current Route: {route}")
            else:
                print(f"[SWITCH CLICKED] No switch found for block {block_id}")

        elif icon_type == "railway_crossing":
            crossing_state = line.dynamic_track.crossing_states.get(block_id, False)
            print(f"[CROSSING INFO]")
            print(f"  Block: {block_id}")
            print(f"  State: {'Active' if crossing_state else 'Inactive'}")

        elif icon_type == "traffic_light":
            light_state = line.dynamic_track.light_states.get(block_id, False)
            print(f"[TRAFFIC LIGHT INFO]")
            print(f"  Block: {block_id}")
            print(f"  State: {'Green' if light_state else 'Red'}")

        else:
            print(f"[ICON CLICKED] Unknown icon type: {icon_type} on block {block_id}")

        payload = self.build_infrastructure_display_payload(icon_type, block_id)
        if payload:
            self.infrastructure_display.update_display(icon_type, payload)


    # Sends Dynamic Infrastructure payload data
    def build_infrastructure_display_payload(self, icon_type, block_id):
        backend = self.current_line
        status = backend.runtime_status.get(block_id, {})
        payload = {"name": "", "icon_path": "", "line1": ("", ""), "line2": ("", ""), "line3": ("", ""), "line4": ("", ""), "line5": ("", "")}

        if icon_type == "station":
            station = backend.track_data.stations.get(block_id)
            if not station:
                return None
            boarding_side = "Left" if station.doors == 0 else "Right" if station.doors == 1 else "Both"
            train_present = status.get("train_present", False)

            # Determine icon
            if station.doors == 0:
                icon = "station_icon_left_train.png" if train_present else "station_icon_left_no_train.png"
            elif station.doors == 1:
                icon = "station_icon_right_train.png" if train_present else "station_icon_right_no_train.png"
            else:
                icon = "station_icon_both_train.png" if train_present else "station_icon_both_no_train.png"

            payload.update({
                "name": station.name,
                "icon_path": os.path.join(BASE_DIR, "Resources", icon),
                "line1": ("Ticket Sales", str(status.get("ticket_sales", "N/A"))),
                "line2": ("Boarding", str(status.get("boarding", "N/A"))),
                "line3": ("Departing", str(status.get("departing", "N/A")))
            })

        elif icon_type == "switch":
            switch = backend.track_data.switches.get(block_id)
            if not switch:
                return None
            state = backend.dynamic_track.switch_states.get(block_id, False)
            route = switch.positions[1 if state else 0]

            try:
                entrance_0, exit_0 = switch.positions[0].split("-")
                entrance_1, exit_1 = switch.positions[1].split("-")
            except ValueError:
                print(f"[ERROR] Malformed switch position string for block {block_id}: {switch.positions}")
                return None

            # Always treat exit_0 as top and exit_1 as bottom - fixed logic
            top_exit = exit_0
            bottom_exit = exit_1

            # Determine which route is active
            route_exit = route.split("-")[1]

            # Set icon direction based on which exit is active (not relabeling)
            direction_icon = "switch_icon_up.png" if route_exit == top_exit else "switch_icon_down.png"

            payload.update({
                "name": "Switch",
                "icon_path": os.path.join(BASE_DIR, "Resources", direction_icon),
                "entrance": block_id,
                "exit_top": top_exit,
                "exit_bottom": bottom_exit
            })

            print(f"[SWITCH PAYLOAD] block_id={block_id}, route={route}, icon={direction_icon}, top={top_exit}, bottom={bottom_exit}")


            payload.update({
                "name": "Switch",
                "icon_path": os.path.join(BASE_DIR, "Resources", direction_icon),
                "entrance": block_id,
                "exit_top": top_exit,
                "exit_bottom": bottom_exit
            })

            print(f"[SWITCH PAYLOAD] block_id={block_id}, state={state}, route={route}, direction_icon={direction_icon}")



        elif icon_type == "railway_crossing":
            crossing_state = backend.dynamic_track.crossing_states.get(block_id, False)
            payload.update({
                "name": "Railway Crossing",
                "icon_path": os.path.join(BASE_DIR, "Resources",
                    "railway_crossing_icon_active.png" if crossing_state else "railway_crossing_icon_inactive.png"),
                "line1": ("State", "Active" if crossing_state else "Inactive")
            })

        elif icon_type == "traffic_light":
            light_state = backend.dynamic_track.light_states.get(block_id, False)
            payload.update({
                "name": "Traffic Light",
                "icon_path": os.path.join(BASE_DIR, "Resources",
                    "traffic_light_icon_green.png" if light_state else "traffic_light_icon_red.png"),
                "line1": ("State", "Green" if light_state else "Red")
            })

        elif icon_type == "train":
            return None

        return payload



    # Displays train specific information
    def on_train_icon_clicked(self, train_id):
        if 0 <= train_id < len(self.current_line.trains):
            train = self.current_line.trains[train_id]
            data = train.train_model.get_output_data()

            block_id = train.current_block.id if train.current_block else "N/A"
            passengers = train.passenger_count
            speed = data.get("actual_speed", 0.0)
            wayside_speed = data.get("wayside_speed", 0.0)
            authority = data.get("wayside_authority", 0.0)
            direction = "Ascending" if train.travel_direction else "Descending"

            payload = {
                "name": f"Train {train_id}",
                "icon_path": ICON_PATHS["train"],
                "line1": ("Location", str(block_id)),
                "line2": ("Passengers", str(passengers)),
                "line3": ("Actual Speed", f"{speed:.2f} mph"),
                "line4": ("Wayside Speed", f"{wayside_speed:.2f} mph"),
                "line5": ("Authority", f"{authority:.2f} yd")
            }

            self.infrastructure_display.update_display("train", payload)

        else:
            print(f"[TRAIN CLICKED] Train {train_id} not found.")

    # Allow excel files to be upload for new tracks
    def import_new_track_layout(self):
        from openpyxl import load_workbook

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Import Track Layout Excel",
            "",
            "Excel Files (*.xlsx *.xls)"
        )

        if not file_path:
            return

        try:
            if not file_path.endswith((".xlsx", ".xls")):
                raise ValueError("Only Excel files (.xlsx or .xls) are allowed.")

            wb = load_workbook(filename=file_path, data_only=True)
            sheet = wb["Sheet1"]
            line_name_cell = sheet["A2"].value.strip() if sheet["A2"].value else ""

            expected_line = self.current_line_name  # "Green" or "Red"
            if line_name_cell != expected_line:
                raise ValueError(f"File is for line '{line_name_cell}', but you are on the '{expected_line}' line.")

            # Parse new layout into global data
            track_data_class.init(file_path)

            # Replace backend for this line
            self.track_models[expected_line] = TrackModel(expected_line, self.wayside_integrated)

            # Reload UI if it's the current line
            self.setup_line(f"{expected_line} Line")

            QMessageBox.information(self, "Success", f"{expected_line} Line layout loaded successfully.")

        except Exception as e:
            QMessageBox.critical(self, "Import Error", f"Track layout import failed:\n{e}")

    # Temperature input handler
    def handle_temperature_input(self):
        try:
            temp = float(self.ui.track_temperature_value.text())
            temp = max(min(temp, 140.0), -140.0)
            self.current_line.set_temperature(temp)
            self.current_line.update_heaters()  # <-- force heater logic to update immediately
            self.update_temperature_display(temp, self.current_line_name)  # <-- refresh display
        except ValueError:
            fallback_temp = 35.0
            self.ui.track_temperature_value.setText(f"{fallback_temp:.1f}")
            self.current_line.set_temperature(fallback_temp)
            self.current_line.update_heaters()
            self.update_temperature_display(fallback_temp, self.current_line_name)



    def update_temperature_display(self, new_temp, line_name):
        if line_name != self.current_line_name:
            return

        self.ui.track_temperature_value.setText(f"{new_temp:.1f}")

        heater_on = any(
            self.current_line.heater_status.get(block.id, False)
            for block in self.current_line.track_data.blocks
        )
        self.ui.track_heater_value.setText("Enabled" if heater_on else "Disabled")

        # Force UI panel update for selected block
        selected = self.ui.block_selected_value.text()
        if selected:
            self.display_block_info(selected)






if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = TrackModelFrontEnd(wayside_integrated=False)
    window.show()
    sys.exit(app.exec_())
