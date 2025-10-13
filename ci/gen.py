import json
import pathlib

ACTIONS_CHECKOUT = {"name": "Check out repository", "uses": "actions/checkout@v5"}
THIS_FILE = pathlib.PurePosixPath(
    pathlib.Path(__file__).relative_to(pathlib.Path.cwd())
)


def gen(content: dict, target: str) -> None:
    pathlib.Path(target).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(target).write_text(
        json.dumps(content, indent=2, sort_keys=True), newline="\n"
    )


def gen_workflow_check_devices():
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


def main():
    gen_workflow_check_devices()
    gen_workflow_publish()


if __name__ == "__main__":
    main()
