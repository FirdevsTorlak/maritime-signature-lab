Maritime Signature Lab – Project Documentation
=======================================
1. Project Overview
____________________

Maritime Signature Lab is a compact, end-to-end prototype for working with synthetic ship signature data.
The project combines:

Python for data processing and analysis

Relational databases (SQLite) for structured storage

Basic computer vision (OpenCV) for extracting features from infrared (IR) images

to model, store and analyse different types of maritime signatures.

The project is designed as a professional showcase for:

working with ship signatures (acoustic, magnetic, RCS, IR),

designing and using a relational data model, and

implementing Python-based tools including a command-line interface (CLI) and simple computer vision.

All data used in this project is synthetic and serves demonstration and training purposes only.

2. Signature Types Covered
_______________________

The prototype currently supports four main signature types:

Acoustic signatures

Example: band-limited sound pressure levels in dB

Stored as frequency bands (e.g. 63 Hz, 125 Hz, 250 Hz) per ship

Magnetic signatures

Example: magnetic field components in different axes

Stored per ship and axis (X, Y, Z) in nT

Radar Cross Section (RCS)

Example: RCS values in dBsm versus aspect angle (0°, 45°, 90°)

Used to show how detectable a ship is at different angles

Infrared (IR) signatures

Represented as grayscale images

Simple computer-vision algorithms are applied to extract:

mean intensity

hotspot count

silhouette area in pixels

These features are stored in a dedicated table and can be correlated with the other signature types.

3. Project Goals
_______________

The main goals of Maritime Signature Lab are:

Relational Data Model
Design and implement a clear, extensible relational schema for ship signature data.

Python Tooling for Data Handling
Provide Python tools to:

import CSV data into a relational database (SQLite by default),

query and visualise acoustic, magnetic and RCS signatures,

compute basic statistics and summaries.

Computer Vision for IR Signatures
Apply simple computer-vision algorithms (OpenCV) to synthetic IR images and store the extracted features (e.g. mean intensity, hotspot count, area) back into the database for further analysis.

4. System Requirements
_____________________

To run the project, you will need:

Operating system: Windows 10/11, Linux or macOS

Python: version 3.9 or higher (Python 3.12 works as well, as in the current setup)

Virtual environment (recommended): venv

Disk space: only a few MB (the project is small)

Optional: a basic Python-capable IDE such as Visual Studio Code

All Python dependencies are listed in requirements.txt:

numpy

pandas

matplotlib

opencv-python

5. Project Structure
_____________________

The repository is organised as follows:

maritime-signature-lab/
  README.md
  requirements.txt
  .gitignore
  .vscode/
    launch.json
    settings.json
  data/
    csv/
      ships.csv
      acoustic_signatures.csv
      magnetic_signatures.csv
      rcs_signatures.csv
    images/
      ir/
        README.txt          (place IR images here)
  db/
    schema.sql              (relational schema)
    init_db.py              (helper to initialise the database)
  src/
    shipsig/
      __init__.py
      config.py
      db.py
      loaders.py
      cli.py
      analysis/
        __init__.py
        acoustic.py
        magnetic.py
        rcs.py
        ir_cv.py
  notebooks/
    (currently empty; can be used for Jupyter notebooks)

Key components:

db/schema.sql – definition of the database tables

data/csv/ – sample CSV files with synthetic ship and signature data

data/images/ir/ – folder for IR images (PNG). The filenames encode the ship ID.

src/shipsig/ – the Python package providing configuration, database access, data import and analysis functions

src/shipsig/cli.py – the command-line interface entry point

6. Installation and Setup (Step-by-Step)
______________________________
6.1. Download the project
--------------------------

Download the ZIP archive maritime-signature-lab.zip.

Extract it, for example to:

Windows: C:\Users\<yourname>\Downloads\maritime-signature-lab

Linux/macOS: ~/projects/maritime-signature-lab

Open this folder in Visual Studio Code (File → Open Folder).

6.2. Create and activate a virtual environment
-------------------------------------------

Open a terminal inside the maritime-signature-lab folder.

Windows PowerShell:

