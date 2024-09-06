# VideoEditor

VideoEditor is an automated video editing tool that uses the MoviePy library to perform video editing tasks based on user requirements. Key features include the ability to extract and add subtitles to videos quickly and easily. VideoEditor leverages advanced AI technology from OpenAI and can use the WhisperModel for language-related tasks.

## Features

- Extract text from video subtitles.
- Add subtitles to videos.
- Utilize AI to enhance and optimize the video editing process.
- Edit videos quickly according to user specifications.

## Installation

To use VideoEditor, follow these steps:

### Step 1: Clone the Repository

```bash
git clone https://github.com/DienStudio/VideoEditor.git
```

### Step 2: Create a Virtual Environment

Navigate to the VideoEditor directory:

```bash
cd VideoEditor
```

Create a virtual environment:

```bash
python -m venv .venv
```

### Step 3: Activate the Virtual Environment

```bash
.venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run the Application

```bash
py main.py
```

## Notes

- Ensure that `magick.exe` is downloaded and installed. Set the path to `IMAGEMAGICK_BINARY` in the configuration file to use image-related features.

- If OpenAI cannot be used, you can replace it with WhisperModel. However, note that this may take longer.
