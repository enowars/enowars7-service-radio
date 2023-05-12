def get_metadata(file):
    with open(file, "rb") as f:
        header = f.read(10)
        if header[:3] != b"ID3":
            print("File does not have ID3 tag")
            return

        # Get the tag version.
        major_version = header[3]
        minor_version = header[4]

        # Get the size of the tag.
        size = 0
        for i in range(4):
            size = (size << 7) + (header[6 + i] & 0x7F)

        # Read the tag data.
        tag_data = f.read(size)

        # Parse the tag data.
        pos = 0
        while pos < len(tag_data):
            # Get the frame ID.
            frame_id = tag_data[pos : pos + 4]
            pos += 4

            # Get the frame size.
            frame_size = int.from_bytes(tag_data[pos : pos + 4], byteorder="big")
            pos += 4

            # Get the frame flags.
            frame_flags = tag_data[pos : pos + 2]
            pos += 2

            # Get the frame data.
            frame_data = tag_data[pos : pos + frame_size]
            pos += frame_size

            # Handle the frame data.
            if frame_id == b"TIT2":
                # This is the title frame.
                title = frame_data.decode("utf-8")
                print("Title:", title)
            elif frame_id == b"TPE1":
                # This is the artist frame.
                artist = frame_data.decode("utf-8")
                print("Artist:", artist)
            elif frame_id == b"TCON":
                # This is the genre frame.
                genre = frame_data.decode("utf-8")
                print("Genre:", genre)


get_metadata("../../exploit.mp3")
