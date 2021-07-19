<!-- ABOUT THE PROJECT -->
# Auto-lingo
A <a href="https://www.duolingo.com/" target="_blank">Duolingo</a> Bot for automatic XP earning.

Auto-lingo works in both the [Learn mode](#learn-mode) and the [Stories mode](#stories-mode).

Built with [Python](https://www.python.org/) and [Selenium](https://www.selenium.dev/).

## Modes
   
### Learn mode
Completes every available skill until it is fully leveled up.
<br>

![learn](https://user-images.githubusercontent.com/65187002/126021764-1e29e0fd-54a4-4041-91ce-ea0e6e68c09e.gif)
 
### Stories mode
Completes every available story as long as it gives XP.
<br>

![stories](https://user-images.githubusercontent.com/65187002/126019082-07b89071-cce6-4a92-a826-d539d9f09ca1.gif)

<!-- GETTING STARTED -->
## Getting Started

<!-- To get a local copy up and running follow these simple steps. -->

### Prerequisites
You will need [Python](https://www.python.org/), [Selenium](https://www.selenium.dev/), [Chrome](https://www.google.com/intl/en_en/chrome/) and [Chromedriver](https://chromedriver.chromium.org/downloads) installed.

### Installing Selenium
   ```sh
   $ pip install selenium
   ```
   
### Installing Chromedriver
1. Check your version of [Chrome](https://www.google.com/intl/en_en/chrome/) by going [here](https://www.google.com/chrome/update/) and following the 3 steps in "How to check your version of Chrome".
2. Go [here](https://chromedriver.chromium.org/downloads) and download the right version of chromedriver.
3. Place the downloaded chromedriver executable in default path given in [settings.json](https://github.com/drknzz/auto-lingo/blob/main/settings.json) under "chromedriver_path" <br>OR<br>change the path in [settings.json](https://github.com/drknzz/auto-lingo/blob/main/settings.json) to point to the chromedriver executable.

### Installation

1. Download the ZIP file or clone the repository

   ```sh
   $ git clone https://github.com/drknzz/auto-lingo.git
   ```
2. Make sure the path to chromedriver executable is correctly set in [settings.json](https://github.com/drknzz/auto-lingo/blob/main/settings.json)
   ```sh
   "chromedriver_path": "C:\\Program Files (x86)\\chromedriver.exe"
   ```
3. (Optional) Save both your login / mail and password to Duolingo in [credentials.json](https://github.com/drknzz/auto-lingo/blob/main/credentials.json)
   ```sh
   "login": "example@mail.com",
   "password": "example"
   ```

<!-- USAGE EXAMPLES -->
## Usage
   ```sh
   $ python auto-lingo.py
   ```
### Additional flags:
   * ``-s`` or ``--stories`` &emsp; - [Stories mode](#stories-mode)
   * ``-l`` or ``--learn`` &emsp;&emsp; - [Learn mode](#learn-mode)
   * ``-i`` or ``--incognito`` &thinsp; - Start browser in incognito mode
   * ``-m`` or ``--mute`` &emsp;&emsp;&thinsp;&thinsp;&thinsp; - Start browser with muted audio
   * ``-a`` or ``--autologin`` &thinsp; - Automatically login using [credentials.json](https://github.com/drknzz/auto-lingo/blob/main/credentials.json)
   
## Settings
Settings are located in [settings.json](https://github.com/drknzz/auto-lingo/blob/main/settings.json) file.

* `chromedriver_path` &emsp; - Path to chromedriver executable
* `antifarm_sleep` &emsp;&emsp;&thinsp;&thinsp; - Sleep time inbetween completing stories / skills
* `maximize_window` &emsp;&emsp; - Start browser in full screen
* `headless` &emsp;&emsp;&emsp;&emsp;&thinsp;&thinsp;&thinsp;&thinsp;&thinsp;&thinsp; - No browser gui required
* `incognito` &emsp;&emsp;&emsp;&emsp;&thinsp;&thinsp;&thinsp;&thinsp; - Start browser in incognito mode
* `auto_login` &emsp;&emsp;&emsp;&emsp;&thinsp;&thinsp; - Automatically login to Duolingo using data in [credentials.json](https://github.com/drknzz/auto-lingo/blob/main/credentials.json)
* `mute_audio` &emsp;&emsp;&emsp;&emsp;&thinsp;&thinsp; - Start browser with muted audio

## Acknowledgments
Huge thanks to [Kubvv](https://github.com/Kubvv) for countless tests which led to bug and corner case finds.

<!-- LICENSE -->
## License

[Auto-lingo](#auto-lingo) is distributed under the [MIT License](https://github.com/drknzz/auto-lingo/blob/main/LICENSE).
