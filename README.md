# MicroPythonScripts

Main repository of MicroPython projects and modules I have built on my spare time.

## Structure of the repository

- **`projects/<project_name>`**

  Folder containing everything related to the script.

  | Name      | Type          | Description                                                                                                 |
  | --------- | ------------- | ----------------------------------------------------------------------------------------------------------- |
  | `code`    | :file_folder: | Commented code for better understanding of it.                                                              |
  | `release` | :file_folder: | Code without comments and trying to be as small as possible in order to save memory on the microcontroller. |
  | `docs`    | :file_folder: | Files like images and so on for documentation purposes.                                                     |

- **`modules`**

  Folder containing everything related to MicroPython and some help classes and scripts to make deployments more easy.

  | Name       | Type          | Description                                                                                                 |
  | ---------- | ------------- | ----------------------------------------------------------------------------------------------------------- |
  | `code`     | :file_folder: | Commented code for better understanding of it.                                                              |
  | `release`  | :file_folder: | Code without comments and trying to be as small as possible in order to save memory on the microcontroller. |
  | `docs`     | :file_folder: | Files like images and so on for documentation purposes.                                                     |
  | `examples` | :file_folder: | Example files that in some cases will need to be renamed into `main.py` so it will be run at boot time.     |

- **`snipets`** :file_folder:

  Scripts used to saved some common code so I don't forget how to do some things.

- **`static`** :file_folder:

  Contains images for documentation purposes and other static files like HTML and CSS code.

- **`tools`** :file_folder:

  Tools used when developing within this repo.

- **`README.md`** :page_with_curl: on :file_folder:

  Documentation of the script, class or other important information.

---

## Project list

| Project name    | Description                                                                                              | Status | Link                                        |
| :-------------- | :------------------------------------------------------------------------------------------------------- | :----- | ------------------------------------------- |
| Bulleting board | Online messages board with its own Access Point.                                                         | DONE   | [Get me there!](./projects/bulleting_board) |
| Camera slider   | Online camera slider controller.                                                                         | WIP    | [Get me there!](./projects/camera_slider)   |
| Micro server    | Serve static site from your board.                                                                       | DONE   | [Get me there!](./projects/micro_server)    |
| Pomodoro        | Implementation of the Pomodoro technique.                                                                | DONE   | [Get me there!](./projects/pomodoro)        |
| Problem solver  | Rubber duck debugging Technique with OLED LCD.                                                           | DONE   | [Get me there!](./projects/problem_solver)  |
| Script console  | Execute any python files on the filesystem.                                                              | DONE   | [Get me there!](./projects/script_console)  |
| Weather display | Use OpenWeatherMap API to retrieve forecast and current weather and also local data from a DHT11 sensor. | DONE   | [Get me there!](./projects/weather_display) |
| Weather station | Online server for DHT11 sensor readings.                                                                 | DONE   | [Get me there!](./projects/weather_station) |
| WiFi scanner    | Scans all available networks, it will show the strength, name and security                               | DONE   | [Get me there!](./projects/wifi_scan)       |

---

<!-- Support -->

## Support :mechanic:

Reach out to me at one of the following places!

- Website at [juanbiondi.com](https://www.juanbiondi.com)
- Create an [issue](https://github.com/yeyeto2788/Things-Organizer/issues/new/choose) on this repository. :pirate_flag:
- Send me an [email](mailto:jebp.freelance@gmail.com) :email:

---

<!-- Contributing -->

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/super_awesome_feature`)
3. Commit your Changes (`git commit -m 'Add some awesome feature'`)
4. Push to the Branch (`git push origin feature/super_awesome_feature`)
5. Open a Pull Request
