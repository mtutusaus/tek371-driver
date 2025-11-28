from tek371 import Tek371

# Replace with your actual GPIB resource string
RESOURCE = "GPIB0::10::INSTR"

def main():
    # Connect to instrument
    tek = Tek371(RESOURCE)
    print("Connected to Tek371")

    # Query ID string
    print("Instrument ID:", tek.id_string())

    # Initialize instrument
    tek.initialize()
    print("Instrument initialized")

    # Set and get collector supply
    tek.set_collector_supply(50.0)
    print("Collector Supply set to 50%")
    print("Collector Supply status:", tek.get_collector_supply())

    # Set measurement mode
    tek.set_measurement_mode("SWE")
    print("Measurement mode set to SWEEP")
    print("Current measurement mode:", tek.get_measurement_mode())

    # Close connection
    tek.close()
    print("Connection closed")

if __name__ == "__main__":
    main()
