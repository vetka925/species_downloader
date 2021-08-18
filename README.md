![Logo of the project](https://raw.githubusercontent.com/vetka925/species_downloader/master/logo.png)

# species_downloader
> Download any number of photos for any species. 

Download photos of animals, birds, plants, insects you are looking for. 
This project uses iNaturalist API that provides an access to a really huge database 
of biological species observations containing photos. 
The main purpose of this project is to collect datasets 
for training Deep Learning models.

## Installing / Getting started

### Download species using shell and -s parameter

```shell
git clone https://github.com/vetka925/species_downloader.git
cd species_downloader
pip3 install -r requirements.txt
python3 -m species_downloader -s "Cygnus columbianus,Cygnus olor" -l 10 -sd "./downloads" -w 10
```

###Download species using shell and -f parameter

Firstly, you need a text file with species names separated with a new line '\n'.

#### *your_path/species.txt*
```shell
Cygnus columbianus
Cygnus olor
```

```shell
git clone https://github.com/vetka925/species_downloader.git
cd species_downloader
pip3 install -r requirements.txt
python3 -m species_downloader -f "test.txt" -l 10 -sd "./downloads" -w 10
```

It downloads 10 images for *Cygnus columbianus*  in ./downloads/Cygnus columbianus and 10 for *Cygnus olor* in  ./downloads/Cygnus olor.


### Download with SpeciesDownloader class
Example in [Jupyter Notebook](https://github.com/vetka925/species_downloader/blob/master/example.ipynb).

## Features
* Download photos of particular species.
* Download photos with any length list of species.
* You need to specify the only number of photos that you want. Photos with the best possible quality will be downloaded.
* Shell script or Python module usage.


## Links

- Repository: https://github.com/vetka925/species_downloader
- iNaturalist API: https://api.inaturalist.org/v1/docs/
