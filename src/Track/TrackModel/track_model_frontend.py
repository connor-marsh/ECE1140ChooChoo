from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QMainWindow
from PyQt5.QtGui import QBrush, QPen, QColor, QPainter
from PyQt5.QtCore import Qt, QRectF, QTimer, pyqtSignal
from PyQt5.QtWidgets import QGraphicsPixmapItem, QVBoxLayout
from PyQt5.QtGui import QPixmap
from Track.TrackModel.track_model_ui import Ui_MainWindow
from Track.TrackModel.track_model_backend import TrackModel
from Track.TrackModel.track_model_enums import Occupancy
from Track.TrackModel.track_model_enums import Failures

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# HARDCODED LAYOUT DATA: (block_id, x, y, width, height) GREEN LINE
HARDCODED_LAYOUT = [
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

# Icon file paths (relative to your project structure)
ICON_PATHS = {
    "train": os.path.join(BASE_DIR, "Resources/train_icon.png"),
    "station": os.path.join(BASE_DIR, "Resources/station_icon.jpeg"),
    "switch": os.path.join(BASE_DIR, "Resources/switch_icon.png"),
    "traffic_light": os.path.join(BASE_DIR, "Resources/traffic_light_icon.png"),
    "railway_crossing": os.path.join(BASE_DIR, "Resources/railway_crossing_icon.png")
}

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
        for block_id, item in self.block_items.items():
            occ = self.backend.dynamic_track.occupancies.get(block_id, Occupancy.UNOCCUPIED)
            fail = self.backend.dynamic_track.failures.get(block_id, Failures.NONE)
            if fail != Failures.NONE:
                item.setBrush(QBrush(QColor("yellow")))
            elif occ == Occupancy.OCCUPIED:
                item.setBrush(QBrush(QColor("green")))
            else:
                item.setBrush(QBrush(QColor("gray")))

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

        for tid in list(self.train_icons.keys()):
            if tid not in current_ids:
                self.scene.removeItem(self.train_icons[tid])
                del self.train_icons[tid]



class TrackModelFrontEnd(QMainWindow):
    def __init__(self, wayside_integrated=True):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_map)
        self.update_timer.start(100)  # every 100 ms

        # Backend Setup
        #self.red_line
        self.green_line = TrackModel("Green", wayside_integrated=wayside_integrated)
        self.outside_temp = 70.0
        self.track_heater_status = False

        # Load Map Canvas into GraphicsView
        # Create a canvas and embed it into the track_map_display placeholder
        self.map_canvas = TrackMapCanvas(self.ui.track_map_display)
        self.map_canvas.blockClicked.connect(self.on_block_selected)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.map_canvas)
        self.ui.track_map_display.setLayout(layout)

        # Buttons to zoom in and out
        #self.ui.zoom_in_button.clicked.connect(self.map_canvas.zoom_in)
        #self.ui.zoom_out_button.clicked.connect(self.map_canvas.zoom_out)

        # Mapping combobox with physical blocks
        self.block_number_to_id = {}
        self.block_id_to_number = {}

        # Populate mappings
        for idx, (block_id, *_rest) in enumerate(HARDCODED_LAYOUT, start=1):
            self.block_number_to_id[str(idx)] = block_id
            self.block_id_to_number[block_id] = str(idx)

        self.map_canvas.load_from_backend(self.green_line, HARDCODED_LAYOUT)
        self.populate_block_combobox(HARDCODED_LAYOUT)


        # Button Hooks
        self.ui.import_track_layout_button.clicked.connect(lambda: self.map_canvas.load_from_backend(self.green_line, HARDCODED_LAYOUT))
        self.ui.track_circuit_failure_toggle.clicked.connect(lambda: self.toggle_failure("track"))
        self.ui.broken_rail_failure_toggle.clicked.connect(lambda: self.toggle_failure("rail"))
        self.ui.power_failure_toggle.clicked.connect(lambda: self.toggle_failure("power"))
        self.ui.reset_errors_button.clicked.connect(self.reset_failures)

        self.ui.block_number_selected.currentTextChanged.connect(self.on_combobox_selected)

        # Signals for icons being clicked
        self.map_canvas.iconClicked.connect(self.on_icon_clicked)
        self.map_canvas.trainIconClicked.connect(self.on_train_icon_clicked)

    # Displays the current block selected
    def on_block_selected(self, block_id):
        print(f"[DEBUG] Looking for block_number of {block_id} -> {self.block_id_to_number.get(block_id)}")
        self.display_block_info(block_id)
        block_number = self.block_id_to_number.get(block_id)
        if block_number:
            self.ui.block_number_selected.blockSignals(True)
            self.ui.block_number_selected.setCurrentText(block_number)
            self.ui.block_number_selected.blockSignals(False)
        else:
            print(f"[WARNING] No block number found for block_id: {block_id}")


        self.map_canvas.update_block_colors()

        selected_item = self.map_canvas.block_items.get(block_id)
        if selected_item:
            for item in self.map_canvas.block_items.values():
                item.setPen(QPen(Qt.black, 0.5))
            selected_item.setPen(QPen(Qt.red, 2))

    def display_block_info(self, block_id):
        block = next((b for b in self.green_line.track_data.blocks if b.id == block_id), None)
        if not block:
            print(f"Block {block_id} not found.")
            return

        occ = self.green_line.dynamic_track.occupancies.get(block_id, Occupancy.UNOCCUPIED)
        fail = self.green_line.dynamic_track.failures.get(block_id, Failures.NONE)
        heater = self.track_heater_status
        temp = self.outside_temp

        self.ui.block_selected_value.setText(str(block_id))
        self.ui.block_length_value.setText(f"{float(block.length):.2f}")
        self.ui.speed_limit_value.setText(f"{float(block.speed_limit):.2f}")
        self.ui.underground_value.setText("Yes" if getattr(block, "underground", False) else "No")
        self.ui.elevation_value.setText(f"{block.grade:.2f}")
        self.ui.grade_value.setText(f"{block.grade:.2f}")

        # Wayside Authority
        authority = self.green_line.runtime_status.get(block_id, {}).get("wayside_authority", "N/A")
        self.ui.wayside_authority_value.setText(f"{authority}" if authority != "N/A" else "N/A")

        # Wayside Speed
        speed = self.green_line.runtime_status.get(block_id, {}).get("wayside_speed", "N/A")
        self.ui.wayside_speed_value.setText(f"{speed}" if speed != "N/A" else "N/A")

        # Travel Direction from Excel (section info)
        section_id = block_id[0]
        section = self.green_line.track_data.sections.get(section_id)
        if section:
            if section.increasing == 0:
                direction = "Descending"
            elif section.increasing == 1:
                direction = "Ascending"
            elif section.increasing == 2:
                direction = "Bidirectional"
            else:
                direction = "Unknown"
        else:
            direction = "Unknown"
        self.ui.direction_of_travel_value.setText(direction)

        # Beacon Data
        beacon = self.green_line.track_data.beacons.get(block_id)
        self.ui.beacon_value.setText(beacon.data if beacon else "None")

        # Railway Crossing Status
        crossing_state = self.green_line.dynamic_track.crossing_states.get(block_id, False)
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
        current = self.green_line.dynamic_track.failures.get(block_id, 0)
        self.green_line.dynamic_track.failures[block_id] = 0 if current else 1
        self.map_canvas.update_block_colors()

    def reset_failures(self):
        for block_id in self.green_line.dynamic_track.failures:
            self.green_line.dynamic_track.failures[block_id] = 0
        self.map_canvas.update_block_colors()

    def update_map(self):
        # Update block colors based on occupancy/failure
        self.map_canvas.update_block_colors()

        # Build a dict of train_id -> current block_id directly from backend
        train_data = {
            train.train_id: train.current_block.id
            for train in self.green_line.trains
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
        if icon_type == "station":
            station = self.green_line.track_data.stations.get(block_id)
            if station:
                boarding_side = (
                    "Left" if station.doors == 0 else
                    "Right" if station.doors == 1 else
                    "Both"
                )
                print(f"[STATION INFO]")
                print(f"  Block: {block_id}")
                print(f"  Name: {station.name}")
                print(f"  Boarding Side: {boarding_side}")
                print(f"  Ticket Sales: IMPLEMENT")
                print(f"  Passengers Boarding: IMPLEMENT")
                print(f"  Passengers Departing: IMPLEMENT")
            else:
                print(f"[STATION CLICKED] No station found for block {block_id}")

        elif icon_type == "switch":
            switch = self.green_line.track_data.switches.get(block_id)
            state = self.green_line.dynamic_track.switch_states.get(block_id)
            if switch and state is not None:
                route = switch.positions[1 if state else 0]
                print(f"[SWITCH INFO]")
                print(f"  Block: {block_id}")
                print(f"  Current Route: {route}")
            else:
                print(f"[SWITCH CLICKED] No switch found for block {block_id}")

        elif icon_type == "railway_crossing":
            print(f"[CROSSING CLICKED] Block: {block_id}")
            # You could print active/inactive here later

        elif icon_type == "traffic_light":
            print(f"[TRAFFIC LIGHT CLICKED] Block: {block_id}")
            # Could add red/green status here too

        else:
            print(f"[ICON CLICKED] Unknown icon type: {icon_type} on block {block_id}")

    # Displays train specific information
    def on_train_icon_clicked(self, train_id):
        if 0 <= train_id < len(self.green_line.trains):
            train = self.green_line.trains[train_id]
            data = train.train_model.get_output_data()
            position = data.get("position", 0.0)
            speed = data.get("actual_speed", 0.0)
            wayside_speed = data.get("wayside_speed", 0.0)
            authority = data.get("wayside_authority", 0.0)

            print(f"[TRAIN {train_id} INFO]")
            print(f"  Current Block: {train.current_block.id}")
            print(f"  Passengers On Board: {train.passenger_count}")
            print(f"  Actual Speed (mph): {speed:.2f}")
            print(f"  Wayside Speed (mph): {wayside_speed:.2f}")
            print(f"  Wayside Authority (yd): {authority:.2f}")
            print(f"  Direction: {'Ascending' if train.travel_direction else 'Descending'}")
        else:
            print(f"[TRAIN CLICKED] Train {train_id} not found.")



if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = TrackModelFrontEnd(wayside_integrated=False)
    window.show()
    sys.exit(app.exec_())
