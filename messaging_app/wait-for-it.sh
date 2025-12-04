#!/bin/bash
# wait-for-it.sh - A simple bash script to wait for a service to be ready
# Usage: wait-for-it.sh host:port [-s] [-t timeout] [-- command args]
# -s: only check if service is available
# -t: timeout in seconds (default 15)

set -e

host=""
port=""
timeout=15
strict=0
cmd=""

usage() {
  echo "Usage: $0 host:port [-s] [-t timeout] [-- command args]"
  echo "  -h, --help            Show this help message"
  echo "  -s, --strict          Only check if service is available, fail if not"
  echo "  -t, --timeout timeout Timeout in seconds (default 15)"
  echo "  -- command args       Command to run after service is available"
  exit 1
}

# Parse arguments
if [[ $# -eq 0 ]]; then
  usage
fi

host_port="$1"
shift

IFS=':' read -r host port <<< "$host_port"

if [[ -z "$host" ]] || [[ -z "$port" ]]; then
  echo "Error: Invalid host:port format"
  usage
fi

while [[ $# -gt 0 ]]; do
  case "$1" in
    -s|--strict)
      strict=1
      shift
      ;;
    -t|--timeout)
      timeout="$2"
      shift 2
      ;;
    -h|--help)
      usage
      ;;
    --)
      shift
      cmd="$@"
      break
      ;;
    *)
      cmd="$@"
      break
      ;;
  esac
done

end=$((SECONDS + timeout))

while [ $SECONDS -lt $end ]; do
  if nc -z "$host" "$port" 2>/dev/null; then
    echo "✓ $host:$port is available"
    if [[ -n "$cmd" ]]; then
      exec "$@"
    fi
    exit 0
  fi
  sleep 1
done

if [[ $strict -eq 1 ]]; then
  echo "✗ Timeout waiting for $host:$port"
  exit 1
else
  echo "⚠ Timeout waiting for $host:$port, continuing anyway"
  if [[ -n "$cmd" ]]; then
    exec "$@"
  fi
  exit 0
fi
