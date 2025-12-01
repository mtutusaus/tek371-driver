
from tek371 import Tek371
import time

RESOURCE = "GPIB0::23::INSTR"
HORIZONTAL_SCALE = 200e-3
VERTICAL_SCALE = 5
VCE_PERCENTAGE = 100
DUT = "Diode"


def main():
    tek = Tek371(RESOURCE)
    print("Connected:", tek.id_string())

    # Initialize instrument
    tek.initialize()

    # Set peak power to 300W
    tek.set_peak_power(300)

    # Configure step generator (do not modify)
    tek.set_step_number(0)
    tek.enable_step_offset("OFF")
    tek.set_step_voltage(200e-3) # necessary?
    tek.set_step_offset(0) # necessary?

    # Enable SRQ handling
    tek.enable_srq_event()

    # Configure graticule
    tek.set_horizontal("COL", HORIZONTAL_SCALE)  # 200 mV/div
    tek.set_vertical(VERTICAL_SCALE)                # 5 A/div

    # Set STORE mode before sweep
    tek.set_display_mode("STO")

    for i in range(1, 2):
        # Set Collector Supply to desired %
        tek.set_collector_supply(VCE_PERCENTAGE)

        # Set measurement mode to sweep
        tek.set_measurement_mode("SWE")

        # Start the sweep
        print(f"Starting sweep number {i}...")
        if tek.wait_for_srq(timeout_s=60.0):
            print(f"Sweep {i} finished!")
        else:
            raise TimeoutError(f"Sweep {i} did not complete within timeout")

        # Read curve and save to CSV
        filename = f"I-V_{DUT}_{i}.csv"
        tek.read_curve(filename)

        # Reset SRQ for new sweep
        tek.discard_and_disable_all_events()
        tek.enable_srq_event()

    tek.disable_srq_event()
    tek.close()
    print("Done")


if __name__ == "__main__":
    main()
