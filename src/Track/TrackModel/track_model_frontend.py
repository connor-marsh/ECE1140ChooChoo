from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QMainWindow
from PyQt5.QtGui import QBrush, QPen, QColor, QPainter
from PyQt5.QtCore import Qt, QRectF, QTimer 
from Track.TrackModel.track_model_ui import Ui_MainWindow
from Track.TrackModel.track_model_backend import TrackModel

# HARDCODED LAYOUT DATA: (block_id, x, y, width, height)
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
    ("K68", 323, 286, 8, 16),
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
    ("Q100", 93, 356, 15, 14),
    ("R101", 187, 339, 29, 29),
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
    ("Z150", 56, 99, 27, 28),
    ("I0", 259, 141, 59, 21),
    ("J0", 324, 137, 8, 59),
]

class TrackMapCanvas(QGraphicsView):
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

    def mousePressEvent(self, event):
        item = self.itemAt(event.pos())
        if isinstance(item, QGraphicsRectItem) and item in self.block_lookup:
            block_id = self.block_lookup[item]
            if hasattr(self.parent(), "on_block_selected"):
                self.parent().on_block_selected(block_id)
        super().mousePressEvent(event)

    def update_block_colors(self):
        if not self.backend:
            return
        for block_id, item in self.block_items.items():
            occ = self.backend.dynamic_track.occupancies.get(block_id, 0)
            fail = self.backend.dynamic_track.failures.get(block_id, 0)
            if fail:
                item.setBrush(QBrush(QColor("yellow")))
            elif occ == 1:
                item.setBrush(QBrush(QColor("green")))
            else:
                item.setBrush(QBrush(QColor("gray")))

class TrackModelFrontEnd(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_map)
        self.update_timer.start(100)  # every 100 ms

        # Backend Setup
        self.green_line = TrackModel("Green")
        self.outside_temp = 70.0
        self.track_heater_status = False

        # Load Map Canvas into GraphicsView
        self.map_canvas = TrackMapCanvas(parent=self.ui.track_map_display)
        self.ui.track_map_display.setScene(self.map_canvas.scene)
        self.ui.track_map_display.setRenderHint(QPainter.Antialiasing)

        # Use hardcoded layout data
        self.map_canvas.load_from_backend(self.green_line, HARDCODED_LAYOUT)

        # Button Hooks
        self.ui.import_track_layout_button.clicked.connect(lambda: self.map_canvas.load_from_backend(self.green_line, HARDCODED_LAYOUT))
        self.ui.track_circuit_failure_toggle.clicked.connect(lambda: self.toggle_failure("track"))
        self.ui.broken_rail_failure_toggle.clicked.connect(lambda: self.toggle_failure("rail"))
        self.ui.power_failure_toggle.clicked.connect(lambda: self.toggle_failure("power"))
        self.ui.reset_errors_button.clicked.connect(self.reset_failures)

    def on_block_selected(self, block_id):
        self.display_block_info(block_id)
        self.map_canvas.update_block_colors()

    def display_block_info(self, block_id):
        block = next((b for b in self.green_line.track_data.blocks if b.id == block_id), None)
        if not block:
            print(f"Block {block_id} not found.")
            return

        self.ui.block_selected_value.setText(str(block_id))
        self.ui.block_length_value.setText(str(block.length))
        self.ui.speed_limit_value.setText(str(block.speed_limit))
        self.ui.underground_value.setText("Yes" if getattr(block, "underground", False) else "No")
        self.ui.elevation_value.setText(str(block.grade))
        self.ui.sum_elevation_value.setText(str(block.grade))  # You can replace with actual sum elevation if available

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
        self.map_canvas.update_block_colors()
