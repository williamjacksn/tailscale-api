pip install uv
uv run examples/check-devices.py | tee output.txt

echo "## Tailscale Network Alerts" >> "$GITHUB_STEP_SUMMARY"
if [ -s output.txt ]; then
  cat output.txt >> "$GITHUB_STEP_SUMMARY"
else
  echo "No alerts found." >> "$GITHUB_STEP_SUMMARY"
fi
