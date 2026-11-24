#!/bin/bash

# API Testing Script for Clinic CRM
# Run this after docker compose up

set -e

API_URL="http://localhost:8000/api/v1"
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== Clinic CRM API Tests ===${NC}\n"

# 1. Health Check
echo -e "${YELLOW}1. Testing Health Check${NC}"
HEALTH=$(curl -s ${API_URL}/health)
echo "Response: $HEALTH"
if echo "$HEALTH" | grep -q '"status":"ok"'; then
    echo -e "${GREEN}✓ Health check passed${NC}\n"
else
    echo -e "${RED}✗ Health check failed${NC}\n"
    exit 1
fi

# 2. Create First User (Admin)
echo -e "${YELLOW}2. Creating Admin User${NC}"
CREATE_USER=$(curl -s -X POST ${API_URL}/users/ \
    -H "Content-Type: application/json" \
    -d '{
        "email": "admin@clinic.test",
        "password": "admin123",
        "role": "admin"
    }')
echo "Response: $CREATE_USER"
if echo "$CREATE_USER" | grep -q '"email":"admin@clinic.test"'; then
    echo -e "${GREEN}✓ Admin user created${NC}\n"
else
    echo -e "${YELLOW}⚠ User might already exist or error occurred${NC}\n"
fi

# 3. Login
echo -e "${YELLOW}3. Testing Login${NC}"
LOGIN=$(curl -s -X POST ${API_URL}/auth/login \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=admin@clinic.test&password=admin123")
echo "Response: $LOGIN"

ACCESS_TOKEN=$(echo $LOGIN | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
REFRESH_TOKEN=$(echo $LOGIN | grep -o '"refresh_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$ACCESS_TOKEN" ]; then
    echo -e "${RED}✗ Login failed - no access token${NC}\n"
    exit 1
fi
echo -e "${GREEN}✓ Login successful${NC}"
echo "Access Token: ${ACCESS_TOKEN:0:20}..."
echo -e "Refresh Token: ${REFRESH_TOKEN:0:20}...\n"

# 4. Get Current User (/me)
echo -e "${YELLOW}4. Testing /auth/me${NC}"
ME=$(curl -s ${API_URL}/auth/me \
    -H "Authorization: Bearer $ACCESS_TOKEN")
echo "Response: $ME"
if echo "$ME" | grep -q '"email":"admin@clinic.test"'; then
    echo -e "${GREEN}✓ /auth/me works${NC}\n"
else
    echo -e "${RED}✗ /auth/me failed${NC}\n"
    exit 1
fi

# 5. Refresh Token
echo -e "${YELLOW}5. Testing Token Refresh${NC}"
REFRESH=$(curl -s -X POST "${API_URL}/auth/refresh?refresh_token=$REFRESH_TOKEN")
echo "Response: $REFRESH"
NEW_ACCESS_TOKEN=$(echo $REFRESH | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
if [ -z "$NEW_ACCESS_TOKEN" ]; then
    echo -e "${RED}✗ Token refresh failed${NC}\n"
    exit 1
fi
echo -e "${GREEN}✓ Token refresh successful${NC}"
echo -e "New Access Token: ${NEW_ACCESS_TOKEN:0:20}...\n"

# 6. Create Second User (Doctor)
echo -e "${YELLOW}6. Creating Doctor User${NC}"
CREATE_DOCTOR=$(curl -s -X POST ${API_URL}/users/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -d '{
        "email": "doctor@clinic.test",
        "password": "doctor123",
        "role": "doctor"
    }')
echo "Response: $CREATE_DOCTOR"
DOCTOR_ID=$(echo $CREATE_DOCTOR | grep -o '"id":[0-9]*' | cut -d':' -f2)
if [ ! -z "$DOCTOR_ID" ]; then
    echo -e "${GREEN}✓ Doctor user created (ID: $DOCTOR_ID)${NC}\n"
else
    echo -e "${YELLOW}⚠ Doctor might already exist${NC}\n"
    # Try to get existing doctor ID
    DOCTOR_ID=2
fi

# 7. Update User (Admin only)
echo -e "${YELLOW}7. Testing User Update (Admin only)${NC}"
UPDATE=$(curl -s -X PATCH ${API_URL}/users/${DOCTOR_ID}/update \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -d '{
        "is_active": false
    }')
echo "Response: $UPDATE"
if echo "$UPDATE" | grep -q '"is_active":false'; then
    echo -e "${GREEN}✓ User update successful${NC}\n"
else
    echo -e "${RED}✗ User update failed${NC}\n"
fi

# 8. Test Unauthorized Access
echo -e "${YELLOW}8. Testing Unauthorized Access${NC}"
UNAUTH=$(curl -s ${API_URL}/auth/me \
    -H "Authorization: Bearer invalid_token")
echo "Response: $UNAUTH"
if echo "$UNAUTH" | grep -q "401\|Unauthorized\|Невалидный токен"; then
    echo -e "${GREEN}✓ Unauthorized access blocked correctly${NC}\n"
else
    echo -e "${RED}✗ Authorization check failed${NC}\n"
fi

# 9. Test Forbidden Access (Non-admin trying to update)
echo -e "${YELLOW}9. Testing Forbidden Access (Doctor can't update users)${NC}"
DOCTOR_LOGIN=$(curl -s -X POST ${API_URL}/auth/login \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=doctor@clinic.test&password=doctor123")
DOCTOR_TOKEN=$(echo $DOCTOR_LOGIN | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ ! -z "$DOCTOR_TOKEN" ]; then
    FORBIDDEN=$(curl -s -X PATCH ${API_URL}/users/1/update \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $DOCTOR_TOKEN" \
        -d '{"is_active": true}')
    echo "Response: $FORBIDDEN"
    if echo "$FORBIDDEN" | grep -q "403\|Forbidden\|Недостаточно прав"; then
        echo -e "${GREEN}✓ Role-based access control works${NC}\n"
    else
        echo -e "${RED}✗ RBAC check failed${NC}\n"
    fi
else
    echo -e "${YELLOW}⚠ Doctor login failed, skipping RBAC test${NC}\n"
fi

echo -e "${GREEN}=== All Tests Completed ===${NC}"
