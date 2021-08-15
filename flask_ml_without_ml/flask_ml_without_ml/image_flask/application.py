import codecs
import image_processor
import states
import SCORE
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("upload.html")
    else:
        image_file = request.files["fileToUpload"]
        file_name = secure_filename(image_file.filename)
        image_file.save("static/"+file_name)
        image_file.close()
        ascii_image_filename1 = "static/ascii_image1"
        ascii_image_filename2 = "static/ascii_image2"
        ascii_image_filename3 = "static/ascii_image3"
        ascii_image_filename4 = "static/ascii_image4"
        # ,ascii_image_filename3,ascii_image_filename4]
        ascii_image_filename = [ascii_image_filename1, ascii_image_filename2, ascii_image_filename3, ascii_image_filename4]
        emoji_list_index = sorted(
            SCORE.score.items(), key=lambda item: item[1], reverse=True)
        states.CURR_IDX = 0
        for count in range(states.MAX_IDX + 1):
            i = emoji_list_index[count]
            key = i[0]
            image_processor.process_image(
                "static/"+file_name, ascii_image_filename[count], key)
            states.CONTENT.append("NOTHING")
            with open(ascii_image_filename[count], "r") as f:
                states.CONTENT[count] = f.read()
                f.close()
        choice = request.args.get('selection')
        SCORE.score[states.CURR_IDX] += (1 if choice == 'yes' else -1)
        # for i in range(4):
        #     print("ascii_file_name",ascii_image_filename[i])
        #     image_processor.process_image("static/"+file_name, ascii_image_filename[i],i)
        #     states.CONTENT.append( "NOTHING")
        #     with open(ascii_image_filename[i], "r") as f:
        #         states.CONTENT[i] = f.read()
        #         f.close()
        return render_template("display_ascii.html", content=states.CONTENT[states.CURR_IDX])


@app.route('/change-image', methods=['GET'])
def change_image():
    choice = request.args.get('selection')
    SCORE.score[states.CURR_IDX] += (1 if choice == 'yes' else -1)
    # TODO: implement choice logic
    states.CURR_IDX += 1
    if states.CURR_IDX > states.MAX_IDX:
        states.CURR_IDX = 0
    return render_template("display_ascii.html", content=states.CONTENT[states.CURR_IDX])

# 0. Meaningful variable names -> Comments lie, code doesn't
# 1. KISS = Keep it short and simple
# # 2. DRY = Don't repeat yourself
# # 3. YAGNI = You ain't gonna need it

# def say_hi():
#     return "hi"

# def say_hello():
#     return "hello"

# def talk(what_to_say):
#     return what_to_say

# <5-15-20 lines 