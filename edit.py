from moviepy.editor import * 
import moviepy.config as moviepyconf
from moviepy.video.fx.all import fadein, fadeout, rotate
from moviepy.video.tools.subtitles import SubtitlesClip  
import random
import os
import threading

# Cài đặt đường dẫn cho công cụ ImageMagick
moviepyconf.IMAGEMAGICK_BINARY = r'D:\Apps\ImageMagick-7.1.1-Q16-HDRI\magick.exe'

class VideoEditor:
    def __init__(self, video_path):
        self.video = VideoFileClip(video_path)
 
    # Cắt video từ thời điểm bắt đầu đến thời điểm kết thúc
    def cut(self, start_time, end_time):
        self.video = self.video.subclip(start_time, end_time)
        return self.video
        
    # Thay đổi kích thước của video
    def resize(self, width, height):
        self.video = self.video.resize(width, height) 
        return self.video
    
    # Tăng tốc độ của video theo hệ số
    def speedx(self, factor):
        self.video = self.video.fx(vfx.speedx, factor)
        return self.video
    
    # Đóng video
    def close(self):
        self.video.close()

    # Lấy thời lượng của video
    def get_duration(self):
        return self.video.duration
    
    # Chỉnh sửa màu sắc của video
    def edit_color(self, saturation=None, contrast=None, brightness=None):
        if saturation is not None:
            self.video = self.video.fx(vfx.colorx, saturation=saturation)
        if contrast is not None:
            self.video = self.video.fx(vfx.colorx, contrast=contrast)
        if brightness is not None:
            self.video = self.video.fx(vfx.colorx, brightness=brightness)
        return self.video
    
    # Xoay hoặc lật video
    def rotate_flip(self, rotation=None, flip='vertical'):
        if rotation is not None:
            self.video = self.video.rotate(rotation)
        if flip == 'vertical':
            self.video = self.video.fx(vfx.mirror_y)
        elif flip == 'horizontal':
            self.video = self.video.fx(vfx.mirror_x)
        return self.video

    # Chuyển đổi định dạng của video và lưu vào đường dẫn đích
    def convert_format(self, output_format='mp4'):
        output_path = "converted_video." + output_format
        self.video.write_videofile(output_path)
        return output_path
    
    # Chèn hình ảnh vào video
    def add_image(self, image_path, start_img=0, end_img=None, x='center', y='center', width_img=None, height_img=None):
        if end_img is None:
            end_img = self.video.duration
        if width_img is None:
            width_img = self.video.size[0]
        if height_img is None:
            height_img = self.video.size[1]
        image = ImageClip(image_path)
        image = image.set_duration(end_img - start_img)
        image = image.set_start(start_img)
        image = image.resize(width=width_img, height=height_img)
        image = image.set_position((x, y))
        self.video = CompositeVideoClip([self.video, image])
        return self.video
    
    # Chèn văn bản vào video
    def add_text(self, text, start_time=0, end_time=None, x='center', y='center',color='black',fontsize=70,bg_color='white',font='Arial'):
        if end_time is None:
            end_time = self.get_duration() 
        text = TextClip(text, fontsize=fontsize, color=color,font=font, bg_color=bg_color)
        text = text.set_duration(end_time - start_time)
        text = text.set_start(start_time)
        text = text.set_position((x, y)) 
        self.video = CompositeVideoClip([self.video, text])
        return self.video
    
    
    # Chèn phụ đề vào video
    def add_subtitle(self, srt_text,  x='center', y='center', font='Arial', fontsize=24, color='white'):
        generator = lambda txt: TextClip(txt, font=font, fontsize=fontsize, color=color)
        subtitles = SubtitlesClip(srt_text, generator)
        subtitles = subtitles.set_position((x,y))
        self.video = CompositeVideoClip([self.video, subtitles])
        return self.video

    # Chèn âm thanh vào video
    def add_audio(self, audio_path, start_audio=0, end_audio=None, volume=1,start_video=0, end_video=None):
        if end_audio is None:
            end_audio = self.get_duration()
        if end_video is None:
            end_video = self.get_duration()
        audio = AudioFileClip(audio_path)
        audio = audio.subclip(start_audio, end_audio)
        audio = audio.volumex(volume)
        audio = audio.set_start(start_video)
        audio = audio.set_duration(end_video - start_video)
        self.video = self.video.set_audio(audio)
        return self.video
     
    # Trích xuất âm thanh từ video
    def get_audio(self, audio_path='audio.mp3',download=False):
        audio = self.video.audio
        if download:
            audio.write_audiofile(audio_path) 
        return audio
    
    # tắt âm thanh của video
    def mute(self):
        self.video = self.video.set_audio(None)
        return self.video
    
    # Chèn video vào video hiện tại
    def add_in_video(self, video_path, start_time=0, end_time=None, x='center', y='center', width=None, height=None):
        if end_time is None or end_time > self.get_duration():
            end_time = self.get_duration()
        
        if width is None:
            width = self.video.size[0]
        if height is None:
            height = self.video.size[1]

        video = VideoFileClip(video_path)
        video_duration = min(video.duration, end_time - start_time)
        video = video.subclip(0, video_duration)
        video = video.resize(width=width, height=height)
        video = video.set_position((x, y))
        
        self.video = CompositeVideoClip([self.video, video])
        return self.video

    # Nối video với video khác
    def concatenate(self, video_path):
        video = VideoFileClip(video_path)
        self.video = concatenate_videoclips([self.video, video])
        return self.video
    
    # Thêm hiệu ứng vào video
    def fx(self, fx, *args, **kwargs):
        self.video = self.video.fx(fx, *args, **kwargs)
        return self.video
    
    # Tạo hiệu ứng di chuyển cho hình ảnh
    def animate_image(self, image_path, start_time=0, end_time=None, x1='center', y1='center', x2='center', y2='center', width_img=None, height_img=None):
        if end_time is None:
            end_time = self.get_duration()
        if width_img is None:
            width_img = self.video.size[0]
        if height_img is None:
            height_img = self.video.size[1]
         
        dict_x = {
            "center": self.video.size[0] / 2-width_img/2,
            "left": 0,
            "right": self.video.size[0]-width_img
        }
        dict_y = {
            "center": self.video.size[1] / 2- height_img/2,
            "top": 0,
            "bottom": self.video.size[1]- height_img
        }
        
        if isinstance(x1, str):
            x1 = dict_x[x1]
        if isinstance(y1, str):
            y1 = dict_y[y1]
        if isinstance(x2, str):
            x2 = dict_x[x2]
        if isinstance(y2, str):
            y2 = dict_y[y2]  
        
        image = ImageClip(image_path)
        image = image.set_duration(end_time - start_time)
        image = image.set_start(start_time)
        image = image.resize(width=width_img, height=height_img)
         
        dx = (x2 - x1) / (end_time - start_time)
        dy = (y2 - y1) / (end_time - start_time)
         
        def update_position(t):
            x = x1 + dx * t
            y = y1 + dy * t
            return x, y
         
        image = image.set_position(update_position) 
        self.video = CompositeVideoClip([self.video, image])
        return self.video
    
    # Lưu video
    def save(self, output_path):
        self.video.write_videofile(output_path)
        return self.video
    
    # Làm nét video
    def sharpen(self, factor):
        self.video = self.video.fx(vfx.sharpen, factor)
        return self.video

    # Làm mờ video
    def blur(self, factor):
        self.video = self.video.fx(vfx.blur, factor)
        return self.video

    # Thêm hiệu ứng đậm dần vào và ra của video
    def fade_in_out(self, duration):
        fade_in = self.video.fadein(duration)
        fade_out = self.video.fadeout(duration)
        self.video = concatenate_videoclips([fade_in, self.video, fade_out])
        return self.video

    # Thay đổi âm lượng của video
    def change_volume(self, volume):
        self.video = self.video.volumex(volume)
        return self.video

    # Chuyển đổi sang video trắng đen
    def black_and_white(self):
        self.video = self.video.fx(vfx.blackwhite)
        return self.video

    # Trích xuất các khung hình từ video
    def extract_frames(self, fps, output_path):
        return self.video.write_images_sequence(output_path, fps=fps)

    # Đảo ngược video
    def reverse(self):
        self.video = self.video.fx(vfx.time_mirror)
        return self.video

    # Phóng to hoặc thu nhỏ video
    def zoom(self, factor):
        self.video = self.video.fx(vfx.zoom, factor)
        return self.video

    # Cắt video
    def crop(self, x1, x2, y1, y2):
        self.video = self.video.fx(vfx.crop, x1=x1, x2=x2, y1=y1, y2=y2)
        return self.video
    
    # Làm đóng băng một phần của video
    def freeze(self, duration):
        freeze = self.video.to_ImageClip(t=0)
        freeze = freeze.set_duration(duration)
        freeze = freeze.set_start(0)
        self.video = CompositeVideoClip([freeze.set_position('center'), self.video])
        return self.video
    
    # Lặp lại video
    def loop(self, n):
        self.video = self.video.fx(vfx.loop, n)
        return self.video
    
    # Đặt số khung hình trên giây cho video
    def set_fps(self, fps):
        self.video = self.video.set_fps(fps)
        return self.video
    
    # Đặt thời lượng cho video
    def set_duration(self, duration):
        self.video = self.video.set_duration(duration)
        return self.video
    
    # Đặt thời điểm bắt đầu cho video
    def set_start(self, start_time):
        self.video = self.video.set_start(start_time)
        return self.video
    
    # Đặt thời điểm kết thúc cho video
    def set_end(self, end_time):
        self.video = self.video.set_end(end_time)
        return self.video
    
    # Đặt vị trí của video
    def set_position(self, x, y):
        self.video = self.video.set_position((x, y))
        return self.video
    
    # Cắt và thu nhỏ video
    def resize_crop(self, width, height, x_center=True, y_center=True):
        self.video = self.video.crop(x_center=x_center, y_center=y_center).resize(width=width, height=height)
        return self.video
    
    # Tăng tốc độ video
    def speed_up(self, factor):
        self.video = self.video.fx(vfx.speedx, factor)
        return self.video
    
    # Giảm tốc độ video
    def speed_down(self, factor):
        self.video = self.video.fx(vfx.speedx, 1/factor)
        return self.video
    
    # Giảm nhiễu của video
    def reduce_noise(self):
        self.video = self.video.fx(vfx.reduce_noise)
        return self.video
    
    # Phản chiếu video theo trục
    def mirror(self, axis):
        if axis == 'x':
            self.video = self.video.fx(vfx.mirror_x)
        elif axis == 'y':
            self.video = self.video.fx(vfx.mirror_y)
        else:
            self.video = self.video.fx(vfx.mirror_x).fx(vfx.mirror_y)
        return self.video

    # Thêm hiệu ứng đậm dần vào và ra của video
    def fade_in_out(self, fade_in_duration, fade_out_duration):
        self.video = fadein(self.video, fade_in_duration)
        self.video = fadeout(self.video, fade_out_duration)
        return self.video

    # Xoay video
    def rotate(self, angle):
        self.video = rotate(self.video, angle)
        return self.video

    # Chia video thành n phần
    def split(self, n):
        duration = self.video.duration / n
        videos = []
        for i in range(n):
            start_time = i * duration
            end_time = (i + 1) * duration
            video = self.video.subclip(start_time, end_time)
            videos.append(video)
        return videos
    
    # Chọn ngẫu nhiên một phần của video
    def random_part(self, duration):
        start_time = random.randint(0, self.video.duration - duration)
        end_time = start_time + duration
        return self.video.subclip(start_time, end_time)
    
    # Chia nhỏ video thành các khung hình 
    def split_frames(self, fps):
        return self.video.iter_frames(fps=fps)
    
    # Chuyển đổi video thành mảng các khung hình
    def to_frames(self, fps):
        return list(self.video.iter_frames(fps=fps))
    
    # 
    
