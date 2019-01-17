## LOCUS Requirements and Design

### Introduction

There is a current need for a new software system that will control of the detectors used
in the instruments at the DCT, write complete FITS files on disk, and provide telescope
focusing and guiding capabilities. The old LOIS system is difficult to understand, poorly
documented, contains a lot of unused legacy code, nobody at Lowell knows its internals, and
it needs modification to work with more modern 64-bit operating systems. Our hardware is
aging and we need new software that can operate on new hardware to head off age-related
instrument failures.

The modules in the new software system will communicate among themselves and with other
DCT software systems using the ActiveMQ message broker. The primary external software systems
are the instrument control GUI (LOUI), the “Moving Parts” software (joe), and the various
aspects of the telescope control system via the ActiveMQ Bridge. The new software will be
broadly configurable using configuration files and will produce various levels of log files
that report progress as well as errors as specified below.

### Scope of this Document

This document will be an overview of the LOCUS system and include Requirements and Design
information.  LOCUS will consist of multiple pieces as listed below:

1. LoCam - Provide an interface to various cameras including ARC and, possibly, Starlight
and others.
2. LoFits - Provide an application that will create FITS files from science and
engineering data.  These files will include complete headers containing information
gathered from various parts of the DCT computer network.
3. LoFocus - Provide an application which gathers focus sweep data, locates the stellar
center for each image in the sweep, and returns the point of best focus for the secondary.
4. LoGuide - Provide an application that will take images at regular intervals, locate
the position of the star in each image and provide feedback to the telescope control system
to update telescope pointing.
5. possible others?

Each of these sub-elements will have its own Requirements and Design document.

![diagram](https://github.com/LowellObservatory/Locus/blob/master/_images/LOCUS-Structure-011519.png "test")
