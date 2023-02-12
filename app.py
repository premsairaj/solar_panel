from flask import Flask,render_template,url_for,request,redirect
import base64
from modelcode import models
app=Flask(__name__)

@app.route('/',methods=['POST','GET'])
def passing_data():
    if(request.method=='POST'):
        if(request.files['filename'].filename==''):
            inputvariable=dict(request.form)
            inst1=models.deploymentsetup()
            indepen_data=inst1.piplinestepuptest(inputvariable)
            resultstring = inst1.results(indepen_data)[0].to_html().encode('utf-8').decode('utf-8')
            return render_template('input.html',result_table=resultstring,note=str(inst1.results(indepen_data)[1]))

        else:
           inst1=models.deploymentsetup()
           resultstring=inst1.filepre_processing(request.files['filename'])[0].to_html().encode('utf-8').decode('utf-8')
           return render_template('input.html',result_table=resultstring)
    else:
        return render_template('input.html')

if __name__=='__main__':
    app.run(debug=True)