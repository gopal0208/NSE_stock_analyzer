@echo off
echo 🔧 Setting up Python virtual environment...

IF NOT EXIST "myenv" (
    echo Creating virtual environment...
    py -m venv myenv
) ELSE (
    echo Virtual environment already exists.
)

echo Activating environment...
call .\myenv\Scripts\activate

echo Installing required packages...
pip install --upgrade pip
pip install pandas matplotlib seaborn

echo Setup complete.
pause