class Audio:
    def __init__(self, audio_path):
        self.audio = AudioFileClip(audio_path)
    
    # Cắt audio từ thời điểm bắt đầu đến thời điểm kết thúc
    def cut(self, start_time, end_time):
        self.audio = self.audio.subclip(start_time, end_time)
        return self.audio
    
    # Tăng tốc độ của audio theo hệ số
    def speedx(self, factor):
        self.audio = self.audio.fx(vfx.speedx, factor)
        return self.audio
    
    # Đóng audio
    def close(self):
        self.audio.close()
    
    # Lấy thời lượng của audio
    def get_duration(self):
        return self.audio.duration
    
    # Chuyển đổi định dạng của audio và lưu vào đường dẫn đích
    def convert_format(self, output_format='mp3'):
        output_path = "converted_audio." + output_format
        self.audio.write_audiofile(output_path)
        return output_path
    
    # Thêm hiệu ứng vào audio
    def fx(self, fx, *args, **kwargs):
        self.audio = self.audio.fx(fx, *args, **kwargs)
        return self.audio
    
    # Lưu audio
    def save(self, output_path):
        self.audio.write_audiofile(output_path)
        return self.audio
    
    # Thay đổi âm lượng của audio
    def change_volume(self, volume):
        self.audio = self.audio.volumex(volume)
        return self.audio
    
    # Thêm hiệu ứng đậm dần vào và ra của audio
    def fade_in_out(self, duration):
        fade_in = self.audio.fadein(duration)
        fade_out = self.audio.fadeout(duration)
        self.audio = concatenate_audioclips([fade_in, self.audio, fade_out])
        return self.audio
    
    # Tách audio từ video
    def from_video(self, video_path):
        video = VideoFileClip(video_path)
        self.audio = video.audio
        return self.audio
    
    # Làm nét audio
    def sharpen(self, factor):
        self.audio = self.audio.fx(vfx.sharpen, factor)
        return self.audio

    # Làm mờ audio
    def blur(self, factor):
        self.audio = self.audio.fx(vfx.blur, factor)
        return self.audio
    
    # Tăng tốc độ audio
    def speed_up(self, factor):
        self.audio = self.audio.fx(vfx.speedx, factor)
        return self.audio
    
    # Giảm tốc độ audio
    def speed_down(self, factor):
        self.audio = self.audio.fx(vfx.speedx, 1/factor)
        return self.audio
    
    # Giảm nhiễu của audio
    def reduce_noise(self):
        self.audio = self.audio.fx(vfx.reduce_noise)
        return self.audio
    
    # Thêm hiệu ứng đậm dần vào và ra của audio
    def fade_in_out(self, fade_in_duration, fade_out_duration):
        self.audio = fadein(self.audio, fade_in_duration)
        self.audio = fadeout(self.audio, fade_out_duration)
        return self.audio
    
    # Chia audio thành n phần
    def split(self, n):
        duration = self.audio.duration / n
        audios = []
        for i in range(n):
            start_time = i * duration
            end_time = (i + 1) * duration
            audio = self.audio.subclip(start_time, end_time)
            audios.append(audio)
        return audios
    
    # Chọn ngẫu nhiên một phần của audio
    def random_part(self, duration):
        start_time = random.randint(0, self.audio.duration - duration)
        end_time = start_time + duration
        return self.audio.subclip(start_time, end_time)