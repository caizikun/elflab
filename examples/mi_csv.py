""" The main script to run the measurements with a mutual inductance probe
"""

DEBUG_INFO = False

# Parameters to be set by the user for each measurement
# ____Measurement Parameters
MEASUREMENT_PERIOD = 0.001    # interval between single measurements, in s
THERMOMETER = ("elflab.devices.thermometers.fake_therms", "StepTherm")
                # (module, class) of the instrument
LOCKIN = (r"elflab.devices.lockins.fake_lockins", "SinCosLockin")
MAGNET = (r"elflab.devices.magnets.fake_magnets", "StepMagnet")

# ____Plot Parameters
NROWS = 2   # number of rows of sub plots
NCOLS = 1   # number of columns of sub plots
PLOT_REFRESH_PERIOD = 0.5     # Interval between plot refreshes
PLOT_LISTEN_PERIOD = 0.003    # Interval between listening events

XYVARS = [
            [("t", "X")],
            [("t", "Y")]
         ]      # Names of variable pairs to plot in each sub-plot
            

    
# Import other modules
import time
import importlib
from elflab import galileo, abstracts
from elflab.dataloggers import csvlogger
import mi_common as mi
from mi_nofile import SimMIMeasurer

    
# The main procedure
if __name__ == '__main__':
    
    timeString = time.strftime("%Y%m%d_%H.%M.%S")
    filename = r"D:\downloads\temp{}.csv".format(timeString)
    measurer = SimMIMeasurer()
    logger = csvlogger.Logger(filename, mi.indicesData, mi.dataLabels, mi.formatStrings)
    sim = abstracts.ML_Experiment("MI Simulator - csv logging", measurer, logger)
    gali = galileo.Galileo(experiment=sim, measurement_interval=MEASUREMENT_PERIOD, plotXYs=XYVARS)
    gali.start()