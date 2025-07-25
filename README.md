# AI House Plan Generator

## Overview
The AI House Plan Generator is a Streamlit-based web application that leverages artificial intelligence to help users design custom house plans. Users can specify various house dimensions, room requirements, design preferences, and outdoor features. The application then generates a professional-style floor plan with labeled dimensions and provides additional city-specific information related to construction, such as material costs, builder contacts, project timeline estimations, solar panel companies, and legal/permit guidance.

## Features
- **AI-Powered Plan Generation:** Generate detailed house plans based on user input using the `g4f` AI model.
- **Customizable Specifications:** Define total length, width, number of floors, bedrooms, bathrooms, and various room types (kitchen, living room, office, laundry, etc.).
- **Design Preferences:** Choose house styles (Modern, Traditional, Contemporary, etc.), layout preferences (Open Floor Plan, Compartmentalized), and include accessibility features.
- **Outdoor Features:** Specify garage options and outdoor spaces like patios, decks, and gardens.
- **Multiple Rendering Styles:** Generate plans in various visualization styles, including Blueprint (2D), Detailed Floor Plan (2D), 3D Floor Plan, and Isometric View.
- **Furniture Detail Control:** Adjust the level of furniture detail in the generated plans.
- **Color Schemes & Resolution:** Select color schemes (Blueprint, Grayscale, Colored) and image resolution (Standard, High, Ultra High).
- **Saved Plans:** View and manage previously generated house plans within the application.
- **City-Specific Information (Tamil Nadu, India):**
    - **Material Cost Estimates:** Approximate costs and supplier contacts for construction materials (steel, bricks, cement, sand).
    - **Top Builders & Budget Estimates:** Information on leading builders and estimated house model budgets.
    - **Project Timeline Estimation:** A general timeline breakdown for house construction phases.
    - **Solar Panel Companies & Cost:** Details on solar panel providers and cost estimates for energy efficiency.
    - **Legal & Permit Guidance:** Essential information on required documents and processes for house construction approvals.

## Technologies Used
- **Python**
- **Streamlit:** For building the interactive web application.
- **g4f:** Used for AI image generation.
- **Requests:** For handling HTTP requests (e.g., fetching generated images).

## Setup and Installation

### Prerequisites
- Python 3.x
- pip (Python package installer)

### Using `py.bat` (Windows Batch Script)
The `py.bat` script provides a convenient way to manage the Python virtual environment and run the application on Windows.

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd AI-House-Plan-Generator
    ```

2.  **Run `py.bat`:**
    Double-click `py.bat` or run it from your command prompt:
    ```bash
    py.bat
    ```

3.  **Follow the menu options:**
    -   **1. Create and setup virtual environment:** This will create a virtual environment named `myenv`, activate it, install all dependencies from `requirements.txt`, and then deactivate it.
    -   **2. Delete virtual environment:** Removes the `myenv` directory.
    -   **3. Run Python file in virtual environment:** Allows you to select and run a Python file (e.g., `app.py`) within the activated virtual environment.
    -   **4. Exit:** Closes the script.

### Manual Setup (Alternative)

1.  **Create a virtual environment:**
    ```bash
    python -m venv myenv
    ```

2.  **Activate the virtual environment:**
    -   **Windows:**
        ```bash
        .\myenv\Scripts\activate
        ```
    -   **macOS/Linux:**
        ```bash
        source myenv/bin/activate
        ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Activate your virtual environment** (if not using `py.bat` option 3):
    -   **Windows:** `.\myenv\Scripts\activate`
    -   **macOS/Linux:** `source myenv/bin/activate`

2.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```

3.  Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

## Project Structure

```
AI-House-Plan-Generator/
├── app.py                  # Main Streamlit application code
├── py.bat                  # Windows batch script for environment management and running the app
├── requirements.txt        # Lists Python dependencies
└── har_and_cookies/
    └── blackbox.json       # Placeholder for potential HAR/cookie data (currently contains a validated value)
```

## Important Disclaimer
The floor plans generated by this application are conceptual in nature and are intended for visualization purposes only. They are not construction documents and should not be used for building without proper review and modification by a licensed architect or engineer.

The dimensions, room layouts, and structural elements shown may not comply with local building codes, zoning regulations, or other requirements. Always consult with a professional before proceeding with any construction project.

## License
[Specify your license here, e.g., MIT License]

## Contact
[Your Contact Information or GitHub Profile]
