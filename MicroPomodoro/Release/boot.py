# This file is executed on every boot (including wake-boot from deepsleep)
import gc
gc.collect()

import pomodoro
pomodoro.main_logic()
