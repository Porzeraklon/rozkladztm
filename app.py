from flask import Flask, flash, redirect, session, url_for, render_template, request

app = Flask(__name__)
app.secret_key = "1234"

@app.route("/", methods=['POST', 'GET'])
def home():
    

    if request.method == "POST":
        
        return render_template("index.html")

    

    
    if request.method == "GET":
        #PAMIETAJ CEPIE ZEBY POST I GET ZMIENIC

        #stop = request.form['stop']
        #stop_len = len(stop)
        #stop_len = int(stop_len) - 1 
        #stop_len_b = int(stop_len) - 1
        #stop_nr = str(stop[stop_len_b]) + str(stop[stop_len])
        #i = 0
        #while i < stop_len - 2:
        #    stop_final = stop[i]
        #stops = get('https://ckan.multimediagdansk.pl/dataset/c24aa637-3619-4dc2-a171-a23eec8f2172/resource/4c4025f0-01bf-41f7-a39f-d156d201b82b/download/stops.json').text
        #response_stops = loads(stops)
        #for one in response_stops:
        #    if one['stopName'] == stop_final:
        #        if one['stopCode'] == stop_nr:
        #            stop = one['stopId']
        #            print(stop)
        
        return render_template("index.html")
        
        
@app.route("/<stop>")
def schedule(stop):
    from datetime import date
    from requests import get
    from json import loads

    today = date.today()
    today = today.strftime("%Y-%m-%d")

    stops = get('https://ckan.multimediagdansk.pl/dataset/c24aa637-3619-4dc2-a171-a23eec8f2172/resource/4c4025f0-01bf-41f7-a39f-d156d201b82b/download/stops.json').text
    response_stops = loads(stops)
    for data in response_stops[today]['stops']:
        if data['stopId'] == int(stop):
            stop_name = data['stopName']
            stop_code = data['stopCode']
            stop_name = str(stop_name) + ' ' + str(stop_code)

    routs = get('https://ckan2.multimediagdansk.pl/departures?stopId=' + str(stop)).text
    response_routs = loads(routs)
    for data in response_routs['departures']:
        _id = data['id']
        estimated = data['estimatedTime']
        delay = data['delayInSeconds']
        headsign = data['headsign']
        route = data['routeId']
        status = data['status']
        theoretical = data['theoreticalTime']
        estimated_time = int(estimated[11]) * 10 + int(estimated[12]) + 2
        if int(estimated_time) >= 24:
            estimated_time = int(estimated_time) - 24
        estimated = str(estimated_time) + str(estimated[13]) + str(estimated[14]) + str(estimated[15]) + str(estimated[16]) + str(estimated[17]) + str(estimated[18])
        theoretical_time = int(theoretical[11]) * 10 + int(theoretical[12]) + 2
        if int(theoretical_time) >= 24:
            theoretical_time = int(theoretical_time) - 24
        theoretical = str(theoretical_time) + str(theoretical[13]) + str(theoretical[14]) + str(theoretical[15]) + str(theoretical[16]) + str(theoretical[17]) + str(theoretical[18])
        delay_rest = ''
        if str(delay) != 'None':
            delay_rest = int(delay) % 60
            delay = int(delay) - int(delay_rest)
            delay = int(delay) / 60
            delay = (int(delay))

        flash('================================')
        flash('Autobus nr: ' + str(route))
        flash('Kierunek: ' + headsign)
        flash('Planowany odjazd: ' + theoretical)
        flash('Opoźnienie: ' + str(delay) + 'min ' + str(delay_rest) + 's')
        flash('Przewidywany odjazd: ' + estimated)
        flash('================================')
        return render_template("stop.html", stop=stop_name)
        
            
        
        


if __name__ == "__main__":
    app.run(debug=True)