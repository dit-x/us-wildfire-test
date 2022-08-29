# added this to prevent redownloading the dataset in my env

if ls -a | grep 188-million-us-wildfires.zip;
then 
    echo "file found"
    if unzip -o 188-million-us-wildfires.zip;
    then
        echo "success"
    else
        echo "downloading file all over again"
        echo unzip -o 188-million-us-wildfires.zip
    fi
else
    echo "downloading"
    kaggle datasets download -d rtatman/188-million-us-wildfires
    sleep 5
    echo "unzipping"
    echo unzip -o  188-million-us-wildfires.zip
fi
