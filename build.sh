#!/bin/bash

# Create build directory
mkdir -p build

# Copy only the necessary files
cp jobspy_app.py build/
cp requirements.txt build/
cp Procfile build/
cp runtime.txt build/
cp -r jobspy build/

# Create minimal wrangler.toml in build dir
cat > build/wrangler.toml << EOF
[site]
bucket = "./"

[env.production]
name = "lucy-job-search"
EOF

echo "Build completed successfully!" 