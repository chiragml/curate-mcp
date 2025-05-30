# Curate-MCP

Curate-MCP is an automation tool designed to help users curate and customize their resumes based on specific job descriptions (JD), with a focus on LinkedIn job postings. It leverages browser automation and scraping to extract job requirements and provides tools for tailoring resumes to better match targeted roles.

## Features

- **LinkedIn Job Scraping:** Automatically scrape job details from LinkedIn postings using Selenium and the `linkedin-scraper` library.
- **Resume Customization (Planned):** Tools to help customize resumes based on scraped job descriptions and Overleaf integration (coming soon).
- **Session Management:** Start and close browser sessions programmatically.
- **Configuration Management:** Securely load credentials and configuration from environment variables.
- **Extensible Tools:** Easily add new tools and prompts for resume validation and customization.

## Project Structure

```
curate-mcp/
│
├── main.py                  # Entry point for the application
├── pyproject.toml           # Project dependencies and metadata
├── .env                     # Environment variables (credentials)
├── app/
│   ├── server.py            # FastMCP server setup and tool registration
│   ├── scrape.py            # LinkedIn scraping logic
│   ├── drivers/
│   │   └── chrome.py        # Chrome WebDriver management
│   └── config/
│       ├── __init__.py      # Configuration loading/reset logic
│       ├── load.py          # Loads credentials from environment
│       └── schema.py        # Configuration schemas
└── README.md                # Project documentation
```

## Getting Started

### Prerequisites

- Python 3.13+
- Chrome browser installed


### Usage

Run the main application:

```sh
uv run mcp install ./app/server.py
```

This will start the FastMCP server and register available tools.

#### Example: Scraping a LinkedIn Job

Use the `scrape_job_posting_linkedIn` tool (registered with the server) to scrape job details by providing a LinkedIn job URL.

#### Closing a Browser Session

Use the `close_session` tool to safely close the automated browser.

## Configuration

Configuration is managed via environment variables and loaded at runtime. See `app/config/` for details.

## Development

- All scraping logic is in `app/scrape.py`.
- Chrome WebDriver management is in `app/drivers/chrome.py`.
- Server and tool registration is in `app/server.py`.

## Roadmap

- [ ] Implement Overleaf integration for automated resume customization.
- [ ] Add more resume validation and improvement prompts.
- [ ] Enhance error handling and logging.

## License

MIT License

---

*Curate your resume, land your dream job!*