# Chat Application

This repository contains the source code for a simple yet feature-rich chat application built with Flask and Socket.IO. The application allows users to register, login, participate in a global chat room, send private messages to other users, and view their message history.

## Features

- **User Registration and Login**: Users can create accounts and log in to access the chat functionalities.
- **Global Chat Room**: A common area where all online users can communicate in real-time.
- **Private Messaging**: Users can send private messages to each other directly.
- **Message History**: Users can view their past conversations within the application.

## Getting Started

### Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed the latest version of Python.
- You have installed Flask, Flask-SocketIO, and Flask-SQLAlchemy. If not, please refer to the installation instructions below.

### Installation

Follow these steps to set up the project:

1. Clone the repository:

   ```
   git clone https://github.com/NafisRayan/chat-app.git
   ```

2. Navigate to the project directory:

   ```
   cd chat-app
   ```

3. Create a virtual environment and activate it:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

5. Run the application:

   ```
   python app.py
   ```

   The application will start on `http://localhost:5000`.

## Usage

1. Open a web browser and navigate to `http://localhost:5000`.
2. Register a new user or log in with an existing user.
3. Once logged in, you can chat in the global chat room or send private messages to other users.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Project Link: [https://github.com/NafisRayan/chat-app](https://github.com/NafisRayan/chat-app)
