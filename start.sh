#!/bin/bash
set -e

echo "🚀 Starting Jitsi recorder"
python recorder.py
echo "✅ Recorder finished, container exiting"
