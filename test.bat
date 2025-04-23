@echo off
REM ====== Step 1: Register Voter ======
echo [1] Registering voter...
curl -X POST http://localhost:5000/register ^
-H "Content-Type: application/json" ^
-d "{\"voterId\": \"voter123\"}"
echo.

REM ====== Step 2: Submit Vote ======
echo [2] Submitting vote...
curl -X POST http://localhost:5000/vote ^
-H "Content-Type: application/json" ^
-d "{\"voterId\": \"voter123\", \"vote\": \"CandidateA\"}"
echo.

REM ====== Step 3: Mine a Block ======
echo [3] Mining block...
curl http://localhost:5000/mine
echo.

REM ====== Step 4: View Blockchain ======
echo [4] Viewing blockchain...
curl http://localhost:5000/chain
echo.

REM ====== Step 5: Admin View Results ======
echo [5] Viewing vote results as admin...
curl http://localhost:5000/admin/results ^
-H "X-Admin-Key:00112233445566778899aabbccddeeff"
echo.

REM ====== Step 6: Register Another Node ======
echo [6] Registering node http://localhost:5001...
curl -X POST http://localhost:5000/nodes/register ^
-H "Content-Type: application/json" ^
-d "{\"nodes\": [\"http://localhost:5001\"]}"
echo.

REM ====== Step 7: Sync Chain (Consensus) ======
echo [7] Resolving chain consensus...
curl http://localhost:5000/nodes/resolve
echo.

echo Done!
pause
