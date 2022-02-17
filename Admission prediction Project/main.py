from flask import Flask, render_template, request, url_for
import pickle


lasso_model = pickle.load(open('lasso.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))

app = Flask(__name__)
@app.route('/home')
@app.route('/', methods = ['GET','POST'])
def home():
    if request.method == 'POST':
        GRE = request.form.get('GRE')
        TOEFL = request.form.get('TOEFL')
        UR = request.form.get('UR')
        SOP = request.form.get('SOP')
        LOR = request.form.get('LOR')
        CGPA = request.form.get('CGPA')
        Rese = request.form.get('Research')

    try:
        s_array = scaler.transform([[GRE,TOEFL,UR,SOP,LOR,CGPA,Rese]])
        pred = lasso_model.predict(s_array)[0]*100
        point = 1
    except:
        pred = "Plzz Fill Proper values!!!!!"
        point = 0
     
    return render_template('home.html', pred=pred, point=point)



if __name__=="__main__":
    app.run(debug=True)