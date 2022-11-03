# Joan Bosco Olives Florit  NIA: 217056
import os
import subprocess


def relevant_data(path):
    """
    Return 4 relevant data from container. For any case, we extract the information with ffprobe command
    and save the information in string variable with subprocess.check_output command
    :param path: path of video
    :return: None return, only relevant data information in PRINT format
    """
    wxh = subprocess.check_output('ffprobe -v error -select_streams v -show_entries stream=width,height -of '
                                  'csv=p=0:s=x ' + path, stderr=subprocess.STDOUT, shell=True)

    # https://stackoverflow.com/questions/33699091/ffprobe-to-get-codec
    video_codec = subprocess.check_output('ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of '
                                          'default=noprint_wrappers=1:nokey=1 ' + path, stderr=subprocess.STDOUT,
                                          shell=True)

    audio_codec = subprocess.check_output('ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of '
                                          'default=noprint_wrappers=1:nokey=1 ' + path, stderr=subprocess.STDOUT,
                                          shell=True)

    audio_br = subprocess.check_output('ffprobe -v error -select_streams a:0 -show_entries stream=bit_rate -of '
                                       'default=noprint_wrappers=1:nokey=1 ' + path, stderr=subprocess.STDOUT,
                                       shell=True)
    string_replace = str(r"\r\n'")  # string to replace (subprocess return string with some undesirable characters)
    wxh = str(wxh)
    wxh = wxh.replace("b'", '')
    wxh = wxh.replace(string_replace, '')

    video_codec = str(video_codec)
    video_codec = video_codec.replace("b'", '')
    video_codec = video_codec.replace(string_replace, '')

    audio_codec = str(audio_codec)
    audio_codec = audio_codec.replace("b'", '')
    audio_codec = audio_codec.replace(string_replace, '')

    audio_br = str(audio_br)
    audio_br = audio_br.replace("b'", '')
    audio_br = audio_br.replace(string_replace, '')

    print('Width x Height: ' + wxh)
    print('Video Codec: ' + video_codec)
    print('Audio Codec: ' + audio_codec)
    print('Audio Bitrate: ' + audio_br + ' bps')
    print()


def new_container(path):
    """
    from input video, first of all, export 1min input version, for later generate 2 different versions of
    these video, first with mp3 audio codec and the second to aac audio codec but with 1/2 of the original bitrate
    :param path: path input video
    :return: export 3 different videos: 1min cutted video and two versions of these but diferent audio codec format
    """
    # command used for cut video
    # https://superuser.com/questions/138331/using-ffmpeg-to-cut-up-video
    os.system('ffmpeg -ss 0 -i ' + path + ' -c copy -t 60 output_1min.mp4')

    # command used for change audio codec
    # https://ottverse.com/transcode-audio-codec-ffmpeg-without-changing-video/
    os.system('ffmpeg -i output_1min.mp4 -acodec mp3 -vcodec copy output_mp3.mp4')

    # get audio BIT RATE and store in variable 'audio_br'
    audio_br = subprocess.check_output('ffprobe -v error -select_streams a:0 -show_entries stream=bit_rate -of '
                                       'default=noprint_wrappers=1:nokey=1 ' + path, stderr=subprocess.STDOUT,
                                       shell=True)
    string_replace = str(r"\r\n'")
    audio_br = str(audio_br)
    audio_br = audio_br.replace("b'", '')
    audio_br = audio_br.replace(string_replace, '')
    audio_br = str(round(int(audio_br) / 2))
    # force audio codec AAC and change bitrate of half of the original
    os.system('ffmpeg -i output_1min.mp4 -acodec aac -vcodec copy -b:a ' + audio_br + ' output_aac.mp4')

    # Prints to show Audio codec of two videos outputs and respective bitrate
    print('Cutted 1min video MP3 stereo track')
    relevant_data('output_mp3.mp4')
    print('Cutted 1min video AAC w/ lower bitrate')
    relevant_data('output_aac.mp4')


def resize_video(path):
    """
    Generate a resize that you want, without any limitation, although it doesn't make much sense, visually speaking.
    Need 2 input int parameters Width and Height
    :param path: path input video
    :return: Export video with name WidthxHeight.mp4
    """
    w = input("Choose resize width format: \n")
    h = input("Choose resize height format: \n")
    resize_string = str(w + 'x' + h)
    print(resize_string)
    os.system('ffmpeg -i ' + path + ' -s ' + resize_string + ' -c:a copy ' + resize_string + '.mp4')


def check_audio_tracks(path):
    """
    These function check the audio track codec and return a print with specific information it will
    explain in which broadcasting standard the video can fit
    :param path: path input video
    :return: None return, only return information with PRINT format
    """
    audio_codec = subprocess.check_output('ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of '
                                          'default=noprint_wrappers=1:nokey=1 ' + path, stderr=subprocess.STDOUT,
                                          shell=True)
    string_replace = str(r"\r\n'")

    audio_codec = str(audio_codec)
    audio_codec = audio_codec.replace("b'", '')
    audio_codec = audio_codec.replace(string_replace, '')

    print('Audio Codec: ' + audio_codec)
    match audio_codec:
        case 'aac':
            print('AAC audio, that means it can be DVB, ISDB and DTMB')
        case 'mp3':
            print('AAC audio, that means it can be DVB and DTMB')
        case 'AC-3':
            print('AAC audio, that means it can be DVB, ATSC and DTMB')
        case 'mp2':
            print('AAC audio, that means it can be DTMB')
        case 'dra':
            print('AAC audio, that means it can be DTMB')


def main():
    path = "BBB.mp4"
    while True:
        n = input("1.- Relevant Data\n2.- MP3 vs. AAC\n3.- Resize Video\n4.- Broadcasting Standard\n5.- Exit\n")
        n = int(n)
        # menu with case's
        match n:  # match function only works in python 3.10 or superior
            case 1:
                print("Visualize Relevant Data Video File")
                relevant_data(path)

            case 2:
                print("MP3 vs. AAC w/ lower bitrate")
                new_container(path)

            case 3:
                print("Resize Video Choosed")
                resize_video(path)

            case 4:
                print("Broadcasting Standard")
                check_audio_tracks(path)
            case 5:
                print("Exit")
                return
            case _:
                print("You are introduced an invalid input, choose [1, 2, 3, 4 or 5 ]")
                main()


if __name__ == "__main__":
    main()
