import json
import ffmpeg

class Video:
    def __init__(self, trim_list:list, path:str) -> None:
        self.trim_list = trim_list
        self.segments = len(trim_list)
        self.path = "inputs/" + path
    
    def __str__(self):
        print(self.trim_list)
    
    def trim(self):
        print("trim video...")
        number = 0
        for segment in self.trim_list:
            output_path = 'inputs/trims/video{}.mp4'.format(number)
            (
            ffmpeg
            .input(self.path, ss=segment, t="00:00:20")
            .output(output_path, codec='copy')
            #.global_args('-report')
            .global_args('-loglevel', 'error')
            .global_args('-y')
            .run()
            )
            number +=1



def concat_video(video:Video):
    print(f"concat video {video.segments} parts...")
    streams = []
    for x in range(video.segments):
        streams.append(ffmpeg.input(f'inputs/trims/video{x}.mp4').video)
        streams.append(ffmpeg.input(f'inputs/trims/video{x}.mp4').audio)
    output_path = 'output/videoFinal.mp4'
    joined = ffmpeg.concat(*streams,v=1, a=1).node
    (
        ffmpeg
        .output(joined[0], joined[1], output_path)
        .global_args('-y')
        #.global_args('-report')
        .global_args('-loglevel', 'error')
        .run()
    )

data:dict = None
with open("info.json") as f:
    data = json.load(f)

videos:list[Video] = []
for file, time_list in data.items():
    videos.append(Video(time_list, path=file))

for video in videos:
    print(video)
    video.trim()
    concat_video(video)
