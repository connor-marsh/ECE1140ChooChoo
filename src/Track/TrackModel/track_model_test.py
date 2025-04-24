import sys
import os

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, QTime, QDateTime, QObject
os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

# Global inits
import globals.global_clock as global_clock
import globals.track_data_class as track_data
import globals.signals as signals

# Actual backend
from Track.TrackModel.track_model_backend import TrackModel
from Track.TrackModel.track_model_enums import Occupancy

# Other components (not needed for test)
from Train.train_collection import TrainCollection
from CTC.centralized_traffic_controller_backend import CtcBackEnd
from CTC.centralized_traffic_controller_frontend import CtcFrontEnd
from Track.TrackModel.track_model_frontend import TrackModelFrontEnd

# Set this to "UnitTest" to run our train init test
running_module = "UnitTest"

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Required global state
    global_clock.init()
    track_data.init()  # This is the actual real data you want
    signals.init()

    if running_module == "UnitTest":
        import unittest

        class TestTrackModelTrainInitialization(unittest.TestCase):
            def setUp(self):
                self.track_model = TrackModel(name="Green", wayside_integrated=False)

            def test_initialize_train_and_occupancy(self):
                self.track_model.initialize_train()

                train = self.track_model.trains[0]
                block_id = train.current_block.id
                occupancy = self.track_model.dynamic_track.occupancies[block_id]

                print(f"Train successfully initialized on block {block_id}")
                print(f"Block {block_id} occupancy: {occupancy.name}")

                self.assertEqual(occupancy, Occupancy.OCCUPIED)

        unittest.main(argv=[sys.argv[0]], verbosity=2)

    elif running_module == "TrackModel":
        track_model = TrackModelFrontEnd(wayside_integrated=False)
        track_model.show()

    elif running_module == "CTC":
        ctc_backend = CtcBackEnd()
        ctc_frontend = CtcFrontEnd(ctc_backend)
        ctc_frontend.show()

    sys.exit(app.exec_())
