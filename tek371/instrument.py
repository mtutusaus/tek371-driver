import pyvisa
from pyvisa.constants import (
    VI_EVENT_SERVICE_REQ,
    EventMechanism,
    VI_ALL_ENABLED_EVENTS,
)
from . import commands as cmd
import time
import threading
import csv


class Tek371:
    """Driver class for Tektronix 371 Curve Tracer using PyVISA."""

    def __init__(self, resource: str, timeout_ms: int = 5000):
        self.rm = pyvisa.ResourceManager()
        self.inst = self.rm.open_resource(resource)
        self.inst.timeout = timeout_ms
        self.inst.write_termination = '\n'
        self.inst.read_termination = '\n'

        # --- SRQ state ---
        self._srq_called = False
        self._srq_lock = threading.Lock()
        self._srq_handler_installed = False

    # -----------------------
    # Low-level I/O
    # -----------------------
    def write(self, command: str) -> None:
        self.inst.write(command)

    def query(self, command: str) -> str:
        return self.inst.query(command)

    def read_raw(self) -> bytes:
        return self.inst.read_raw()

    def close(self) -> None:
        try:
            # Remove SRQ handler if installed
            if self._srq_handler_installed:
                try:
                    self.inst.disable_event(VI_EVENT_SERVICE_REQ, EventMechanism.all)
                except Exception:
                    pass
            self.inst.close()
        finally:
            self.rm.close()

        # -----------------------------
        # Connection & Utilities
        # -----------------------------

    def initialize(self) -> None:
        self.write(cmd.INI_SET)

    def id_string(self) -> str:
        return self.query(cmd.ID_QUERY)

    def get_help(self) -> str:
        return self.query(cmd.HEL_QUERY)

    def get_settings(self) -> str:
        return self.query(cmd.SET_QUERY)

    def perform_test(self) -> str:
        return self.query(cmd.TES_QUERY)

        # -----------------------------
        # Collector Supply
        # -----------------------------

    def set_collector_polarity(self, mode: str) -> None:
        self.write(cmd.CSP_SET.format(mode=mode))

    def get_collector_polarity(self) -> str:
        return self.query(cmd.CSP_QUERY)

    def set_peak_power(self, watts: int) -> None:
        self.write(cmd.PKP_SET.format(set=watts))

    def get_peak_power(self) -> str:
        return self.query(cmd.PKP_QUERY)

    def set_collector_supply(self, percent: float) -> None:
        self.write(cmd.VCS_SET.format(data=f"{percent:.1f}"))

    def get_collector_supply(self) -> str:
        return self.query(cmd.VCS_QUERY)

    def get_breaker_status(self) -> str:
        return self.query(cmd.CSO_QUERY)

        # -----------------------------
        # Display
        # -----------------------------

    def set_display_mode(self, mode: str) -> None:
        self.write(cmd.DIS_MODE_SET.format(mode=mode))

    def view_curve(self, index: int) -> None:
        self.write(cmd.DIS_VIEW_SET.format(index=index))

    def compare_curve(self, index: int) -> None:
        self.write(cmd.DIS_COMP_SET.format(index=index))

    def invert_display(self, status: str) -> None:
        self.write(cmd.DIS_INV_SET.format(status=status))

    def set_calibration(self, status: str) -> None:
        self.write(cmd.DIS_CAL_SET.format(status=status))

    def get_display_settings(self) -> str:
        return self.query(cmd.DIS_QUERY)

    def store_display(self, index: int) -> None:
        self.write(cmd.ENT_SET.format(index=index))

        # -----------------------------
        # Horizontal & Vertical
        # -----------------------------

    def set_horizontal(self, source: str, volt_div: float) -> None:
        self.write(cmd.HOR_SET.format(source=source, volt=f"{volt_div:.2E}"))

    def get_horizontal(self) -> str:
        return self.query(cmd.HOR_QUERY)

    def set_vertical(self, amp_div: float) -> None:
        self.write(cmd.VER_SET.format(amp=f"{amp_div:.2E}"))

    def get_vertical(self) -> str:
        return self.query(cmd.VER_QUERY)

        # -----------------------------
        # Step Generator
        # -----------------------------

    def enable_step_output(self, mode: str) -> None:
        self.write(cmd.STP_OUT_SET.format(mode=mode))

    def set_step_current(self, val: float) -> None:
        self.write(cmd.STP_CUR_SET.format(val=f"{val:.2E}"))

    def set_step_voltage(self, val: float) -> None:
        self.write(cmd.STP_VOL_SET.format(val=f"{val:.2E}"))

    def set_step_number(self, val: int) -> None:
        self.write(cmd.STP_NUM_SET.format(val=val))

    def invert_step(self, mode: str) -> None:
        self.write(cmd.STP_INV_SET.format(mode=mode))

    def set_step_multiplier(self, mode: str) -> None:
        self.write(cmd.STP_MUL_SET.format(mode=mode))

    def set_step_offset(self, val: float) -> None:
        self.write(cmd.STP_OFF_SET.format(val=f"{val:.2f}"))

    def get_step_settings(self) -> str:
        return self.query(cmd.STP_QUERY)

        # -----------------------------
        # Measurement
        # -----------------------------

    def set_measurement_mode(self, mode: str) -> None:
        self.write(cmd.MEA_SET.format(mode=mode))

    def get_measurement_mode(self) -> str:
        return self.query(cmd.MEA_QUERY)

        # -----------------------------
        # Cursor & CRT
        # -----------------------------

    def cursor_off(self) -> None:
        self.write(cmd.CURS_SET)

    def set_dot_cursor(self, pos: int) -> None:
        self.write(cmd.DOT_SET.format(data=pos))

    def get_dot_cursor(self) -> str:
        return self.query(cmd.DOT_QUERY)

    def set_line_cursor(self, hor: int, ver: int) -> None:
        self.write(cmd.LIN_SET.format(hor=hor, ver=ver))

    def get_line_cursor(self) -> str:
        return self.query(cmd.LIN_QUERY)

    def set_window_cursor(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self.write(cmd.WIN_SET.format(bott_l_hor=x1, bott_l_ver=y1, up_r_hor=x2, up_r_ver=y2))

    def get_window_cursor(self) -> str:
        return self.query(cmd.WIN_QUERY)

    def get_cursor_readout(self, fmt: str = "") -> str:
        return self.query(cmd.REA_QUERY.format(number_format=fmt).strip())

    def get_beta_gm(self) -> str:
        return self.query(cmd.BGM_QUERY)

        # -----------------------------
        # Text
        # -----------------------------

    def write_text(self, text: str) -> None:
        self.write(cmd.TEX_SET.format(string=f'"{text}"'))

    def read_text(self) -> str:
        return self.query(cmd.TEX_QUERY)

        # -----------------------------
        # Waveform & Curve
        # -----------------------------


    def read_curve(self, filename: str) -> None:
        """
        Reads the curve from the instrument, parses and scales points,
        and saves them to a CSV file.

        Args:
            filename (str): Path to the output CSV file.
        """
        # Read preamble and split into array
        preamble_array = self.read_preamble().split(",")

        # Extract values
        nr_pt = int(preamble_array[2].split(":")[1].strip())  # NR.PT
        xmult = float(preamble_array[4].split(":")[1].strip())  # XMULT
        ymult = float(preamble_array[8].split(":")[1].strip())  # YMULT
        xoff = int(preamble_array[6].split(":")[1].strip())  # XOFF
        yoff = int(preamble_array[10].split(":")[1].strip())  # YOFF

        # Calculate expected bytes
        curve_head_len = 25
        bytes_for_data_len = 2
        bytes_for_checksum = 1
        bytes_per_x = 2
        bytes_per_y = 2
        points_to_read = nr_pt * (bytes_per_x + bytes_per_y)
        expected_bytes = curve_head_len + bytes_for_data_len + points_to_read + bytes_for_checksum

        # Request curve and read exact number of bytes
        self.write(cmd.CUR_QUERY)
        raw_curve = self.inst.read_bytes(expected_bytes)

        # Parse and scale points
        start_idx = curve_head_len + bytes_for_data_len
        end_idx = len(raw_curve) - bytes_for_checksum
        points_bytes = raw_curve[start_idx:end_idx]

        points = []
        for i in range(0, len(points_bytes), 4):
            x_bytes = points_bytes[i:i + 2]
            y_bytes = points_bytes[i + 2:i + 4]
            if len(x_bytes) < 2 or len(y_bytes) < 2:
                break
            coord_x = int.from_bytes(x_bytes, byteorder="big", signed=False) - xoff
            coord_y = int.from_bytes(y_bytes, byteorder="big", signed=False) - yoff
            voltage = coord_x * xmult
            current = coord_y * ymult
            points.append((voltage, current))
            points.sort(key=lambda p: p[1])  # Ascending order by curren

        print(f"Number of points parsed: {len(points)} (expected {nr_pt})")

        # Save scaled points to CSV
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Voltage (V)", "Current (A)"])
            writer.writerows(points)

        print(f"Curve saved to {filename}")

    def read_preamble(self) -> str:
        return self.query(cmd.WFM_QUERY)

    def read_waveform(self) -> str:
        return self.query(cmd.WAV_QUERY)

    def set_waveform_length(self, points: int) -> None:
        self.write(cmd.WFM_LENGTH_SET.format(points=points))

    def get_waveform_length(self) -> str:
        return self.query(cmd.WFM_LENGTH_QUERY)

        # -----------------------------
        # Miscellaneous
        # -----------------------------

    def save_settings(self, index: int) -> None:
        self.write(cmd.SAV_SET.format(index=index))

    def recall_settings(self, index: int) -> None:
        self.write(cmd.REC_SET.format(index=index))

    def get_output_status(self) -> str:
        return self.query(cmd.OUT_QUERY)

    def print_curve(self, mode: str) -> None:
        self.write(cmd.PLO_SET.format(mode=mode))

    def get_printer_status(self) -> str:
        return self.query(cmd.PST_QUERY)

    def debug_mode(self, status: str) -> None:
        self.write(cmd.DEB_SET.format(status=status))

    def get_debug_status(self) -> str:
        return self.query(cmd.DEB_QUERY)

    def get_event_code(self) -> str:
        return self.query(cmd.EVE_QUERY)

    def set_opc(self, status: str) -> None:
        self.write(cmd.OPC_SET.format(status=status))

    def get_opc_status(self) -> str:
        return self.query(cmd.OPC_QUERY)

    def set_rqs(self, status: str) -> None:
        self.write(cmd.RQS_SET.format(status=status))

    def get_rqs_status(self) -> str:
        return self.query(cmd.RQS_QUERY)

    # =====================================================
    # SRQ HANDLING (new)
    # =====================================================
    def discard_and_disable_all_events(self) -> None:
        """
        Clear any pending VISA events and disable delivery.
        Useful before enabling SRQ to start clean.
        """
        try:
            self.inst.discard_events(VI_ALL_ENABLED_EVENTS, EventMechanism.all)
            self.inst.disable_event(VI_ALL_ENABLED_EVENTS, EventMechanism.all)
        except Exception:
            # Different VISA backends may behave slightly differently;
            # swallow harmless errors.
            pass

    def enable_srq_event(self) -> None:
        """
        Enable SRQ at instrument level (OPC & RQS) and at controller level (VISA events).
        Installs a handler that flips a flag when SRQ arrives.
        """
        # 1) Ask instrument to assert SRQ when operations complete
        #    (these map to your commands.py)
        self.write(cmd.OPC_SET.format(status="ON"))   # Operation Complete ON
        self.write(cmd.RQS_SET.format(status="ON"))   # Service Request ON

        # 2) Reset state and clean previous event configuration
        with self._srq_lock:
            self._srq_called = False
        self.discard_and_disable_all_events()

        # 3) Install handler and enable SRQ delivery in VISA
        def _srq_handler(resource, event, user_handle):
            # Flip the flag and optionally you can query EVENT code here if you need to distinguish causes.
            with self._srq_lock:
                self._srq_called = True

        wrapped = self.inst.wrap_handler(_srq_handler)
        self.inst.install_handler(VI_EVENT_SERVICE_REQ, wrapped, None)
        self.inst.enable_event(VI_EVENT_SERVICE_REQ, EventMechanism.handler, None)
        self._srq_handler_installed = True

    def wait_for_srq(self, poll_interval: float = 0.1, timeout_s: float = 30.0) -> bool:
        """
        Block until SRQ arrives (sweep complete), or timeout.

        Returns:
            True if SRQ received before timeout, False otherwise.
        """
        deadline = time.time() + timeout_s
        while time.time() < deadline:
            with self._srq_lock:
                if self._srq_called:
                    # reset for next operation
                    self._srq_called = False
                    return True
            time.sleep(poll_interval)

        # As a fallback, you can poll OPC? here if you want:
        # try:
        #     status = self.query(cmd.OPC_QUERY).strip().upper()
        #     if status in ("ON", "OPC ON", "OPC 1", "OPC"):
        #         return True
        # except Exception:
        #     pass
        return False

    def disable_srq_event(self) -> None:
        """Disable SRQ generation in the instrument and stop VISA SRQ delivery."""
        # instrument side
        try:
            self.write(cmd.RQS_SET.format(status="OFF"))
        except Exception:
            pass
        try:
            self.write(cmd.OPC_SET.format(status="OFF"))
        except Exception:
            pass

        # controller side
        try:
            self.inst.disable_event(VI_EVENT_SERVICE_REQ, EventMechanism.all)
        except Exception:
            pass
        self._srq_handler_installed = False
        with self._srq_lock:
            self._srq_called = False
