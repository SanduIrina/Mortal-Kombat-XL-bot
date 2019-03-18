A short example of a video streaming client implementation.


# Usage:

After configuring your dependencies and configuring the stream parameters (see stream_config API), run

```
python main.py <port>
```

# Dependencies

- Python (tested with Python 2.7.15)

- Opencv-python ( see https://pypi.org/project/opencv-python/ )

- Pillow

After installing Python & Pip, run

```
pip install Pillow
pip install opencv-python
```

# Short explanation

Packets are sent over UDP. Each frame packet also contains the following information:

- Current frame number

- Current packet number

- Max number of packets

- The resized ratio the server used for the current frame (you must specify this when configuring your stream, see /stream_config API)