cd C:\Users\<yourname>\Downloads\maritime-signature-lab
python -m venv .venv
.\.venv\Scripts\Activate.ps1

You should now see (.venv) at the beginning of your terminal prompt.

Linux / macOS (bash/zsh):

cd ~/projects/maritime-signature-lab
python -m venv .venv
source .venv/bin/activate

6.3. Install Python dependencies
---------------------------------

With the virtual environment activated:

pip install --upgrade pip
pip install -r requirements.txt

This will install numpy, pandas, matplotlib and opencv-python into the virtual environment.

6.4. Ensure Python can find the shipsig package (PYTHONPATH)
------------------------------------------------

The Python package code lives under src/shipsig/.
To make python -m shipsig.cli work from the project root, we add src to PYTHONPATH.

Windows PowerShell:

$env:PYTHONPATH = "$PWD\src"

Linux / macOS:

export PYTHONPATH="$PWD/src"

You need to run this command in every new terminal where you want to use the CLI, unless you add it to your shell profile.

7. Database Setup and Sample Data
_________________________________

Once the environment is ready, you can set up the SQLite database and import the sample data.

From the project root (maritime-signature-lab):

python -m shipsig.cli init-db
python -m shipsig.cli import-data

init-db

Creates or resets the db/signatures.db file using db/schema.sql.

import-data

Reads CSV files from data/csv/ and populates the tables:

ships

acoustic_signatures

magnetic_signatures

rcs_signatures

You should see messages in the terminal confirming that the database has been initialised and that the sample data has been imported.

8. Command-Line Interface (CLI) Usage
_____________________________________

The CLI is implemented in src/shipsig/cli.py and exposes several commands for typical analysis tasks.

8.1. Available commands
---------------------------

From the project root (with .venv active and PYTHONPATH set):
python -m shipsig.cli init-db          # create/reset the database
python -m shipsig.cli import-data      # import sample CSV data
python -m shipsig.cli acoustic-summary # show average acoustic levels
python -m shipsig.cli magnetic-summary # show magnetic field summary
python -m shipsig.cli rcs-summary      # show RCS values vs. aspect angle
python -m shipsig.cli ir-features      # compute IR image features (if images exist)

8.2. Example: Acoustic summary
-------------------------------
python -m shipsig.cli acoustic-summary

Example output:
ship_name band_label  mean_level_db
    Alpha     125 Hz           92.0
    Alpha     250 Hz           88.0
    Alpha      63 Hz           95.0
    Bravo     125 Hz           94.0
    Bravo     250 Hz           90.0
    Bravo      63 Hz           98.0
  Charlie     125 Hz           87.0
  Charlie     250 Hz           83.0
  Charlie      63 Hz           90.0

9. Working with the Data in Python (Interactive Mode)
_______________________________________________

You can also work with the data interactively in a Python REPL (or Jupyter notebook).

9.1. Open Python
----------------

From the project root, with the virtual environment active and PYTHONPATH set:
python

Then in Python:

from shipsig.db import get_connection
import pandas as pd

conn = get_connection()

df_acoustic = pd.read_sql_query("SELECT * FROM acoustic_signatures", conn)
print(df_acoustic.head())

9.2. Using analysis functions
-------------------------------

You can also use the analysis functions provided in shipsig.analysis:

from shipsig.analysis.acoustic import acoustic_summary
from shipsig.analysis.magnetic import magnetic_summary
from shipsig.analysis.rcs import rcs_summary

df_acoustic_summary = acoustic_summary(conn)
df_magnetic_summary = magnetic_summary(conn)
df_rcs_summary = rcs_summary(conn)

print(df_acoustic_summary)
print(df_magnetic_summary)
print(df_rcs_summary)

9.3. Plotting (visualisations)
-------------------------------

The analysis modules contain plotting functions using matplotlib.
These open a window with the corresponding chart (if you have a GUI environment).

Example:
from shipsig.analysis.acoustic import plot_acoustic_bands
from shipsig.analysis.magnetic import plot_magnetic_axes
from shipsig.analysis.rcs import plot_rcs_curve

