# ByteStorm - Disaster Prevention and Assistance Web App

## Overview

ByteStorm is a Django web app that provides prevention and assistance during natural disasters. The platform offers guidelines and essential help to those in need before, during, and after natural disasters. ByteStorm helps users prepare for emergencies, locate critical resources, and connect with others who are willing to offer help.

## Features

- **Prevention Guidelines**: Offers AI-driven predictive tips on reducing risks and preparing for potential natural disasters. This includes creating emergency kits, knowing evacuation routes, securing homes, and staying informed.
- **Emergency Resources**: Provides information on essential emergency resources such as shelters, hospitals, and gas stations. Users can quickly find the nearest available help when disaster strikes. Resource information is updated regularly to ensure accuracy.
- **Community Assistance Matching**: Matches people in need with those who are offering assistance, allowing for community-driven support during difficult times. Matching is based on location and specific needs.
- **Real-Time Alerts and ByteBot Chat**: Users can interact with ByteBot, an integrated chatbot that provides real-time information and answers to frequently asked questions about natural disasters.

## Technology Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript (Materialize CSS framework for design)
- **Chatbot**: Integrated using JavaScript to facilitate real-time interactions

## Installation

To get started with ByteStorm, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/username/bytestorm.git
   cd bytestorm
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the Web App**:
   Open your web browser and navigate to `http://127.0.0.1:8000/`.

## Usage

Once the server is running, you can use ByteStorm to:

- **Prepare for Disasters**: Access detailed prevention guidelines to help minimize risks.
- **Locate Emergency Resources**: Use the resource finder to get real-time information on shelters, hospitals, and gas stations nearby.
- **Get Assistance**: Connect with other users who are offering assistance.
- **Chat with ByteBot**: Use the integrated chatbot to get immediate answers to your questions.

## Contribution

We welcome contributions to improve ByteStorm. To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

Before contributing, please review the existing issues to avoid redundancy.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details. The MIT License is a permissive license that allows for reuse with few restrictions, making it ideal for open-source projects.

