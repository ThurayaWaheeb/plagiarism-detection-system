# Plagiarism Detection System

A system for detecting plagiarism in graduation projects using AI embeddings.

## Run the system

1. Install Docker
2. Clone the repository

git clone https://github.com/ThurayaWaheeb/plagiarism-detection-system

3. Go to project folder

cd ai_service

4. Build Docker image

docker build -t plagiarism-system .

5. Run the system

docker run -p 8000:8000 plagiarism-system

6. Open API documentation

http://localhost:8000/docs
