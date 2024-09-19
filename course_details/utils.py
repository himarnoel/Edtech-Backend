import cloudinary
import cloudinary.api


def get_video_duration(public_id):
    """
    Retrieves the duration of a video from Cloudinary using the public ID.

    Args:
        public_id (str): The public ID of the video.

    Returns:
        float: Duration of the video in seconds, or None if not found.
    """
    try:
        # Fetch the resource details for the given public ID
        response = cloudinary.api.resource(public_id, resource_type='video')
        print("response"+" " + str(response))
        # Extract and return the duration
        duration = response.get('duration', None)
        return duration
    except cloudinary.exceptions.Error as e:
        # Handle errors (e.g., invalid public ID, API issues)
        print(f"Error fetching video details: {e}")
        return None
