from flask import Flask, render_template, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from werkzeug.utils import secure_filename
import os
import csv

def fetch(FN):
    def time(t):
        time = t
        y = t.strip().split(':')
        total = float(y[0])*3600+float(y[1])*60+float(y[2])
        return total/60

    if FN:
        with open(FN, encoding='utf-16') as csvf:
            content = csv.reader(csvf)
            members = dict()
            c = False
            last = None
            for row in content:
                if c:
                    k = row[0].split('\t')
                    if k[1] == 'Joined':
                        if k[0] not in members:
                            members[k[0]] = [row[-1], 0, True]
                        else:
                            members[k[0]][0] = row[-1]
                            members[k[0]][2] = True
                    elif k[1] == 'Left':
                        if k[0] not in members:
                            members[k[0]] = [None, time(row[-1]), False]
                        else:
                            members[k[0]][1] = members[k[0]][1] + time(row[-1])-time(members[k[0]][0])
                            members[k[0]][2] = False
                c = True       
                last = row[-1]

            for key in members:
                if members[key][2]:
                    members[key][1] = members[key][1] + time(last) - time(members[key][0])
            
            res = list()
            
            for i in sorted(members.items(), key=lambda v:v[1][1], reverse=True):
                res.append([i[0],str(round(i[1][1],2))])

        csvf.close()
    return res

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Shhh...'
app.config['UPLOADS_FOLDER'] = os.path.join(APP_ROOT,'uploads')

class CsvUpload(FlaskForm):
    fileinput = FileField('ATTACH ATTENDANCE CSV', validators=[FileRequired(), FileAllowed(['csv'], 'Only .csv files are allowed!')])
    upload = SubmitField('UPLOAD CSV')

res = None
@app.route('/', methods=['GET','POST'])
def home():
    disp_table = False
    csv_form = CsvUpload()
    f = csv_form.fileinput.data
    res = []
    if csv_form.validate_on_submit():
        filename = secure_filename(f.filename)
        filename_str = os.path.join(app.config['UPLOADS_FOLDER'], f'{filename}')
        if not os.path.exists(app.config['UPLOADS_FOLDER']):
            os.makedirs(app.config['UPLOADS_FOLDER'])
        f.save(filename_str)
        res = fetch(filename_str)
        disp_table = True

    return render_template('home.html', res=res, res_len=range(len(res)), form=csv_form, formsub=disp_table, url_for=url_for)

port = int(os.environ.get('PORT', 5000))

if __name__ == '__main__':
	app.run(threaded=True, port=port)

