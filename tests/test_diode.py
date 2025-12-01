from tek371 import Tek371

tek371_gpib_address = "GPIB0::23::INSTR"
tek371_horizontal_scale = 200e-3
tek371_vertical_scale = 5
tek371_vce_percentage = 100
DUT = "Diode"
number_of_curves = 10


def main():
    tek = Tek371(tek371_gpib_address)
    print(f"Tracer connected at address {tek371_gpib_address.split('::')[1]}: {tek.id_string()}")

    # Initialize instrument
    tek.initialize()

    # Set peak power to 300W
    tek.set_peak_power(300)

    # Configure step generator (not needed for diodes)
    tek.set_step_number(0)
    tek.set_step_voltage(200e-3)
    tek.set_step_offset(0)

    # Enable SRQ handling
    tek.enable_srq_event()

    # Configure graticule
    tek.set_horizontal("COL", tek371_horizontal_scale)  # 200 mV/div
    tek.set_vertical(tek371_vertical_scale)  # 5 A/div

    # CRT settings
    print("\nCRT SETTINGS")
    print(f"  Horizontal scale set to: {tek.get_horizontal().split(':')[1]} V/DIV")
    print(f"  Vertical scale set to: {tek.get_vertical().split(':')[1]} A/DIV\n")

    # Set STORE mode before sweep
    tek.set_display_mode("STO")

    print("START OF MEASUREMENT")
    print("-" * 50)
    for i in range(1, number_of_curves+1):
        print(f"CURVE {i}/{number_of_curves}")
        # Set Collector Supply to desired %
        tek.set_collector_supply(tek371_vce_percentage)
        print(f"  Collector supply set to: {tek.get_collector_supply().split()[-1]} %")

        # Set measurement mode to sweep
        tek.set_measurement_mode("SWE")

        # Start the sweep
        print(f"  Starting sweep number {i}/{number_of_curves}...")
        if tek.wait_for_srq(timeout_s=60.0):
            print(f"  Sweep {i}/{number_of_curves} finished!")
        else:
            raise TimeoutError(f"  Sweep {i} did not complete within timeout")

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
