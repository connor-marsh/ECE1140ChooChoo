# When infrastructure is displayed, show it (station, switches, railway crossings, lights) / May also put trains here

# For each train on the track, display a train icon correlating to each train & include train name label above train icon

# Retrieving switch postions (0 is for lower # connection, 1 is for higher # connection)
# Ex: (5;6) & (5;11) (0 = 6), (1 = 11)

# Retrieving railway crossing state

# Retrieving light states

from Track.TrackModel.track_model_backend import TrackModel
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QTableWidgetItem, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsTextItem
from PyQt5.QtGui import QBrush, QColor, QPen, QPainter
from PyQt5.QtCore import Qt

###############################################################################
# Tr UI Class
###############################################################################
class TrackMapCanvas(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.scale_factor = 1.0
        self.min_scale = 0.2
        self.max_scale = 5.0

        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.block_items = {}
        self.train_icons = {}
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

    def load_from_backend(self, track_model):
        self.backend = track_model
        self.scene.clear()
        self.block_items.clear()
        self.train_icons.clear()
        self.draw_blocks()

    def draw_blocks(self):
        for block in self.backend.track_data.blocks:
            block_id = block.id
            index = int(block_id[1:]) if block_id[1:].isdigit() else 0
            # Implement each block

            # Make each item a rectangle? - prob
            item.setPos(x, y)
            item.setBrush(QBrush(QColor("gray")))
            item.setPen(QPen(Qt.black))
            item.setFlag(QGraphicsEllipseItem.ItemIsSelectable)
            self.scene.addItem(item)

            label = QGraphicsTextItem(block_id)
            label.setDefaultTextColor(Qt.black)
            label.setPos(x, y) # figure pos out
            self.scene.addItem(label)

            self.block_items[block_id] = item

    def update_block_states(self):
        if not self.backend:
            return

        for block in self.backend.track_data.blocks:
            item = self.block_items.get(block.id)
            if not item:
                continue

            occ = self.backend.dynamic_track.occupancies.get(block.id, 0)
            fail = self.backend.dynamic_track.failures.get(block.id, 0)

            if fail:
                item.setBrush(QBrush(QColor("yellow")))
            elif occ == 1:
                item.setBrush(QBrush(QColor("green")))
            else:
                item.setBrush(QBrush(QColor("gray")))

    def update_trains(self):
        if not self.backend:
            return

        for icon in self.train_icons.values():
            self.scene.removeItem(icon)
        self.train_icons.clear()

        for train in self.backend.trains:
            block = train.current_block
            block_item = self.block_items.get(block.id)
            if not block_item:
                continue
            
            # Physical "Train"
            pos = block_item.pos()
            icon = QGraphicsEllipseItem(-5, -5, 10, 10)
            icon.setPos(pos.x(), pos.y()) # Figure this out
            icon.setBrush(QBrush(Qt.black))
            self.scene.addItem(icon)

            label = QGraphicsTextItem(f"Train {train.train_id}")
            label.setDefaultTextColor(Qt.black)
            label.setPos(pos.x() - 10, pos.y() + 30)
            self.scene.addItem(label)

            self.train_icons[train.train_id] = icon


###############################################################################
# Main Track Model UI Class
###############################################################################

class TrackModelFrontEnd(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.red_line = TrackModel("Red")
        self.green_line = TrackModel("Green")
        self.outside_temp = 70.0
        self.track_heater_status = False
        track_model.green_line.dynamic_track.occupancies
        self.map_canvas.block_clicked_callback = self.block_selected_callback


    # TODO: IT4
    # When a block is selected from manual OR clicked on
    def toggle_track_circuit_failure(self, track_):
        """""
        Implement Logic:
        toggle on/off track circuit failure
        Display icon at appropriate block
        Alert backend to pause communication with wayside
        """
    # TODO: IT4
    # When a block is selected from manual OR clicked on
    def toggle_broken_rail_failure(self, track_):
        """""
        Implement Logic:
        toggle on/off broken rail failure
        Display icon at appropriate block
        """
    # TODO: IT4
    # When a block is selected from manual OR clicked on
    def toggle_power_failure(self, track_):
        """""
        Implement Logic:
        toggle on/off power failure
        Display icon at appropriate block
        """
    # TODO: IT4
    # When a block is selected from manual OR clicked on
    def reset_failures(self, track_):
        """""
        Implement Logic:
        Resets ALL failures
        """

    # TODO: IT4
    # WIP Uploading a Track Layout with Track Builder
    def upload_track_layout_data(self, file_path):
        self.red_line.parse_track_layout_data(file_path)
        self.green_line.parse_track_layout_data(file_path)
        print("Successfully loaded and parsed layout for Red and Green lines.")

    # TODO: IT4
    # Changing Temperature
    def change_temperature(self, new_temp):
        try:
            new_temp = float(new_temp)
            self.outside_temp = new_temp
            self.track_heater_status = new_temp <= 36
            print(f"Updated track temperature: {new_temp}°F, Heater {'On' if self.track_heater_status else 'Off'}")
        except ValueError:
            print("Invalid temperature input.")


# Example usage
if __name__ == "__main__":
    track_model = TrackModelFrontEnd()
    track_model.upload_track_layout_data("Track Layout & Vehicle Data vF5.xlsx")
    track_model.change_temperature(35)