plot_acoustic_bands(conn, "Alpha")   # bar chart of acoustic bands
plot_magnetic_axes(conn, "Alpha")    # magnetic field per axis
plot_rcs_curve(conn, "Alpha")        # RCS vs. aspect angle

10. IR Images and Computer Vision Features
__________________________________________

The IR module (shipsig.analysis.ir_cv) processes grayscale IR images and extracts features.

10.1. IR image naming convention
--------------------------------

Place your synthetic IR images (PNG format) in:

data/images/ir/

Use filenames like:
ship_001_view_000.png
ship_001_view_045.png
ship_002_view_000.png

The pattern ship_<ID>_ is used to infer the ship_id.

10.2. Running the IR feature extraction
-------------------------------------------

From the project root:

python -m shipsig.cli ir-features

This will:

Read all .png files in data/images/ir/

Infer the ship_id from the filename

Compute:

mean_intensity (average pixel value)

hotspot_count (number of very bright pixels)

area_px (number of pixels above a lower threshold)

Insert the results into the ir_features table in the database.

You can verify the results in Python:

df_ir = pd.read_sql_query("SELECT * FROM ir_features", conn)
print(df_ir)

11. Data Model – High-Level Description
_________________________________________

The relational schema is intentionally simple and extendable.

Main tables:

ships

Basic information about each ship (name, class, displacement, length, beam)

Primary key: id

acoustic_signatures

Acoustic band levels (in dB) per ship and band

Columns: ship_id, band_label, level_db

Foreign key: ship_id → ships.id

magnetic_signatures

Magnetic field components per ship and axis

Columns: ship_id, axis, value_nt

Foreign key: ship_id → ships.id

rcs_signatures

Radar Cross Section values in dBsm per ship and aspect angle

Columns: ship_id, aspect_deg, rcs_dbsm

Foreign key: ship_id → ships.id

ir_features

Features extracted from IR images

Columns: ship_id, image_path, mean_intensity, hotspot_count, area_px

Foreign key: ship_id → ships.id

Because all signature tables reference ships, it is easy to:

perform joined analyses across multiple signature types,

aggregate results per ship, class, or other attributes.

12. Technologies Used
_________________________

Python 3.9+ – main programming language

SQLite – default relational database backend

pandas, numpy – data handling, grouping, basic statistics

matplotlib – visualisation (e.g. acoustic band plots, RCS curves)

opencv-python (OpenCV) – basic computer vision on IR images

Virtual environments (venv) – isolated Python environment

13. Possible Extensions
_________________________

The project is intentionally kept compact but can be extended in many directions:

Adding more realistic or higher-resolution synthetic data

Introducing additional signature types or sensor configurations

Implementing more advanced signal- and image-processing techniques

Switching from SQLite to PostgreSQL and:

adding indexes,

defining more complex queries,

integrating with external tools or dashboards.

14. Kurze deutschsprachige Zusammenfassung

Dieses Projekt demonstriert in kompakter Form den Aufbau und die Pflege einer
Signaturdatenbank für Schiffe (Akustik, Magnetik, RCS, IR) auf Basis einer
relationalen Datenbank (SQLite) sowie die Auswertung mit Python.

Es umfasst:

ein klar strukturiertes Datenmodell mit Fremdschlüsselbeziehungen,

Python-Skripte zum Import, zur Abfrage und zur Auswertung von
Signaturdaten (pandas, numpy, matplotlib),

eine Command-Line-Interface (CLI) mit typischen Befehlen (z.B. init-db,
import-data, acoustic-summary, ir-features),

sowie einfache Computer-Vision-Algorithmen (OpenCV), um aus
synthetischen IR-Schiffsaufnahmen Merkmale (mittlere Intensität, Anzahl
von Hotspots, Silhouettenfläche) zu extrahieren und in einer eigenen
Tabelle (ir_features) abzulegen.

Damit eignet sich das Projekt als Beispiel für datenbankgestützte Auswertungen,
Prototyping im Bereich Gesamtsignatur und den Einsatz von Python im maritimen Umfeld.



