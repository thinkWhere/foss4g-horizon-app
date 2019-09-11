from line_of_sight_map import LineOfSightMap
from highlight_peaks import HighlightPeaks
from s3_service import S3Service
import os
from viewpoint import Viewpoint
from config import Config
from time import process_time


def process_viewpoints():
    viewpoints = Viewpoint()
    entries = viewpoints.get_unprocessed_viewpoints()
    print(f"Found {len(entries)} records to process")

    start_time = process_time()
    for entry in entries:
        # Generate the LineOfSight map
        map = LineOfSightMap(entry["x"], entry["y"], None)
        map.create_map()

        # Create a Horizon image
        image_filename = f"image{entry['id']}.png"
        map.create_image(image_filename)

        # Create a Peaks file
        peaks_filename = f"peaks{entry['id']}.json"
        peak_finder = HighlightPeaks()
        peaks = peak_finder.get_visible_peaks(map, entry["x"], entry["y"], map.observation_height)
        peak_finder.save_to_file(peaks, peaks_filename)

        # Save the output files to S3
        s3_service = S3Service()
        s3_service.upload_file(Config.VIEWER_BUCKET, f"data/{image_filename}", image_filename)
        s3_service.make_file_public(Config.VIEWER_BUCKET, f"data/{image_filename}")
        s3_service.upload_file(Config.VIEWER_BUCKET, f"data/{peaks_filename}", peaks_filename)
        s3_service.make_file_public(Config.VIEWER_BUCKET, f"data/{image_filename}")

        # Delete the local files
        os.remove(image_filename)
        os.remove(peaks_filename)

        # Update the database
        viewpoints.set_viewpoint_as_processed(entries[0]["id"], image_filename, peaks_filename)

        # User output
        end_time = process_time()
        print(f"processed viewpoint in {end_time - start_time} seconds")
        start_time = end_time


if __name__ == "__main__":
    process_viewpoints()
