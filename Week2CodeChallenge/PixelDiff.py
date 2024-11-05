import cv2
import numpy as np
import os
import re
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from tqdm import tqdm  # For progress display

#This is code that reads from a video directory, and records the frame-by-frame movement between pixels 
#in a region of interest (ROI) in the video. The code then calculates the average movement, standard deviation, and so on and saves it.

# The code is designed to process multiple videos in parallel using ThreadPoolExecutor.
# The challenge is to rewrite this to be more efficient and better use hardware resources like GPUs or CPUs

# If you really want a challenge, try using other Machine Learning libraries like TensorFlow or PyTorch to detect objects movement in the video.





# Set constants
VIDEO_DIRECTORY = '.\video'
ROI = (1520, 1600, 450, 570)  # x1, x2, y1, y2
FRAMES_PER_SEGMENT = 36000  # 60 fps * 60 sec * 10 min = 36,000 frames
OUTPUT_CSV = 'b2 door framediff.csv'
DEBUG=True
# Function to extract the datetime from the video filename
def extract_datetime_from_filename(filename):
    # Assuming the filename format is: "YYYY-MM-DD HH-MM-SS.mp4"
    datetime_str = re.search(r'\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2}', filename)
    if datetime_str:
        return datetime.strptime(datetime_str.group(), '%Y-%m-%d %H-%M-%S')
    elif DEBUG:
        #we'll assume you aren't having direct access to the research files, so we'll just proceed with date now
        return datetime.now()
    else:
        raise ValueError(f"Filename format incorrect: {filename}")

# Function to calculate pixel differences for a segment of frames
def process_video_segment(video_path, segment_start, segment_end):
    movement_data = []
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Cannot open video {video_path}")
        return None

    # Set starting position of the video
    cap.set(cv2.CAP_PROP_POS_FRAMES, segment_start)
    previous_frame = None  # Initialize previous_frame as None

    # Process frames within the segment
    for frame_index in range(segment_start, segment_end):
        ret, frame = cap.read()
        if not ret:
            print(f"Error: Cannot read frame {frame_index} in {video_path}")
            break

        # Convert frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Extract the region of interest (ROI)
        roi_frame = gray_frame[ROI[2]:ROI[3], ROI[0]:ROI[1]]

        if previous_frame is not None:  # Skip the first frame
            # Compute pixel differences in the ROI
            diff = cv2.absdiff(roi_frame, previous_frame)
            pixel_difference = np.sum(diff)
            movement_data.append(pixel_difference)

        # Update previous frame
        previous_frame = roi_frame

    # Release video capture
    cap.release()

    return movement_data

# Function to process each video and calculate metrics
def process_video(video_path):
    video_filename = os.path.basename(video_path)
    window_start_time = extract_datetime_from_filename(video_filename)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Cannot open video {video_path}")
        return []

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    segment_start = 0
    results = []

    while segment_start < frame_count:
        segment_end = min(segment_start + FRAMES_PER_SEGMENT, frame_count)
        movement_data = process_video_segment(video_path, segment_start, segment_end)

        if movement_data and len(movement_data) > 0:
            average_movement = np.mean(movement_data)
            variance = np.var(movement_data)
            std_deviation = np.std(movement_data)
            std_error = std_deviation / np.sqrt(len(movement_data))
        else:
            average_movement = variance = std_deviation = std_error = 0.0

        # Extract hour and minute
        hour = window_start_time.hour
        minute = window_start_time.minute

        # Prepare the result for the current segment
        result = {
            'date_time': window_start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'start_time': window_start_time,
            'end_time': window_start_time + timedelta(minutes=10),  # Always 10-minute segments
            'hour': hour,
            'minute': minute,
            'average_movement': average_movement,
            'std_deviation': std_deviation,
            'std_error': std_error,
            'variance': variance
        }

        # Append result for this segment
        results.append(result)

        # Move to the next segment
        segment_start += FRAMES_PER_SEGMENT
        # Update the window start time to reflect the next 10-minute block
        window_start_time += timedelta(minutes=10)

    return results

# Function to write results to CSV in batches
def write_results_to_csv(results):
    df = pd.DataFrame(results)
    df.to_csv(OUTPUT_CSV, mode='a', header=not os.path.exists(OUTPUT_CSV), index=False)

# Function to process all videos in parallel
def process_videos_in_parallel(video_directory):
    video_paths = [os.path.join(video_directory, f) for f in os.listdir(video_directory) if f.endswith('.mp4')]
    
    total_segments = sum(
        (int(cv2.VideoCapture(video_path).get(cv2.CAP_PROP_FRAME_COUNT)) // FRAMES_PER_SEGMENT) + 1
        for video_path in video_paths if int(cv2.VideoCapture(video_path).get(cv2.CAP_PROP_FRAME_COUNT)) > 0
    )

    with ThreadPoolExecutor(max_workers=3) as executor:
        with tqdm(total=total_segments, desc="Processing segments", unit="segment", ncols=100) as progress_bar:
            futures = []
            
            for video in video_paths:
                print(f"Processing video: {video}")
                futures.append(executor.submit(process_video, video))
            
            all_results = []
            for future in tqdm(futures, desc="Writing results", unit="video", ncols=100):
                try:
                    video_results = future.result()
                    if video_results:
                        all_results.extend(video_results)
                        # Write batch results to CSV
                        write_results_to_csv(video_results)
                        print(f"Finished processing segment. Data written to CSV.")
                except Exception as exc:
                    print(f"Error processing video: {exc}")
                progress_bar.update(1)

# Main function
if __name__ == "__main__":
    # Create CSV file and write headers if it doesn't exist
    pd.DataFrame(columns=[
        'date_time', 'start_time', 'end_time', 
        'hour', 'minute', 'average_movement', 
        'std_deviation', 'std_error', 'variance'
    ]).to_csv(OUTPUT_CSV, mode='w', index=False)

    process_videos_in_parallel(VIDEO_DIRECTORY)
    print("Processing complete.")
