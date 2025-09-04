@echo off

echo Starting PostgreSQL test container...
docker-compose -f docker-compose.test.yml up -d

echo Waiting for PostgreSQL to be ready...
for /L %%i in (1,1,30) do (
    docker exec wort-wirbel-test-db pg_isready -U test_user -d test_wort_wirbel >nul 2>&1
    if !errorlevel! equ 0 (
        echo PostgreSQL is ready!
        goto :ready
    )
    echo Waiting... (%%i/30)
    timeout /t 1 /nobreak >nul
)

echo PostgreSQL failed to start within 30 seconds
exit /b 1

:ready
echo Test database is ready at localhost:5433
echo Connection string: postgresql://test_user:test_password@localhost:5433/test_wort_wirbel
