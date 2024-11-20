import subprocess
import csv
import os
import time
import asyncio
import aiohttp


from settings import (
    input_dir,
    output_dir,
    logger
)

# - - - -- - - - -
# start checking input dir
# - - - - - - - - -
def check_load_folder():
    instruction_file = os.path.join(input_dir, 'loading_instructions.csv')
    cookies_file = os.path.join(input_dir, 'youtube.com_cookies.txt')

    print(f"Watching for file: {instruction_file}")
    while True:
        if os.path.exists(instruction_file):
            logger.info("File exists! Processing...")
            asyncio.run(process_csv_async(instruction_file, cookies_file))
        else:
            logger.info("File not found. Checking again in 2 seconds...")

        time.sleep(2)

# - - - - - - - - -
# Download MP4 with yt-dlp (Async)
# - - - - - - - - -
async def download_mp4_async(
    url: str,
    save_directory: str,
    file_id: str,
    session: aiohttp.ClientSession,
    cookies_file
):
    try:
        logger.info(f"Downloading MP4 from: {url}")

        mp4_output_path = os.path.join(save_directory, f"{file_id}.mp4")
        logger.info(f"Downloading first 30 seconds to: {mp4_output_path}")


        video_format = 137
        audio_format = 251
        download_command = [
            "yt-dlp",
            url,
            "--downloader", "ffmpeg",  # Use ffmpeg for downloading
            "--downloader-args", "ffmpeg:-t 30",  # Limit download to first 30 seconds
            "-f", f"{video_format}+{audio_format}",  # Select video and audio formats
            "--merge-output-format", "mp4",  # Merge into an MP4 file
            "-o", mp4_output_path,  # Output the .mp4 file
            "--add-header", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        ]

        if cookies_file:
            download_command.extend(["--cookies", cookies_file])

        process = await asyncio.create_subprocess_exec(*download_command)

        await process.communicate()

        if process.returncode == 0:
            logger.info(f"File saved: {mp4_output_path}")
            return mp4_output_path
        else:
            raise subprocess.CalledProcessError(process.returncode, download_command)

    except (subprocess.CalledProcessError, Exception) as e:
        logger.error(f"Failed to download {url}: {e}")
        return None

# - - - - - - - - -
# Process CSV File (Async)
# - - - - - - - - -
async def process_csv_async(file_path, cookies_file):
    try:
        tasks = []
        async with aiohttp.ClientSession() as session:
            with open(file_path, mode='r') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    file_id, url = row['id'], row['url']
                    tasks.append(download_mp4_async(
                            url=url,
                            save_directory=output_dir,
                            file_id=file_id,
                            session=session,
                            cookies_file=cookies_file)
                        )
            await asyncio.gather(*tasks)

        os.remove(file_path)
        logger.info(f"File '{file_path}' deleted.")
        if os.path.exists(cookies_file):
            os.remove(cookies_file)
            logger.info(f"Cookies file '{cookies_file}' deleted.")

    except Exception as e:
        logger.error(f"Error processing file: {e}")


if __name__ == '__main__':
    check_load_folder()
