# Activity 1: Exploring the NASA API with Postman and curl

**Time:** 45–60 minutes  
**Start here:** Complete the Postman tasks before moving to the [curl commands](curl_commands.md).

In this activity, you will request NASA's Astronomy Picture of the Day (APOD). You will send a request, inspect its response, change query parameters, and investigate an error. You will then repeat these requests in a terminal.

By the end, you should be able to identify an endpoint, send a GET request with an API key, read a JSON response, and explain how Postman and curl send the same HTTP request.

## Before you begin

- Open the Postman desktop app and have a terminal available (Laragon terminal, PowerShell, Terminal on macOS, or a Linux terminal).
- Use `DEMO_KEY` to get started. It is a shared, rate-limited demonstration key. For classroom use, obtain your own free key from [NASA's API portal](https://api.nasa.gov/) if the shared key reaches its limit.
- Keep personal API keys out of screenshots and committed files. The examples use only `DEMO_KEY`.

## Part 1: Send your first request in Postman

1. Create a collection called **Session 1 – NASA API**.
2. Add a request named **01 – APOD by date** and select **GET**.
3. Enter this URL:

   ```text
   https://api.nasa.gov/planetary/apod
   ```

4. In **Authorization**, select **No Auth**. For this exercise, the API key goes in the query string; there is no separate login request or bearer token.
5. In **Params**, add and enable these rows:

   | Key | Value |
   | --- | --- |
   | `api_key` | `DEMO_KEY` |
   | `date` | `2024-01-01` |

6. In **Headers**, add `Accept` with the value `application/json`.
7. Leave the request **Body** empty, save the request, and click **Send**.

The complete request URL should be:

```text
https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&date=2024-01-01
```

The `?` starts the query string and `&` separates parameters. `GET` retrieves data. The `Accept` header asks for JSON; a request body and `Content-Type` header are unnecessary here because you are not sending JSON data to NASA.

### Inspect the response

Look for a **200 OK** status, the response time, and the JSON response body. In the response headers, find `Content-Type`.

Record:

- The returned `date`, `title`, and `media_type`.
- One sentence summarising the `explanation`.
- The value of `url`. Open it in your browser and describe what it displays.

APOD entries can contain different types of media. Inspect `media_type` before assuming the URL points to an image, and do not assume every response includes `hdurl`.

## Part 2: Change the request in Postman

Duplicate and save the first request for each task so you can compare them later.

### A. Choose another day

Name the request **02 – Another date**. Change `date` to `2024-01-02` and send it. Which fields changed? Which stayed the same?

### B. Request three days

Name the request **03 – Date range**. Disable the `date` row and add:

| Key | Value |
| --- | --- |
| `start_date` | `2024-01-01` |
| `end_date` | `2024-01-03` |

Keep `api_key` enabled. Send the request and count the entries. Notice the outer square brackets (`[...]`): this response is an array of objects, rather than a single object (`{...}`). Do not combine `date` with a date range.

### C. Investigate an invalid date

Duplicate **01 – APOD by date** and name it **04 – Invalid date**. Change `date` to `not-a-date` and send it.

Record the actual HTTP status and error message. Explain what they tell you, then fix the date and send the request again. An invalid date should produce a client error; if you receive a key, rate-limit, or service error instead, address that first.

## Part 3: Move from Postman to curl

1. Open **01 – APOD by date** in Postman.
2. Open the **Code** panel (the `</>` icon) and select **cURL**.
3. Compare the generated command with example 1 in [curl_commands.md](curl_commands.md). Find the method, URL, parameters, and header in both.
4. Follow the terminal setup notes in that file and run examples 1–5 in order.
5. Compare the first curl response with the first Postman response. Formatting may differ, but the requested date and returned content should match.

| Postman | curl equivalent |
| --- | --- |
| GET method | Default method when no body is supplied |
| URL and Params | Quoted URL containing the query string |
| Headers | `--header` |
| Send button | Run the command in the terminal |
| Response status and headers | `--include` |
| Response body | Terminal output, or a file with `--output` |

## Check your understanding

Save brief answers and evidence of your work:

1. A screenshot of your successful Postman request and its response, with any personal key hidden.
2. The curl command for `2024-01-02`, using `DEMO_KEY`, and the title returned.
3. The difference between a single-date response and a date-range response.
4. The status and message from the invalid-date request, and how you fixed it.
5. Explain the purpose of `api_key`, `date`, and `Accept`. Which are query parameters and which is a header?
6. Why is GET appropriate for this activity?

**Optional challenge:** Request today's APOD by removing `date` in both Postman and curl. Compare the results.

## Troubleshooting and references

- **Key error:** Check that `api_key` is enabled and has a value.
- **429 / rate limit:** Pause requests or use your own NASA key. Repeated retries consume the shared allowance.
- **Connection or server error:** Check your internet connection and try again later if NASA is unavailable.
- **Command behaves unexpectedly:** Keep the whole URL in double quotes so the terminal does not interpret `&` as a command separator.

References: [NASA API portal](https://api.nasa.gov/), [NASA APOD API documentation](https://github.com/nasa/apod-api#docs), and [Postman code snippet documentation](https://learning.postman.com/docs/use/send-requests/create-requests/generate-code-snippets/).
