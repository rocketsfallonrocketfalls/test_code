#!python3 -m pip install youtube-dl
import youtube_dl, cv2, glob, os
from pathlib import Path
import shutil



def get_filename(fp, ext=False): # gets filename from a given path removing the extension if ext=False.
    fullname = Path(fp).name
    if ext:
        return fullname
    else:
        return os.path.splitext(fullname)[0]
        
# FPS val may be float. Better use time instead of frequency.
def extract_frames(vpath, step=1): # Extracts frames by "step" in ms. 
    ts_s = 0 # init timestep in seconds.
    fname = get_filename(vpath) # vfilename w/o extension. 
    fpath = './videos/' + fname # target path.   

    print(f"Starting to process {fname}, frames will be extracted to: {fpath}")
    cap = cv2.VideoCapture(vpath)  # Start capture.
    while True:        
        cap.set(cv2.CAP_PROP_POS_MSEC,ts_s*1000) # Jump to the timestep.	
        ret, frame = cap.read()  # read frame.

        # Frame extracted successfully.
        if ret:
            if not os.path.isdir(fpath): # Create target folder if does not exist.
                   os.makedirs(fpath)         
            assert os.path.isdir(fpath), "The target folder does not exist." # Make sure folder is created.

            cv2.imwrite(f"{fpath}/{fname}_{ts_s}.png", frame) # Save the frame accordingly. 

        # No frames left to extract.
        else:
            print('Done.')
            cap.release()
            break

        ts_s = ts_s + step # Jump to the next second to collect with 1 FPS.
        

if __name__ == "__main__":

    # Pre-configurations.
    assert os.path.isfile('target_urls.txt'), "Please provide the target video URLs line-by-line in ./target_urls.txt"
    print('Reading the video links.')
    with open('target_urls.txt', 'r') as targets: # Get the URLs from the file.
        links = targets.readlines()
    if len(links)>0:
        print(f"{len(links)} URLs have been found.")
    else:
        exit("No links have been found in target_urls.txt. Program terminated.")     
    save_path = './videos_temp' # Path to contain the temporary video files.
    ydl_opts = {'outtmpl': save_path+'/%(id)s.%(ext)s'} # ydl-config for path.


    # Download and save the videos accordingly to the pre-configurations.
    ydl_opts = {'outtmpl': save_path+'/%(id)s.%(ext)s'} # Save videos to the predefined path in the format: "vid_id.extension"
    print(f"Starting to download the videos to the path: {save_path}")
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(links)
    print("The videos have been downloaded successfully.")
    
    # Main loop.
    fplist = glob.glob(save_path+'/*') # Get the downloaded file paths.
    for vpath in fplist:
        ts_s = 0 # init timestep in seconds.
        step = 1 # timestep in miliseconds for sampling the frames.
        extract_frames(vpath, step)
    
    print('All frames have been extracted. Removing the actual video files.')
    shutil.rmtree(save_path) # Remove the actual video files.
    print('Please wait...')
    while os.path.exists(save_path):
        pass # Wait for OS to synchronize.
    print('The video files have been deleted.')
    print('The program has finished. Outputs have been saved to: ./videos')
            
