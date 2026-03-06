# coding=utf-8
from libopensesame.py3compat import *
from ._base_conditioner import BaseConditioner
import serial
import time
import threading
import platform


def is_raspberry_pi():
    try:
        machine = platform.machine().lower()
        return any(arch in machine for arch in ("arm", "aarch64"))
    except Exception:
        return False


if is_raspberry_pi():
    try:
        import RPi.GPIO as GPIO

        GPIO.setmode(GPIO.BOARD)
        print(f"Polulu Tic t825 sound control ready")
    except ImportError:
        print("Library RPi.GPIO not installed.")


PIN_RPY_SOUND_CTRL = 8


DEFAULT_PORT = "/dev/ttyConditioner"
BAUD_RATE = 9600

# Parameter for seed dispenser
DEFAULT_MOTOR_N_PULSES = 50


class PoluluTicT825(BaseConditioner):
    def __init__(self, **kwargs):

        super(PoluluTicT825, self).__init__(**kwargs)
        self._port = kwargs.get("port", DEFAULT_PORT)
        self.motor_n_pulses = kwargs.get("motor_n_pulses", DEFAULT_MOTOR_N_PULSES)
        self._serial = serial.Serial(
            self._port, BAUD_RATE, timeout=0.1, write_timeout=0.1
        )

    def _stop(self, seed_dispenser=False, sound_left=False, sound_right=False):
        self.deenergize()

    def reward(self):
        # Don't wait motor to continue
        self._reward_thread = threading.Thread(target=self._reward, daemon=True)
        self._reward_thread.start()

    def _reward(self):
        try:
            position = self.get_current_position()
            new_target = position - self.motor_n_pulses
        except Exception as e:
            print(f"Cannot read motor position: {e}")
            return
        try:
            self.energize()
            self.exit_safe_start()
            self.set_target_position(new_target)
            motor_pause = (
                self.motor_n_pulses * 0.004
            ) + 1  # 1 sec min, and 0.004s/step
            time.sleep(motor_pause)
        except Exception as e:
            print(f"Error in _reward thread : {e}")
        finally:
            self.deenergize()

    # Sends the "Exit safe start" command.
    def exit_safe_start(self):
        self.send_command(0x83)

    # Sets the target position.
    #
    # For more information about what this command does, see the
    # "Set target position" command in the "Command reference" section of the
    # Tic user's guide.
    def set_target_position(self, target):
        self.send_command(
            0xE0,
            ((target >> 7) & 1)
            | ((target >> 14) & 2)
            | ((target >> 21) & 4)
            | ((target >> 28) & 8),
            target >> 0 & 0x7F,
            target >> 8 & 0x7F,
            target >> 16 & 0x7F,
            target >> 24 & 0x7F,
        )

    # Gets the "Current position" variable from the Tic.
    def get_current_position(self):
        b = self.get_variables(0x22, 4)
        position = b[0] + (b[1] << 8) + (b[2] << 16) + (b[3] << 24)
        if position >= (1 << 31):
            position -= 1 << 32
        return position

    # Gets one or more variables from the Tic.
    def get_variables(self, offset, length):
        self.send_command(0xA1, offset, length)
        result = self._serial.read(length)
        if len(result) != length:
            raise RuntimeError(
                "Expected to read {} bytes, got {}.".format(length, len(result))
            )
        return bytearray(result)

    def energize(self):
        self.send_command(0x85)

    def deenergize(self):
        self.send_command(0x86)

    def send_command(self, cmd, *data_bytes):
        header = [cmd]
        #        if self.device_number == None:
        #          header = [cmd]  # Compact protocol
        #        else:
        #          header = [0xAA, device_number, cmd & 0x7F]  # Pololu protocol
        self._serial.write(bytes(header + list(data_bytes)))

    def sound_left(self):

        self.sound_both()

    def sound_right(self):

        self.sound_both()

    def sound_off(self):
        if is_raspberry_pi():
            GPIO.output(PIN_RPY_SOUND_CTRL, GPIO.HIGH)

    def sound_both(self):
        if is_raspberry_pi():
            GPIO.output(PIN_RPY_SOUND_CTRL, GPIO.LOW)
            # sleep a little, amp start
            # time.sleep(0.2)

    def close(self):

        if hasattr(self, "_reward_thread") and self._reward_thread.is_alive():
            print("Wait motor before continue (10s timeout)...")
            self._reward_thread.join(timeout=10)
            self.deenergize()

        self._serial.close()
