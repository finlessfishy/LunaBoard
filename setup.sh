# setup.sh for setting up python dependencies and verifying files



#echo "Installing python dependencies..."



echo "Verifying files..."

FILE1="main.py"
FILE2="lunaboard.lua"
FILE3="pylibs/colors.py"
FILE4="pylibs/inputlib.py"
FILE5="pylibs/utilities.py"

if [ -f "$FILE1" ]; then
    echo "File $FILE1 exists."
else
    echo "Error: File $FILE1 does not exist."
fi

if [ -f "$FILE2" ]; then
    echo "File $FILE2 exists."
else
    echo "Error: File $FILE2 does not exist."
fi

if [ -f "$FILE3" ]; then
    echo "File $FILE3 exists."
else
    echo "Error: File $FILE3 does not exist."
fi

if [ -f "$FILE4" ]; then
    echo "File $FILE4 exists."
else
    echo "Error: File $FILE4 does not exist."
fi

if [ -f "$FILE5" ]; then
    echo "File $FILE5 exists."
else
    echo "Error: File $FILE5 does not exist."
fi



echo ""
read -p "Press enter to close." uinput