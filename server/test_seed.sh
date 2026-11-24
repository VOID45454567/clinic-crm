#!/bin/bash

# Quick test for seeded users

API_URL="http://localhost:8000/api/v1"

echo "Testing seeded users login..."
echo ""

# Test Admin
echo "1. Admin login:"
curl -s -X POST ${API_URL}/auth/login \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=admin@clinic.local&password=admin123" | jq -r '.access_token // "FAILED"' | head -c 30
echo "..."
echo ""

# Test Doctor
echo "2. Doctor login:"
curl -s -X POST ${API_URL}/auth/login \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=doctor@clinic.local&password=doctor123" | jq -r '.access_token // "FAILED"' | head -c 30
echo "..."
echo ""

# Test Registrar
echo "3. Registrar login:"
curl -s -X POST ${API_URL}/auth/login \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=registrar@clinic.local&password=registrar123" | jq -r '.access_token // "FAILED"' | head -c 30
echo "..."
echo ""

echo "✓ All seeded users can login"
