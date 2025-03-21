# SmartDB Architect Frontend

The frontend application for SmartDB Architect, built with React and Material UI.

## Overview

This frontend provides a user-friendly interface to:
- Convert natural language descriptions to SQL code
- Upload and convert ER diagram images to SQL code
- Edit and execute the generated SQL
- Visualize database schema and results

## Directory Structure

```
frontend/
├── package.json           # Project dependencies and scripts
├── vite.config.js         # Vite configuration
├── public/                # Public assets
└── src/                   # Source code
    ├── components/        # Reusable React components
    ├── pages/             # Page components
    ├── services/          # API service modules
    ├── assets/            # Static assets
    ├── App.jsx            # Main application component
    └── main.jsx           # Entry point
```

## Setup

1. Install dependencies:
   ```
   npm install
   ```

2. Start the development server:
   ```
   npm run dev
   ```

3. Build for production:
   ```
   npm run build
   ```

## Features

### Natural Language to SQL
- Input your database structure description in natural language
- Visualize the generated SQL with syntax highlighting
- Edit the generated SQL code
- Execute the SQL to create the database

### ER Diagram to SQL
- Drag and drop or select an ER diagram image
- Preview the image before processing
- Convert the diagram to SQL code
- Execute the SQL to create the database

### Execution and Results
- View execution logs and results
- Error handling with user-friendly messages
- Database schema visualization

## Development

- Frontend uses React for a component-based UI
- Material UI provides a modern, responsive design
- React Router handles navigation
- React Ace for SQL code editing with syntax highlighting
- Axios for API communication with the backend
