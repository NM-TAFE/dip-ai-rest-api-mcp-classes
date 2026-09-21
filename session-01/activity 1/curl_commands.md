# NASA API curl commands

Complete the Postman sections of the [activity](postman.md) first. These commands repeat the same requests directly against NASA's API; no local server is needed.

## Terminal setup

Check curl is available:

```bash
curl --version
```

**Windows PowerShell:** Use `curl.exe` in place of `curl` in every command, including the version check. This avoids the `curl` alias used by some PowerShell versions. The examples are on one line so no shell-specific line continuation is needed.

If curl is unavailable, ask your lecturer to help configure your terminal. Replace `DEMO_KEY` with your personal NASA key locally if needed; do not include it in submitted work.

## 1. Get the APOD for a specific date

```bash
# GET is the default method. Ask NASA for a JSON response.
curl --location "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&date=2024-01-01" --header "Accept: application/json"
```

Find `date`, `title`, and `media_type`. Compare them with Postman request 01. `--location` follows redirects if the server returns one.

## 2. Change a query parameter

```bash
# Change only the date, then compare the returned content.
curl --location "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&date=2024-01-02" --header "Accept: application/json"
```

## 3. Request a date range

```bash
# Replace date with start_date and end_date to request three entries.
curl --location "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&start_date=2024-01-01&end_date=2024-01-03" --header "Accept: application/json"
```

Count the objects in the returned array and compare with Postman request 03.

## 4. Inspect status codes and errors

```bash
# --include displays the HTTP status and response headers before the body.
curl --include --location "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&date=not-a-date" --header "Accept: application/json"
```

Record the HTTP status and error message. Correct the date to `2024-01-01` and rerun the command, keeping `--include`, to compare the successful response. HTTP errors can still print a response body; seeing output alone does not mean the request succeeded.

## 5. Save the JSON response

Run this in a folder where you can save exercise files. It creates or overwrites `nasa-apod.json` in the current directory.

```bash
# Save the response body to a file instead of printing it in the terminal.
curl --location "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&date=2024-01-01" --header "Accept: application/json" --output nasa-apod.json
```

Open `nasa-apod.json` in your editor. This saves the API response, not the image itself. Check that it contains the expected APOD fields rather than an error message.
