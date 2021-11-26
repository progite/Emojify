import codecs
import image_processor
import states
import score_tracker
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("upload.html")

    file_name = file_uploaded(request)
    rearrange_emoji_preferences(file_name)
    choice = request.args.get('selection')
    score_tracker.score[states.curr_idx] += (1 if choice == 'yes' else -1)
    return render_template("display_ascii.html", content=states.content[states.curr_idx])


@app.route('/change-image', methods=['GET'])
def change_image():
    choice = request.args.get('selection')
    score_tracker.score[states.curr_idx] += (1 if choice == 'yes' else -1)
    states.curr_idx += 1
    if states.curr_idx > states.max_idx:
        states.curr_idx = 0
    return render_template("display_ascii.html", content=states.content[states.curr_idx])


def file_uploaded(request):
    image_file = request.files["fileToUpload"]
    file_name = secure_filename(image_file.filename)
    image_file.save("static/"+file_name)
    image_file.close()
    return file_name


def rearrange_emoji_preferences(file_name):
    emoji_list_index = sorted(
        score_tracker.score.items(), key=lambda item: item[1], reverse=True)
    states.curr_idx = 0
    process_images(file_name, emoji_list_index)


def process_images(file_name, emoji_list_index):
    for count in range(states.max_idx + 1):
        emoji_list = emoji_list_index[count]
        emoji = emoji_list[0]
        image_processor.process_image(
            "static/"+file_name, states.ascii_image_filenames[count], emoji)
        states.content.append("NOTHING")
        with open(states.ascii_image_filenames[count], "r") as file:
            states.content[count] = file.read()
            file.close()
