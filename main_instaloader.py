import instaloader
import os
import json
import dotenv

dotenv.load_dotenv()

def load_downloaded_posts():
    """Load previously downloaded post IDs from JSON file"""
    if os.path.exists('downloaded_posts.json'):
        with open('downloaded_posts.json', 'r') as f:
            return set(json.load(f))
    return set()

def save_downloaded_posts(downloaded_posts):
    """Save downloaded post IDs to JSON file"""
    with open('downloaded_posts.json', 'w') as f:
        json.dump(list(downloaded_posts), f)

def download_profile_videos(username, download_only_new=True):
    # Initialize Instaloader
    L = instaloader.Instaloader()
    
    try:
        # Login to Instagram - corrected syntax
        L.login(os.getenv("INSTAGRAM_USERNAME"), os.getenv("INSTAGRAM_PASSWORD"))
        
        # Get profile
        profile = instaloader.Profile.from_username(L.context, username)
        
        # Load previously downloaded posts
        downloaded_posts = load_downloaded_posts() if download_only_new else set()
        newly_downloaded = set()
        
        # Iterate through profile posts
        for post in profile.get_posts():
            # Skip if already downloaded and we only want new videos
            if post.shortcode in downloaded_posts:
                continue
                
            # Check if post contains video
            if post.is_video:
                try:
                    # Download the video
                    L.download_post(post, target=f"videos/{username}")
                    print(f"Video downloaded successfully from post: {post.shortcode}")
                    newly_downloaded.add(post.shortcode)
                except Exception as e:
                    print(f"Error downloading video {post.shortcode}: {str(e)}")
        
        # Update downloaded posts record
        downloaded_posts.update(newly_downloaded)
        save_downloaded_posts(downloaded_posts)
        
        return True
    except Exception as e:
        print(f"Error accessing profile: {str(e)}")
        return False

if __name__ == "__main__":
    # Instagram username
    username = "forklore.asia"
    
    # Create downloads directory if it doesn't exist
    if not os.path.exists(f"videos/{username}"):
        os.makedirs(f"videos/{username}")
    
    # Download videos (True means only download new videos)
    download_profile_videos(username, download_only_new=True)
