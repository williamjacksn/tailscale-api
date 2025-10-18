import json
import pathlib

ACTIONS_CHECKOUT = {"name": "Check out repository", "uses": "actions/checkout@v5"}
DEFAULT_BRANCH = "main"
THIS_FILE = pathlib.PurePosixPath(
    pathlib.Path(__file__).relative_to(pathlib.Path.cwd())
)


def gen(content: dict, target: str) -> None:
    pathlib.Path(target).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(target).write_text(
        json.dumps(content, indent=2, sort_keys=True), newline="\n"
    )


def gen_dependabot() -> None:
    target = ".github/dependabot.yaml"
    content = {
        "version": 2,
        "updates": [
            {
                "package-ecosystem": e,
                "allow": [{"dependency-type": "all"}],
                "directory": "/",
                "schedule": {"interval": "weekly"},
            }
            for e in ["github-actions", "uv"]
        ],
    }
    gen(content, target)


def gen_workflow_check_devices() -> None:
    target = ".github/workflows/check-devices.yaml"
    content = {
        "env": {
            "description": f"This workflow ({target}) was generated from {THIS_FILE}"
        },
        "name": "Check devices in the Tailscale network",
        "on": {"schedule": [{"cron": "0 0 * * *"}], "workflow_dispatch": {}},
        "jobs": {
            "check-devices": {
                "name": "Check devices in the Tailscale network",
                "runs-on": "ubuntu-latest",
                "environment": "tailscale-check-devices",
                "steps": [
                    ACTIONS_CHECKOUT,
                    {
                        "name": "Check devices",
                        "run": "sh ci/check-devices.sh",
                        "env": {
                            "SMTP_FROM": "${{ vars.smtp_from }}",
                            "SMTP_PASSWORD": "${{ secrets.smtp_password }}",
                            "SMTP_SERVER": "${{ vars.smtp_server }}",
                            "SMTP_TO": "${{ vars.smtp_to }}",
                            "SMTP_USERNAME": "${{ vars.smtp_username }}",
                            "TS_CLIENT_ID": "${{ vars.ts_client_id }}",
                            "TS_CLIENT_SECRET": "${{ secrets.ts_client_secret }}",
                        },
                    },
                ],
            }
        },
    }
    gen(content, target)


def gen_workflow_publish() -> None:
    target = ".github/workflows/publish.yaml"
    content = {
        "env": {
            "description": f"This workflow ({target}) was generated from {THIS_FILE}"
        },
        "name": "Publish to PyPI",
        "on": {"release": {"types": ["published"]}},
        "jobs": {
            "publish": {
                "name": "Publish to PyPI",
                "runs-on": "ubuntu-latest",
                "environment": {
                    "name": "pypi-release",
                    "url": "https://pypi.org/p/tailscale-api",
                },
                "permissions": {"id-token": "write"},
                "steps": [
                    ACTIONS_CHECKOUT,
                    {
                        "name": "Build and publish the package",
                        "run": "sh ci/build-and-publish.sh",
                    },
                ],
            }
        },
    }
    gen(content, target)


def gen_workflow_ruff() -> None:
    target = ".github/workflows/ruff.yaml"
    content = {
        "name": "Ruff",
        "on": {
            "pull_request": {"branches": [DEFAULT_BRANCH]},
            "push": {"branches": [DEFAULT_BRANCH]},
        },
        "permissions": {"contents": "read"},
        "env": {
            "description": f"This workflow ({target}) was generated from {THIS_FILE}"
        },
        "jobs": {
            "ruff-check": {
                "name": "Run ruff check",
                "runs-on": "ubuntu-latest",
                "steps": [
                    ACTIONS_CHECKOUT,
                    {"name": "Run ruff check", "run": "sh ci/ruff-check.sh"},
                ],
            },
            "ruff-format": {
                "name": "Run ruff format",
                "runs-on": "ubuntu-latest",
                "steps": [
                    ACTIONS_CHECKOUT,
                    {"name": "Run ruff format", "run": "sh ci/ruff-format.sh"},
                ],
            },
        },
    }
    gen(content, target)


def main() -> None:
    gen_dependabot()
    gen_workflow_check_devices()
    gen_workflow_publish()
    gen_workflow_ruff()


if __name__ == "__main__":
    main()
