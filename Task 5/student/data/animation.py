
# Generate animations 
from matplotlib import animation
from matplotlib.animation import writers, FFMpegWriter
import matplotlib.pyplot as plt
import pickle
from IPython.display import HTML
import matplotlib.cbook as cbook
from skimage import io
import os
import argparse
import sys, math


def generate_video(p_file, ffmpeg_path, lama_images_path='../images'):
    # Unpickle
    infile = open(p_file,'rb')
    best_individuals = pickle.load(infile)
    generations = len(best_individuals)
    output_name = os.path.splitext(p_file)[0] + '.mp4'
    infile.close()

    print("Loaded Pickle start animating now ...")

    plt.rcParams['animation.ffmpeg_path'] = os.path.join(ffmpeg_path)

    # Set up formatting for the movie files
    writer = animation.writers['ffmpeg']
    writer = FFMpegWriter(fps=15, metadata=dict(artist='Me'), bitrate=1800)

    fig = plt.figure()
    fig.set_dpi(100)
    fig.set_size_inches(7, 6.5)
    fig.set_label("Your LAMA cage")

    ax = plt.axes(xlim=(0, 1000), ylim=(0, 1000))

    lama1 = [100,100,300,320]
    lama2 = [280,600,250,310]
    lama3 = [630,320,300,320]

    ground_truth = [
        plt.Rectangle((lama[0], lama[1]), lama[2], lama[3], fill=False, linestyle='--') 
        for lama in [lama1, lama2, lama3]
    ]
    [ax.add_patch(rect) for rect in ground_truth]

    # Generation counter label 
    generation_label = ax.text(600,950, "Generation: 0", fontsize=12)

    max_frames = int((generations * 8000) ** (1./3.)) + 1

    matplot_images = []

    for lama_image in ["lama{}.jpg".format(x) for x in range(1,4)]:
        datafile = cbook.get_sample_data(os.path.join(os.getcwd(), lama_images_path, lama_image))
        img = io.imread(datafile)
        image = plt.imshow(img, zorder=0, extent=[0, 0, 0, 0], animated=True)
        matplot_images.append(image)


    def init_animation():
        return []

    def animate(i):
        state = best_individuals[int((i*i*i)/8000)]
        return_set = []
        
        generation_label.set_text("Generation: {}".format(int((i*i*i)/8000)))
        
        for idx, image in enumerate(matplot_images):
            image.set_extent([state[idx * 4 + 0], state[idx * 4 + 0] + state[idx * 4 + 2], 
                            state[idx * 4 + 1], state[idx * 4 + 1] + state[idx * 4 + 3]])
            return_set.append(image)
                                        
        return_set.append(generation_label)

        draw_progressBar('Frames', i, max_frames)
                                        
        return return_set

    anim = animation.FuncAnimation(fig, animate, init_func=init_animation,
                                frames=int((float(generations))**(1./3.)*20), interval=60, blit=True)
    anim.save(output_name, writer=writer)

###  From: https://stackoverflow.com/questions/6169217/replace-console-output-in-python
def draw_progressBar(name, value, endvalue, comment="", bar_length=50, width=20):
    percent = float(value) / endvalue
    arrow = '-' * int(round(percent*bar_length) - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))
    sys.stdout.write("\r{0: <{1}} : [{2}] {3}% ({4}/{5}) {6:<30}".format(
        name, width, arrow + spaces, int(round(percent*100)), value, endvalue, comment))
    sys.stdout.flush()

    if value == endvalue:
        sys.stdout.write('\n\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, help="pickle file")
    parser.add_argument('--with-ffmpeg', type=str, help="ffmpeg path")
    args = parser.parse_args()
    
    generate_video(args.file, args.with_ffmpeg)