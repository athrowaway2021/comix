# comix
A Python tool to download and remove DRM from comics and manga from ComiXology for backing up

## Disclaimer

This tool is meant to be used only for creating offline, personal, backups of content that you have bought and own. We do not endorse piracy and sharing content downloaded using this tool. The full responsibility of using this tool correctly and not misuing it for misappropriate reasons lies with the user(s).

This tool has been solely written by us, only accesses the platform's publicly-accessible release API, and the token required to access the API is supplied by the user(s). The protocol buffer definitions used by the API were reverse-engineered and "guessed" by us.

## Description

This tool can be used to download DRM-free copies of comics & manga from the ComiXology platform, including both bought items and those covered by the subscription. The content is downloaded at the highest quality available, which is usually what can be found on the mobile versions of the platform, unlike the SD content found in the browser version. This tool requires a single cookie from your account to download content and an ID of the content you wish to download, which can be found in the url of the item's store page or reader page.

## Installation

0. Make sure that you have Python 3 installed before installing this tool
1. Clone the tool using `git clone https://github.com/athrowaway2021/comix` or download the source code as a zip and unpack it in any location.
2. Install libraries required by the tool using `pip install -r requirements.txt`

## Usage

~~First acquire your authentication token cookie (aToken) from the website (region irrelevant) via the Application tab in your browser's devtools (can usually be accessed using the F12 key). You must be logged in order to get the cookie.~~

~~An API update removed the ability to use the browser auth token for the methods used in this tool, so from now you must aquire the token from the mobile app. For this you are required to have an Android device or emulator at hand. I recommend either using Fiddler on PC as a proxy, or the HttpCanary app with the ComiXology app running in Parallel Space to inspect the its HTTPS traffic. There are many guides on how to do this, so please use Google if you have any problems.

~~This repository includes [a patched version of the app](https://github.com/athrowaway2021/comix/blob/main/comix_3.10.17_patched.apk) that allows HTTPS inspection, but if you would like to do it yourself due to trust, or lack thereof, you can simply download an APK for the app from any mirror of your choice and then patch it using [this tool.](https://github.com/shroudedcode/apk-mitm)~~

~~Once you are able to inspect the app's traffic, the auth token, labelled as "amz_access_token", will be present in the bodies of all POST requests to the "cmx-secure.comixology.com" API. Then copy the auth token's value into the `AUTH_TOKEN` field in the `config.py` file.~~

The login process is now automated and all you need to do to login is to enter your Amazon email and password in `config.py`.

You can then use the tool by running `comix.py` and supplying the item ID as an argument. The downloaded content will be saved to the output folder. Be aware that the cookie will expire after some time or if you log out of the session from which you got the cookie and you will have to reacquire it.

```
> python comix.py list
899890 : Haikyu - v41
797946 : Marginal Operation - v01
1720 : New Avengers (2004-2010) - 001
271718 : Attack on Titan Sampler
```

You can also list all of the item IDs for content you own by supplying `list` as an argument.

```
> python comix.py 797946
797946 : Marginal Operation - v01
Downloading page 206 . . .
Done! Content saved to C:\comix\comix_out\Marginal Operation - v01
```

## Third-Party
This program uses the Python standard library and the following:
  - [Protocol Buffers](https://github.com/protocolbuffers/protobuf)
  - [pyzipper](https://github.com/danifus/pyzipper)
  - [requests](https://github.com/psf/requests)

See `/licenses/` for the corresponding licenses, copyright notices, and permission notices.
