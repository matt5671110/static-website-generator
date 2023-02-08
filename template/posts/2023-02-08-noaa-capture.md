---
title: Automatic Capture of NOAA Satellite Images
description: The National Oceanic and Atmospheric Administration (NOAA) owns and operates a number of satellites in orbit around earth. These satellites serve a number of different purposes, ranging from weather monitoring and prediction to helping search and rescue teams locate distress signals from emergency beacons. A group of these satellites known as Polar Operational Environmental Satellites (POES) remain in a low polar orbit — that is, their orbit goes north-south over the poles. This allows the satellites to get a complete view of earth every day as earth rotates underneath them.
tags: bash python rtl-sdr satellite-images
template: templates/post_with_code_highlight.html
---
#Automatic Capture of NOAA Satellite Images

<br>

##Background Information

<div class="text-center">
	<figure class="figure w-lg-50 m-lg-2 float-lg-start">
		<img src="/img/noaa-capture/20230207_160104-NOAA19.png" class="figure-img" alt="Daylight APT Image" onclick="img_box(this)">
		<figcaption class="figure-caption text-center">An APT image captured during daylight.</figcaption>
	</figure>
</div>

The National Oceanic and Atmospheric Administration (NOAA) owns and operates a [number of satellites](https://www.nesdis.noaa.gov/current-satellite-missions/currently-flying) in orbit around earth. These satellites serve a number of different purposes, ranging from weather monitoring and prediction to helping search and rescue teams locate distress signals from emergency beacons. A group of these satellites known as Polar Operational Environmental Satellites ([POES](https://noaasis.noaa.gov/POLAR/poes_overview.html)) remain in a low polar orbit &mdash; that is, their orbit goes north-south over the poles. This allows the satellites to get a complete view of earth every day as earth rotates underneath them. Though several of these satellites were launched between the 1980s and early 2000s, only three remain operational. The interesting thing about these satellites is that they broadcast a few signals that are free to use if you can receive them. One such signal is the High Resolution Picture Transmission ([HRPT](https://noaasis.noaa.gov/POLAR/HRPT/hrpt.html)) which contains high resolution images (obviously) in infrared, near-infrared, and visible spectra. It also contains some non-image data from other instruments on the spacecraft. Sounds super cool, right? Well, the satellites broadcast that data at frequencies 1698, 1707, and 1702.5 MHz and use a bandwidth of 3 MHz. I am currently unaware of a super cheap or easy way to receive signals at those frequencies and *that bandwidth*. For reference, broadcast FM radio stations in the USA are each allocated 200 kHz bandwidth, which is why the frequencies are spaced at least 0.2MHz apart. Ever notice how all FM radio stations end in .1, .3, .5, .7, or .9? At 3 MHz, the HRPT signal spans 15 FM radio stations worth of bandwidth &mdash; basically, that's *huge* and difficult to receive on cheap equipment. There is, however, another option. The NOAA POES satellites also broadcast an Automatic Picture Transmission (APT) signal. APT is a proprietary slow scan TV signal developed for weather satellites in the 1960s. The APT signal uses only about 34 kHz bandwidth to deliver low-resolution images in real time over an FM signal. The bandwidth is narrow enough to easily be received with cheap equipment.

Remember how I said only three POES satellites remain operational? It's time to meet NOAA-15, NOAA-18, and NOAA-19 which at the time of writing all currently have functioning APT at 137.62, 137.9125, and 137.1 MHz respectively. This might not last forever though. NOAA-15's signals have had several issues in recent years and all three satellites are currently operating well past their designed lifespan. Their current status should be able to be seen [here](https://www.ospo.noaa.gov/Operations/POES/status.html "POES Operational Status").

So how do I receive these signals exactly? I'm using an rtl-sdr device. You can read all about what that is and how it works [here](https://www.rtl-sdr.com/about-rtl-sdr/). Basically, there are these chips that were mass produced for DVB-T TV tuners which some very smart people realized could be modified to function as a wide band RX-only software defined radio (SDR). This has since become quite popular and many people have started selling boards using these chips for the sole purpose of SDR. The gist is, you can buy a cheap (<$40) USB dongle that, when plugged into your computer and used with appropriate software, can receive all sorts of radio signals from ~24-1766 MHz. As you can see the NOAA APT radio signals at ~137 MHz fall easily within that range. The dongle I bought can be found [here](https://www.rtl-sdr.com/buy-rtl-sdr-dvb-t-dongles/) although if you shop around on eBay or Amazon you will probably find even cheaper dongles that perform similarly. If you want to mess around with the dongle and see the kinds of things you can listen to (including broadcast radio) I recommend using a piece of software like [Gqrx](https://gqrx.dk/). 
<div class="text-center">
	<figure class="figure w-lg-50 m-lg-2 float-lg-start">
		<img src="/img/noaa-capture/gqrx_screenshot.png" class="figure-img" alt="Gqrx Screenshot" onclick="img_box(this)">
		<figcaption class="figure-caption text-center">Screenshot of Gqrx showing some FM radio stations.</figcaption>
	</figure>
</div>
The signals picked up by the dongle are just raw radio signals but Gqrx will let you tune the dongle to whatever frequency you want and it can do demodulation for AM and FM signals. Gqrx is not available for Windows, however, I've heard of a program called SDR# which is supposed to be similar.
<div class="clearfix"></div>

The kinds of signals you will be able to pickup depend in large part on the type of antenna used. The signals from the NOAA satellites are circularly polarized and there is some debate over the best kind of antenna to use. Generally, a [Quadrifilar Helicoidal (QFH)](http://jcoppens.com/ant/qfh/calc.en.php) antenna is recommended and can be built with some PVC pipe and some copper tubing or wire. I went with a much easier option and used the V dipole antenna that came with my rtl-sdr dongle.
<div class="text-center">
	<figure class="figure w-lg-50 m-lg-2 float-lg-end">
		<img src="/img/noaa-capture/Antenna.jpg" class="figure-img" alt="Antenna" onclick="img_box(this)">
		<figcaption class="figure-caption text-center">Simple V dipole antenna suction cupped to a clipboard screwed to the ceiling. Works great.</figcaption>
	</figure>
</div>
It works well enough for me and some people say they get even better reception with the dipole because it picks up less interference from terrestrial signals. I set it up according to the dimensions found [here](https://www.rtl-sdr.com/simple-noaameteor-weather-satellite-antenna-137-mhz-v-dipole/ "Simple NOAA/Meteor Weather Satellite Antenna: A 137 MHz V-Dipole"). Basically it's two conductors approximately 21 inches long and 120 degrees apart. Lay it horizontally and face the opening of the V either to the north or the south.
<div class="clearfix"></div>

<br>

##Automating Capture

<div class="text-center">
	<figure class="figure w-lg-50 m-lg-2 float-lg-start">
		<img src="/img/noaa-capture/20230207_044000-NOAA18.png" class="figure-img" alt="Nighttime APT Image" onclick="img_box(this)">
		<figcaption class="figure-caption text-center">An APT image captured during the night.</figcaption>
	</figure>
</div>

So with all of that background information out of the way let's learn how to automatically capture APT images using an rtl-sdr dongle while the satellites are passing overhead. I mostly based my setup on [this tutorial](https://www.instructables.com/Raspberry-Pi-NOAA-Weather-Satellite-Receiver/), however, I made a number of changes to improve the process and used noaa-apt instead of wxtoimg. I am using a computer running Linux Mint and I make heavy use of Linux software, a *lot* of changes would have to be made in order to accomplish a similar setup on Windows, although I *suspect* it's possible. By the way [Linux Mint](https://linuxmint.com/) is *totally free* and this could be a *great* project for an old computer. ;)

<div class="clearfix"></div>

###Software Required

To install all the needed software from apt (the package manager not the Automatic Picture Transmission) use the following command.

`sudo apt install rtl-sdr sox at python3 wget libncurses-dev libpthread-stubs0-dev libasound2-dev`

The individual pieces of software including the commands to install them individually are listed below.

- predict - **install manually (see below)** - We will use this program to determine when the satellites will be passing overhead.
- noaa-apt - **install manually (see below)** - This program will decode our radio recordings into the final image.
- rtl-sdr - `sudo apt install rtl-sdr` - This contains the drivers and a few command-line programs for the rtl-sdr dongle.
- sox - `sudo apt install sox` - This is an audio toolkit that we will use to get a wav file in the appropriate format to be decoded.
- at - `sudo apt install at` - This is a command scheduler we will use to receive data at the right times.
- python3 - `sudo apt install python3` - This is likely already installed, but it is needed for my script that resolves conflicting satellite passes.
- wget - `sudo apt install wget` - This is also likely already installed; it will be used to download TLEs to determine satellite orbits.

<br>
The following are dependencies needed to install predict

- ncurses library - `sudo apt install libncurses-dev`
- pthread development headers - `sudo apt install libpthread-stubs0-dev`
- Advanced Linux Sound Architecture (ALSA) library - `sudo apt install libasound2-dev`

Some software is not in the Linux Mint repositories and will have to be installed manually.

####Installing predict

predict is a very important program for making this work, but unfortunately it is no longer available in the Linux Mint software repositories. This means we will have to build it from source, but don't worry it's super easy. First, make sure you have the dependencies required to build predict, the commands are listed above. On Linux Mint you need `libncurses-dev`, `libpthread-stubs0-dev`, and `libasound2-dev`. Then, go to [the predict website](https://www.qsl.net/kd2bd/predict.html), scroll down to where it says "Download PREDICT," and click "PREDICT Version x.x.x for Linux." Alternatively, you can download the version I used directly [from this link](https://www.qsl.net/kd2bd/predict-2.3.0.tar.gz). Extract the tar file into it's own folder by right-clicking it and clicking "Extract here" or similar depending on your desktop environment. Using a terminal, navigate to the folder it was extracted to. For example `cd /home/USERNAME/Downloads/predict-2.3.0`. Then simply run `./configure` and it should compile and install predict automatically. 

Once installed, you will have to run predict once to configure your location. Simply type `predict` in the terminal. You will need your latitude and longitude; they can be easily obtained from Google Maps by right-clicking your location. Note that *Google Maps* uses positive values for North and positive values for **East**, and *predict* uses positive values for North **but** it uses positive values for **West**. This means you will likely have to adjust your longitude accordingly.

####Installing noaa-apt

This is the program that will decode our recordings into images. Go to [the download page](https://noaa-apt.mbernardi.com.ar/download.html) on the noaa-apt website and follow the instructions for "Debian-based distros (Ubuntu, Linux Mint, etc.)." You should see a link labeled "GNU/Linux x86_64 .deb package." Alternatively, if you know what you are doing it may be easier to find the build you need from [the noaa-apt GitHub Releases page](https://github.com/martinber/noaa-apt/releases). On GitHub you will find builds for ARM processors which is useful if you are using a Raspberry Pi computer for example.

Once you have noaa-apt installed you might want to test it by running `noaa-apt --version` from the terminal. If you see

	noaa-apt image decoder version 1.4.0
	You have the latest version available

or similar output then the installation is successful and you are **done installing software for this project.** :)

<div class="clearfix"></div>

###Making it Happen

Oh... my... goodness... This is a lot of writing and I'm tired. I'll write the rest later hopefully. Below is just a test of what bash will look like on this page.

	#!/bin/bash

	#Variables
	readonly min_elevation=25            #Satellites that don't reach this elevation will be ignored
	readonly record_above_elevation=5    #Set to 0 to record entire pass (NOTE: values above 0 will not be exact)

	#Change directory to script directory
	dir=$(cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
	cd "$dir"

	readonly satellite_name=$1
	readonly frequency=$2
	readonly tle_filename=`pwd -P`/noaa.tle
	readonly receive_data_command=`pwd -P`/receive_data.sh

	PREDICTION_START=`predict -t noaa.tle -p "${satellite_name}" | awk -v elev="$record_above_elevation" '{if($5>=elev){print; exit}}'`
	PREDICTION_END=`predict -t noaa.tle -p "${satellite_name}" | tac | awk -v elev="$record_above_elevation" '{if($5>=elev){print; exit}}'`
	TRUE_PREDICTION_END=`predict -t noaa.tle -p "${satellite_name}" | tail -n1`
	MAX_ELEV=`predict -t noaa.tle -p "${satellite_name}" | awk -v max=0 '{if($5>max){max=$5}}END{print max}'`


	end_timestamp=`echo ${PREDICTION_END} | cut -d " " -f 1`
	true_end_timestamp=`echo ${TRUE_PREDICTION_END} | cut -d " " -f 1`

	while [ "`date --date=\"@${true_end_timestamp}\" +%D`" == "`date +%D`" ]
	do
		start_timestamp=`echo ${PREDICTION_START} | cut -d " " -f 1`
		capture_duration=`expr ${end_timestamp} - ${start_timestamp}`

		if [ $MAX_ELEV -gt $min_elevation  ]
		then
			date_string=`TZ=UTC date --date="@${start_timestamp}"`
			local_date_string=`date --date="@${start_timestamp}" "+%H:%M %D"`
			OUTDATE=`TZ=UTC date --date="@${start_timestamp}" +%Y%m%d_%H%M%S`
			filename_base="${OUTDATE}-${1//" "}"
			echo "Scheduling ${satellite_name} at ${date_string}"
			echo "Local Time:    ${local_date_string}"
			echo "Max Elevation: ${MAX_ELEV}"
			echo "Filename base: ${filename_base}"

			prev_queue=`atq`
			echo "/bin/bash ${receive_data_command} \"${satellite_name}\" \"${frequency}\" \"${filename_base}\" \"${tle_filename}\" \"${start_timestamp}\" \"${capture_duration}\"" | at -M ${local_date_string}
			new_queue=`atq`
			atid=`diff <(echo "${prev_queue}") <(echo "${new_queue}") | tail -n1 | cut -d " " -f 2 | cut -f 1`
			echo "${atid} ${satellite_name//" "} ${start_timestamp} ${end_timestamp} ${MAX_ELEV}" >> queued_jobs
			
			echo ""
		fi

		next_predict=`expr $true_end_timestamp + 60`
		PREDICTION_START=`predict -t noaa.tle -p "${satellite_name}" ${next_predict} | awk -v elev="$record_above_elevation" '{if($5>=elev){print; exit}}'`
		PREDICTION_END=`predict -t noaa.tle -p "${satellite_name}" ${next_predict} | tac | awk -v elev="$record_above_elevation" '{if($5>=elev){print; exit}}'`
		TRUE_PREDICTION_END=`predict -t noaa.tle -p "${satellite_name}" ${next_predict} | tail -n1`
		MAX_ELEV=`predict -t noaa.tle -p "${satellite_name}" ${next_predict} | awk -v max=0 '{if($5>max){max=$5}}END{print max}'`

		end_timestamp=`echo ${PREDICTION_END} | cut -d " " -f 1`
		true_end_timestamp=`echo ${TRUE_PREDICTION_END} | cut -d " " -f 1`
	done

Wow, it's beautiful. I assume. If it worked.