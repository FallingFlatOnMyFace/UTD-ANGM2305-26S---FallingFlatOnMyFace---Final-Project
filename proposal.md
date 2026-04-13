# Procedural Map Generator

## Repository
<https://github.com/FallingFlatOnMyFace/UTD-ANGM2305-26S---FallingFlatOnMyFace---Final-Project>

## Description
This program will be a procedural map generator that is able to randomly generate simple grid based maps based on user input. This is primarily to be used for writers, game developers, worldbuilders, and others who may need a source of inspiration or a way to quickly create a map.

## Features
Scalable parameters
    Users will be able to input how big they want their map to be in grid squares, allowing them to change it to their needs.

Multiple types of tiles
    The program will be able to generate flat land, oceans, mountains, and possibly other types of terrain based off of the code and user input.

Heightmap based generation
    The program will generate the terrain based off of a random heightmap, or one can be inserted by a user to be generated with.

Intuitive UI
    The program will be run on a separate application rather than within the terminal, allowing fields to be filled out and a screen to display the final result.

## Challenges
    1. Heightmap Insertion
        Generation using a heightmap will require a user to have one of their own and would require specific code to be run in order to detect the varying levels of blacks, whites, and greys that make up heightmaps.

    2. User Interface / Separate Application
        The program's application will require functioning input and output fields, buttons, and the ability to detect user mouseclicks and keyboard pressing. 

    3. Tile allocation and randomizing
        The program will need to randomize tiles in a relatively coherent way, possibly generating its own heightmaps and ensuring certain terrain tiles are clustered together to form genuine oceans, forests, etc.

## Outcomes

Ideal Outcome:
    A fully working application with its own UI that can generate a fictional map based off of user inputs, file uploads that are in black and white, and at complete random, with custom tiles, biome clustering, and some realism, in color.

Minimal Viable Outcome:
    The program can be run from the terminal with simple user inputs, taking a file uploaded to the application's folder to detect generation maps (only one at a time, however), and then open a window to display the final result.
    

## Milestones

Week 1:
    Goal 1: Set up initial randomizer code
    Goal 2: Set up library for images to be pulled by the program
    Goal 3: Prototype UI and bugfixing

Week 2:
    Goal 1: Finalize randomizer code and ensure it works with a grid based input system
    Goal 2: Take images and cluster them together at certain intervals to ensure the grids stay together and do not appear as random clusters everywhere.
    Goal 3: Second pass of the UI, ensure that the program can display the result to the application and take user inputs.

Week 3:
    Goal 1: Finalize code and repair any and all bugs, make sure it can access the library properly
    Goal 2: Implement file uploading directly from the application if possible, otherwise pull images from a folder through manual uploading
    Goal 3: Complete UI and polish final product.