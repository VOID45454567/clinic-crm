#!/bin/bash

# Seed script runner for docker compose environment

set -e

echo "🌱 Running database seed..."

# Run seed inside docker container
docker compose exec server python -m app.seed

echo "✓ Seed completed!"
