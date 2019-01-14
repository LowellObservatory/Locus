* Over-arching questions

? Dyer - We can decide if some of these requirements should be moved into an internal design document.  I'm operating under the assumption that we have a single requirements document, then a high-level internal design of the ilk that we've already talked about but with more interface detail, internal designs of individual modules with lots of detail, and then we start coding.  Another approach would be to have a top-level requirements document, a top-level architecture document identifying the main parts, subsidiary requirements documents for those parts, and finally detailed design documents for each of the parts.  This is really just a different way of splitting up the requirements.

? Dyer - There's a slippery slope if we decide to expand the LOIS/LOUI communications for LOCUS/LOUI by modifying LOUI.  At what point do we stop modifying LOUI and start making something entirely new?  This will come up with extensions like abort/stop, pause, Fowler sampling, etc. These are desirable, but will impact the communication interface by adding new commands that will require LOUI modifications.

? Dyer - One more topic we need to discuss more broadly is the business of hardware triggering.  The DSP code we have supports it, but there would be some work involved in getting it to work with the Gen III controllers we use at the DCT.  There is also the matter of generating the trigger signal, but I think Mike Collins has already solved this problem in a way that would work well at the DCT.  This need input from Stephen, primarily because it involves timing for occultations.  It would also be the nuclear option for fixing exposure timing with LMI.


LOCUS Requirements draft						1/11/19

* Introduction

There is a current need for a new software system to allow control of the detectors used in the instruments at the DCT. The old LOIS system is difficult to understand, undocumented, contains a lot of unused legacy code, nobody at Lowell knows its internals, and it needs modification to work with more modern 64-bit operating systems.  Our hardware is aging and we need new software that can operate on new hardware to head off age-related instrument failures.

The modules in the new software system will communicate among themselves and with other DCT software systems using the ActiveMQ message broker.  The primary external software systems are the instrument control GUI (LOUI), the “Moving Parts” software (joe), and the various aspects of the telescope control system via the ActiveMQ Bridge.  The new software will be broadly configurable using configuration files and will produce various levels of log files that report progress as well as errors as specified below.

? Dyer - I think one of your patented diagrams would be very helpful to illustrate the overall system as it exists and which part we're replacing.  Do you agree?

In the longer term the intent is to replace joe and LOUI with analogous new software packages but those are distinct development projects and will have separate documentation packages and development activities.  This approach has the effect that the existing ActiveMQ interfaces between LOIS and LOUI, and LOIS and joe, will be preserved.  This may result in undesirable functional limitations.  To mitigate this risk special attention must be given to the ActiveMQ interface modules to make them as easy as possible to upgrade and replace later.

There is no intention of replacing the LabView components with new packages along the lines of the future replacements of LOUI and joe.

? Dyer - I have intentionally left out any mention of the LoThis and LoThat modules in this software package because I feel all that should go into the next document on a high-level internal design that is built in such a way as to meet these requirements.  So, no talk about ARClib, LoFocus, LoFITS, etc. in here.  Tom's go at the requirements includes sub-requirements on these modules but I think that's mixing up requirements and internal design.  But see the question at the beginning of this file.

* Use Cases

  - Science operation of DCT instruments.  Initially this includes LMI, DeVeny, and NIHTS.
  - GWAVES probe operations for guiding and wavefront sensing.
  - Science observations with GWAVES probes such as stellar and lunar occultations
  - Slit viewing camera operations for DeVeny and NIHTS.  This is a future improvement
    that should be considered near-term.
  ? Dyer - It's tempting to include the all-sky camera but I'm not sure we want to touch
    that nerve right now.

* System and Software Requirements

