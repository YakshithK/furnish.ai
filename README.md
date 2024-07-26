# Furnish.AI

Furnish.AI is a web application designed to assist newly moved homeowners in furnishing their homes. Using computer vision and machine learning, the application detects existing furniture in an uploaded room image and recommends new items based on a selected style.

## Features

- Upload an image of your room
- Detect existing furniture items in the image
- Select a style for recommendations (e.g., Modern, Basic, Cozy, Antique)
- Receive furniture recommendations based on the selected style and detected items

## Technologies Used

- Python
- Flask
- OpenCV
- Roboflow
- SQLite
- Bootstrap
- Jinja2

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/furnish.ai.git
    ```

2. Navigate to the project directory:
    ```sh
    cd furnish.ai
    ```

3. Create a virtual environment:
    ```sh
    python -m venv venv
    ```

4. Activate the virtual environment:
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```

5. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

6. Set up the SQLite database:
    ```sh
    python database/sqlite3_generation.py
    ```

## Usage

1. Start the Flask server:
    ```sh
    python app.py
    ```

2. Open your web browser and navigate to:
    ```
    http://127.0.0.1:5000/
    ```

3. Upload an image of your room.

4. Select a style from the provided options.

5. View the detected furniture items and the recommended items based on your selected style.

## Project Structure

```plaintext
furnish.ai/
│
├── database/
│   ├── sqlite3_generation.py     # Script for generating and populating the SQLite database
│   └── furniture.db              # SQLite database file
│
├── static/
│   ├── uploads/                  # Directory for uploaded images
│   ├── styles/                   # Directory for style images
│   └── images/                   # Directory for furniture item images
│
├── templates/
│   └── index.html                # Main HTML template
│
├── app.py                        # Main Flask application
├── requirements.txt              # Python package dependencies
└── README.md                     # Project README file

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any changes or additions.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Roboflow](https://roboflow.com/)
- [OpenCV](https://opencv.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Bootstrap](https://getbootstrap.com/)

---

**Developed by [Yakshith](https://github.com/YakshithK)**

