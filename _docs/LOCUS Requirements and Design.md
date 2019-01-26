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
that report progress as well as errors.

Below is a block diagram of the LOIS software.  LOCUS will replace LOIS.

<img src="https://github.com/LowellObservatory/Locus/blob/master/_images/LOIS.png" allign="middle" alt="test" width="500"/>

### Scope of this Document

This document will be an overview of the LOCUS system and include Requirements and Design
information.  LOCUS will consist of multiple pieces as listed below:

1. LoCam - Provide an interface to various cameras including ARC and, possibly, Starlight
and others. This application will use the ArcLib library to communicate with the ARC controllers.
There is also a possibility of using the "Instrument Neutral Distributed Interface" protocol here.
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

The diagram below outlines the structure of the overall system.

![diagram](https://github.com/LowellObservatory/Locus/blob/master/_images/LOCUS-Structure-011519.png "test")

### Use cases for LOCUS

* Science operation of DCT instruments. Initially this includes LMI, DeVeny, and NIHTS.
* GWAVES probe operations for guiding and wavefront sensing.
* Science observations with GWAVES probes such as stellar and lunar occultations
* Slit viewing camera operations for DeVeny and NIHTS and possibly the all-sky cameras.
  This is a future improvement that should be considered near term. 
  
### Software and System Requirements

Greater detail on these requirements will be detailed in the individual Requirements and Design
documents for the individual modules listed above.

* The software will run under 64-bit linux, in general, but some may operate under the MacOS (e.g. spectrograph slit viewing camera control software).
* The software will be written in Python, the current best choice in terms of flexibility and portability.
* The software will be object oriented and classes will conform the the “single responsibility” principle documented in Robert C. Martin’s “Clean Code”.
* The software will be well documented both externally and within the code. It will be developed following the "waterfall" approach to software design beginning with requirements development, internal design at several levels, code development and testing, with design and code reviews as appropriate. Late changes to requirements and design features will be carefully reviewed before being implemented.
* A programmer's guide and a user’s guide will be developed along with the software.
* The software will include internal unit test modules when possible, which will provide a detailed testing suite when the project is done.
* APIs will be provided to allow libraries to be easily used in future software development.
* The software will be designed with extensibility and modifiability in mind. Particular attention will be given to the ActiveMQ interface area.
* Configuration control of the software and its associated documents will be implemented using github. This includes controller DSP code.
* External software libraries and modules used in development will be evalutated for their breadth of application
and, when possible, we will only use libraries for which the source code is available.
* Various standards for communication will be evaluated and used when their application is appropriate.
These may include:
  * XML (Extensible Markup Language)
  * INDI ([Instrument Neutral Distributed Interface](http://www.clearskyinstitute.com/INDI/INDI.pdf))
  * FITS (Flexible Image Transport System)

### Interface Requirements

* Communication protocols via the ActiveMQ broker must follow the present protocols between LOIS and the software packages it communicates with. (for now).
* The system will operate with detector controllers made by Astronomical Research Cameras (ARC; aka "Leach" controllers). This support must be designed with an eye toward extending support to other camera types such as commercial cameras with USB or network interfaces with software APIs, or STA Archon controllers.
* The system will respond to commands sent from various other software systems and will retrieve information needed for its operation from other subsystems via the ActiveMQ broker. The systems it will interact with include:
  * The LOUI user interface software
  * The joe mechanism control software
  * The various DCT telescope LabView systems such as TCS, AOS, DCS, WRS via the ActiveMQ Bridge.
  * The external NAS for working data and the DCT archival RAID system. Interaction with these systems will not use ActiveMQ but will use standard operating system features such as NFS mounts, scp, etc.
* The system will communicate instrument and image telemetry to the broker for consumption by other processes

The diagram below outlines a possible LoCam to CCD interface using the Instrument Neutral Distributed Interface protocol.

![diagram](https://github.com/LowellObservatory/Locus/blob/master/_images/LOCUS-INDI-Server.png "test")

* The system will write FITS images to disk. Documentation in the form of an observing log will be generated and stored to allow users to find specific data.
* Data will be stored locally, to a working copy on an external NAS that observers may manipulate, and in original form to the DCT data archive RAID system.
* The various parts of the system will display an optional console that can show progress and errors in real time.
* The system will include certain specialized engineering interfaces that are not generally available to observers. This would include, but not be limited to, a scriptable command-line console or control GUI for test and engineering purposes.

### General Functional Requirements

* The system will allow the user to initialize the instrument systems, set up observing parameters, and take/store images.
* The system must include limit checking and error handling for supplied parameters.
* The system will allow for certain automated sequences and repetitive observations to be configured and implemented by a                  scripting approach. Examples include guiding, focusing, dither patterns, and filter sequences.  The scripting language will be      Python and the system will expose a Python API for system control that will not allow dangerous operations.
* This software should be built in a way that allows multiple instruments to be controlled by a single control package in the future.

### Specific Functional Requirements

* These will be detailed in the requirements documents for LoCam, LoFits, LoFocus, and LoGuide

### Logging Requirements

* This information will be specified in more detail in the subsystem requirements.  All parts of the system will
generate log files of commands issued and responses/results of those commands.  Log levels will be used to allow
easy sorting of events.  Log files will need to be managed/rotated to avoid overly large log files.

### Ancillary Data Requirements:

* The software will subscribe to and monitor various facility data (to be specified)
* Some instrument and image telemetry will be supplied to the broker including:
  * Detector, cold tip, heat sink temperatures, cooler power, and heater currents.
  * Instrument status = Software running (heartbeat) = Integrating = Idle = Error (Need to define this). A failed DSP upload would be an example.
  
### Scripting

* Python will be used as a scripting language
* The system will provide at least one API for use in building scripts.  There may be two versions, one for expert users.
* Some of the uses for scripts are:
  * Guiding
  * Wavefront sensing data acquisition
  * Focusing
  * Dither patterns, ABBA dithers, etc.
  * Filter sequences
  * WOLM data acquisition?
  
### Possible Future Improvements

* Slit viewing camera control for spectrographs; DeVeny and NIHTS to begin with.
* Future support for other controllers such as the STA Archon devices.
* Guiding using the spectrograph slit viewing cameras.
* For ARC controllers support abort, stop, pause/resume, and on-the-fly exposure time change.
* Support Fowler sampling for IR arrays with ARC controllers.
* Support sampling up the ramp for IR arrays with ARC controllers.
