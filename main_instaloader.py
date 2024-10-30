import instaloader
import os

def download_instagram_video(post_url):
    # Initialize Instaloader
    L = instaloader.Instaloader()
    
    # Extract shortcode from URL
    shortcode = post_url.split("/p/")[1].rstrip("/")
    
    try:
        # Get post by shortcode
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        
        # Download the video
        L.download_post(post, target="downloads")
        print(f"Video downloaded successfully from post: {shortcode}")
        
        return True
    except Exception as e:
        print(f"Error downloading video: {str(e)}")
        return False

if __name__ == "__main__":
    # Instagram post URL
    post_url = "https://www.instagram.com/p/C4cu1_bLyVL/"
    
    # Create downloads directory if it doesn't exist
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    
    # Download the video
    download_instagram_video(post_url)
