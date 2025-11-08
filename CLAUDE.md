# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a parking fee calculator for a Taiwan parking lot (Nangang housing project). The application calculates parking fees based on entry/exit times with different rates for weekdays and weekends.

## Architecture

The codebase consists of three main components:

1. **calculation.py** - Backend calculation logic (standalone Python)
2. **index.html** - Frontend web interface
3. **styles.css** - Frontend styling

**Important**: The frontend (index.html) expects a web server with a `/calculate` POST endpoint, but no server implementation currently exists. The calculation logic is standalone and needs to be integrated into a web framework (Flask or FastAPI recommended).

## Parking Fee Calculation Logic

The calculation uses time-based pricing with the following parameters:

**Weekdays (Monday-Friday)**:
- First 16 hours (32 intervals): 16 TWD per 30 minutes, capped at 130 TWD daily
- After 16 hours: 8 TWD per 30 minutes, no additional cap

**Weekends (Saturday-Sunday)**:
- All day: 8 TWD per 30 minutes, capped at 130 TWD daily

**Key Implementation Details**:
- Time is calculated in 30-minute intervals
- Partial intervals (< 30 min) count as one full interval
- Fees are calculated per calendar day (resets at midnight)
- Multi-day parking calculates each day separately and sums the total

## Running the Application

**Testing the calculation logic**:
```bash
python calculation.py
```

**To run the web application** (requires implementation):
1. Create a web server (Flask/FastAPI) that:
   - Serves index.html as the frontend
   - Implements POST `/calculate` endpoint
   - Parses `entry_time` and `exit_time` from form data
   - Calls `calculate_parking_fee()` function
   - Returns JSON response: `{"fee": <calculated_fee>}`

## Testing Calculation Logic

When testing or modifying the calculation logic, verify:
- Weekend detection (weekday() >= 5)
- 30-minute interval rounding (partial intervals round up)
- Daily limits apply correctly (130 TWD for both weekday first 16hrs and weekend)
- Multi-day parking splits correctly at midnight
- Rate transitions at 16-hour mark on weekdays

## File Structure

- `calculation.py` - Core parking fee calculation algorithm
- `index.html` - Web UI with datetime inputs and fee display
- `styles.css` - Responsive styling for the calculator interface
- `*.pdf` - Project documentation (Nangang housing parking lot specifications)
