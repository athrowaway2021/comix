# comix

A Python tool to download and remove DRM from comics and manga from Amazon Kindle for backing up

## Update (01/2024)

The tool now works to seamlessly acquire highest-quality (i.e. x3056 for most comics) titles from Kindle, both for old ComiXology and post-merge titles.

Since HD titles on Kindle are tiled, it's impossible to acquire the original JPEG images, and the outputs are saved as PNG to retain quality at the cost of file size.

The tool is very work-in-progress and not all kinds of titles have been tested, and there are some TODO's left in the code, such as processing metadata, parallesing downloading and extraction, and adding a feature to list user's availabe books (the required API URL is in the relevant TODO). Feel free to leave feedback and issues, or make pull requests with improvements.

I will close issues relating to the old ComiXology tool and move the tool itself to a seperate branch for legacy reasons.

## Disclaimer

This tool is meant to be used only for creating offline, personal, backups of content that you have bought and own. We do not endorse piracy and sharing content downloaded using this tool. The full responsibility of using this tool correctly and not misuing it lies with the user(s).

This tool does not use any proprietary code, only accesses the platform's publicly-accessible release APIs, and the credentials required to access the API is supplied by the user(s). The API definitions used by the platform were reverse-engineered and "guessed" by us.

## Description

This tool can be used to download DRM-free copies of comics & manga from the Amazon Kindle platform, including both bought items and those covered by subscriptions. The content is downloaded at the highest quality available, which is usually what can be found on the mobile versions of the platform, unlike the SD content found in the browser version. This tool requires you to input your email and password, which will not be stored, and the ASIN of the content you wish to download, which can be found in the url of the item's store page or reader page.

## Installation

0. Make sure that you have Python 3 installed before installing this tool
1. Clone the tool using `git clone https://github.com/athrowaway2021/comix` or download the source code as a zip and unpack it in any location.
2. Install libraries required by the tool using `pip install -r requirements.txt`

## Usage

The login process is entirely automated and all you need to do is to input your email and password when the program prompts for them. The authentication tokens/cookies are then stored locally and reused in further runs, whilst passwords are never stored or cached. If you have MFA enabled, the program may also request a OTP code from a text or your authenticator app.

You can then use the tool by running `unkindle.py` and supplying the item ASIN as an argument. The downloaded content will be saved to the output folder. Be aware that the authentication will expire after some time so you may have to reinput your credentials every now and then, and 2FA may also be required sometimes, which can be resolved by simply logging out and logging back in on the Amazon site on the same machine.

```
> python unkindle.py B0CLL8484H
  Authenticating . . .
  Enter your Amazon credentials . . .
  Email: athrowaway2021@pm.me
  Password:
  Authenticated!
  Download size: 155MB
  Extracting . . .
  B0CLL8484H : Ultimate Spider-Man (2024-) 001
> magick identify -ping -format "%wx%h" "output/Ultimate Spider-Man (2024-) 001/Ultimate Spider-Man (2024-) 001 - p003.png"
  1988x3056
```
Additional arguments include:
  - -o/--output : custom output folder
  - --jpeg : output as jpeg
  - --keep_temp : keep temp folder, can be imported in calibre (device_id(dsn) from state.json must be imported in DeDRM plugin)


## Third-Party
This program uses the Python standard library and the following:
  - [KFX Input/kfxlib](https://www.mobileread.com/forums/showthread.php?t=291290)
