# MAP GENERATOR

## Demo
Demo Video:

## GitHub Repository
GitHub Repo: https://github.com/FallingFlatOnMyFace/UTD-ANGM2305-26S---FallingFlatOnMyFace---Final-Project

## Description
This program generates randomized maps in a pixel grid with oceans, beaches, variable terrain, and more. It supports black and white images (in the imagelibrary folder) and can be both gridded and ungridded for a seamless map. Here is a list of what the following programs do in the repository:

src (source folder)
    imagelibrary (required for heightmapping)
        heightmapExample.png (Example black and white image used for program - can be deleted / replaced)
        Readme.txt (Instructions on how to use imagelibrary)
    project.py (the program itself)
    requirements.txt (plugin requirements)
    readme.md (this file)

Considerations for design were to make a realistic style of generation. While I am pleased that the program works, it is not as intricate or detailed as I originally wanted it to be and could be improved upon in the future. I mostly concerned myself about the separation of landmasses and water and wanted water to dominate, perhaps this could be changed also in the future with the addition of sliders or additional input boxes to set how much water to land there should be.

It was also critical I got the heightmap function to work - however, only one file can be inside the imagelibrary folder at a time from my testing and it could break if there is more than one. Regardless it can detect the variations in black and white and translate them into a map.

Overall I am quite pleased with how the project turned out even if it required me to do significant rewrites and lots of gutting of the code in order to get it to work. I think it is still a little janky but if it works, it works. One of the biggest challenges for me was learning how the "os" (operating system) plugin worked, and it is still a little weird to me as I had to restructure my heirarchy for the heightmapping function to work in the first place.