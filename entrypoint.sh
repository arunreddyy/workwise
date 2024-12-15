#!/bin/bash

# Set proper permissions for the database file and directory
chmod -R 777 /app/instance

# Start the Flask app
exec "$@"