The new software developed to meet the requirements defined in this document will be subject to the following system and software requirements:

  - The software will run under 64-bit linux, in general, but some may operate under 
    the MacOS (e.g. spectrograph slit viewing camera control software).
  - The software will be written in Python, the current best choice in terms of 
    flexibility and portability.
  - The software will be object oriented and classes will conform the the “single
    responsibility” principle documented in Robert C. Martin’s “Clean Code”.
  - The software will be well documented both externally and within the code.  It will
    be developed following the "waterfall" approach to software design beginning with
    requirements development, internal design at several levels, code development and
    testing, with design and code reviews as appropriate.  Late changes to requirements
    and design features will be carefully reviewed before being implemented.
  - A programmer's guide and a user’s guide will be developed along with the software.
  - The software will include internal unit test modules when possible, which will
    provide a detailed testing suite when the project is done.
  - APIs will be provided to allow libraries to be easily used in future software 
    development.
  - The software will be designed with extensibility and modifiability in mind.
    Particular attention will be given to the ActiveMQ interface area.
  - Configuration control of the software and its associated documents will be 
    implemented using github.  This includes controller DSP code.

? Dyer - Do you think it would be good to limit the number of Python libraries used in this development?  I have the impression that there are many ways to do the same thing and the fewer we use the less likely it will be that changes in the underpinnings of the software will pull the rug out from under us.  This is your call.  This brings up the ugly issue of coping with changes in Python as time goes on.  It's a configuration management problem we have no control over. 

* Interface Requirements
  - Communication protocols via the ActiveMQ broker must follow the present protocols
    between LOIS and the software packages it communicates with.
  - The system will operate with detector controllers made by Astronomical Research
    Cameras (ARC; aka "Leach" controllers).  This support must be designed with an eye
    toward extending support to other camera types such as commercial cameras with 
    USB or network interfaces with software APIs, or STA Archon controllers.
  - The system will respond to commands sent from various other software systems and 
    will retrieve information needed for its operation from other subsystems via the
    ActiveMQ broker.  The systems it will interact with include:
    + The LOUI user interface software
    + The joe mechanism control software
    + The various DCT telescope LabView systems such as TCS, AOS, DCS, WRS via the 
      ActiveMQ Bridge.
    + The external NAS for working data and the DCT archival RAID system.  Interaction
      with these systems will not use ActiveMQ but will use standard operating system 
      features such as NFS mounts, scp, etc.
  - The system will communicate instrument and image telemetry to the broker for
    consumption by other processes
? Dyer - Another diagram here, or do you think the first one is sufficient?
 - The system will write FITS images to disk.  Documentation in the form of an
    observing log will be generated and stored to allow users to find specific data.
  - Data will be stored locally, to a working copy on an external NAS that observers
    may manipulate, and in original form to the DCT data archive RAID system.
  - The various parts of the system will display an optional console that can show 
    progress and errors in real time.
  - The system will include certain specialized engineering interfaces that are not 
    generally available to observers.  This would include, but not be limited to, a
    scriptable command-line console or control GUI for test and engineering purposes.

* General Functional Requirements

  - The software must only allow one control connection to the hardware and disallow
    other attempted connections with notification to avoid confusion.
  - The system will allow the user to initialize the instrument systems, set up observing
    parameters, and take/store images.
  - The system must include limit checking and error handling for supplied parameters.
  - The system will allow for certain automated sequences and repetitive observations to
    be configured and implemented by a scripting approach.  Examples include guiding, 
    focusing, dither patterns, and filter sequences.
  - Since NIHTS and LMI can be used simultaneously this software should be built in a
    way that allows both instruments to be controlled by a single control package in the
    future.
  - Remote operation of the system must be supported by some means.

