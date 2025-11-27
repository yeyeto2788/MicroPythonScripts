# This file is executed on every boot (including wake-boot from deepsleep)
import gc
gc.collect()

import asyncio
import pomodoro
loop = asyncio.get_event_loop()  
loop.create_task(pomodoro.main_logic())  # Create a task to run the main function
loop.run_forever()