* Specific Functional Requirements

  - Initialize detector controller or camera system
    + For ARC controllers this includes uploading the binhex DSP lod files for the PCI
      interface card, the timing board, and the utility board (if present).
    + Verify that the load is correct and post a fatal error if not.
    + Turn the power on and set the clock and bias voltages.
  - Set the operational properties of the device for single frame data:
    + amplifier configuration used to read out the image
      = only one amplifier allowed if more than one subframe
      = allowed amplifier configurations are hardware-specific
    + rectangular on-chip binning factor of the image
      = Limited to instrument-specific value, usually 4 or 5, in the serial direction
        for ARC controllers.
      = Binning is impossible with IR arrays.
    + prescan/overscan/overclock regions
    + exposure time
    + subframe sizes and locations if desired
      = Subframes must not overlap in the row direction for ARC systems
    + Define links between clocks and multiplexers for engineering purposes (setmux).
    + Support the synthetic image command (if present in the DSP) for engineering.
    + Support low-level memory read and write commands for engineering.
    + Read versioning information from ARC controller and PCI card
    + Read and write data from/to ARC controller memory and PCI card
    + Turn on the LED for the wavefront sensor to specific brightness levels.
  - Set additional parameters for time series data:
    + number of integrations to acquire
    + interval between images if this overrides the exposure time
  - Reject or ignore commands to set these operational properties:
      = gain
      = commands unsupported by the ARC controller DSP code for the instrument in use
  - Take data in the following subset of the existing readout modes in the HIPO-based
    DSP codes for ARC Gen II and Gen III controllers:
    + Single
    + Basic Occultation (frame transfer CCDs only)
    + Strips
  - Acquire image, bias, dark, and flat field data types.
  - For IR arrays acquire data in the following ways:
    + store reset and post-integration images
    + Store CDS images (i.e. post-integration minus reset image)
    + Support both pixel-at-a-time reset and global reset (if present in detector).
  - Record the start time of the exposure to < 10 ms [TBC] of the actual exposure start.
  - Report exposure and readout progress
  - Returned images will be reorganized (aka de-interlaced) to match the physical 
    structure of the image impinging on the detector.
    + Pre-scan, overscan, and overclocked regions will be located in the final image as
      per the HIPO DCS ICD.
  - File naming conventions and noon rule.  Needs to be fought out at a partners meeting.
  - Returned images will be FITS files with a header conforming to the FITS standard.
    + Updates to the FITS standard by either the NASA GSFC-led group or the IAU
      Working Group may be adopted as needed to support ongoing data compatibility 
      with modern tools.
  - FITS keywords shall be 8 characters or less
    + LOCUS shall not use the HIERARCH extension
      = FITS keywords requiring a keyline > 80 characters use the CONTINUE keyword
      = The contents of the FITS header shall conform to a FITS keyword dictionary 
        defined and maintained for each instrument.

* Logging Requirements

  - Keep a log file of commands issued and responses/results of those commands
  - Keep an independent log file of software functions
    + These log files will facilitate debugging and troubleshooting.
    + Utilize log levels to facilitate interpretation and sorting of events
    + Auto-rotate these log files periodically to prevent them from being overly large.

* Ancillary Data Requirements:

  - The software will subscribe and monitor the following facility data:
    + Need a list of what LOIS knows about
    + Add anything new that we wish we had.
  - Instrument and image telemetry sent to broker includes:
    + Detector, cold tip, heat sink temperatures, cooler power, and heater currents.
    + Additional temperatures for NIHTS
    + Instrument status
      = Software running (heartbeat)
      = Integrating
      = Idle
      = Error (Need to define this). A failed DSP upload would be an example.

* Scripting requirements: [This section is super important and poorly defined.]

  ? A scheme for scripting that is both convenient and safe for personnel and the 
    telescope needs to be defined fully so we don't have to invent it at coding time.
    We need to get Stephen and Tom in the loop on this because they both have strong
    and probably opposing points of view.
  - Scripted operations include
    + Guiding
    + Wavefront sensing data acquisition
    + Focusing
    + Dither patterns, ABBA dithers, etc.
    + Filter sequences
    + WOLM data acquisition?

* Future Improvements

  - Slit viewing camera control for spectrographs; DeVeny and NIHTS to begin with.
  - Future support for other controllers such as the STA Archon devices.
  - Guiding using the spectrograph slit viewing cameras.
  - For ARC controllers support abort, stop, pause/resume, and on-the-fly exposure time
    change.
  - Support Fowler sampling for IR arrays with ARC controllers.
  - Support sampling up the ramp for IR arrays with ARC controllers.

? Tom mentions visitor instruments.  I'm not sure what he means but LOCUS shouldn't run other people's instruments.  We have enough to worry about already!
