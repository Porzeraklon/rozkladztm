#TODO LIST
#1. Zmien to logo cepie - DONE
#2. Dodaj lapka - DONE
#3. Rozklad lini a nie przystanku
#4. Dodanie linków (rozklad lini itp.)
#5. Dodaj adsense
#6. Nie wygladanie jak gowno



from flask import Flask, flash, redirect, session, url_for, render_template, request
from datetime import date
from requests import get
from json import loads


app = Flask(__name__)
app.secret_key = "1234"

today = date.today()
today = today.strftime("%Y-%m-%d")
        

@app.route("/", methods=['POST', 'GET'])
def home():

    if request.method == "GET":
        
        zone_list = []
        zone_list_fix = []
        stops = get('https://ckan.multimediagdansk.pl/dataset/c24aa637-3619-4dc2-a171-a23eec8f2172/resource/4c4025f0-01bf-41f7-a39f-d156d201b82b/download/stops.json').text
        response_stops = loads(stops)
        for data in response_stops[today]['stops']:
            if data['zoneName'] != None:
                zone_list.append(data['zoneName'])
        zone_list_fix = set(zone_list)
        zone_list_fix = zone_list_fix.sort()
        return render_template("zone.html", zone_list=zone_list_fix)

    if request.method == "POST":
        zone = request.form["zone"]
        return redirect(url_for('zone_site', zone=zone))

@app.route("/<zone>", methods=['POST', 'GET'])
def zone_site(zone):
    
    if request.method == "GET":

        stops_list = []
        stops = get('https://ckan.multimediagdansk.pl/dataset/c24aa637-3619-4dc2-a171-a23eec8f2172/resource/4c4025f0-01bf-41f7-a39f-d156d201b82b/download/stops.json').text
        response_stops = loads(stops)
             

        for data in response_stops[today]['stops']:
            if data['stopName'] != None and data['stopCode'] != None and str(data['zoneName']).lower() == str(zone).lower():
                stop_name = data['stopName']
                stop_code = data['stopCode']
                stop_name = str(stop_name) + ' ' + str(stop_code)
                stops_list.append(stop_name)
        return render_template("index.html", stops_list=stops_list)

    
    if request.method == "POST":

        stop_name = request.form["stop"]
        stop_len = len(stop_name)
        stop_code = str(stop_name[int(stop_len) - 2]) + str(stop_name[int(stop_len) - 1])
        stop = stop_name[:-3:]
        
        stops = get('https://ckan.multimediagdansk.pl/dataset/c24aa637-3619-4dc2-a171-a23eec8f2172/resource/4c4025f0-01bf-41f7-a39f-d156d201b82b/download/stops.json').text
        response_stops = loads(stops)
        for data in response_stops[today]['stops']:
            if str(data['stopName']).lower() == str(stop).lower() and str(data['zoneName']).lower() == str(zone).lower():
                if str(data['stopCode']) == stop_code:
                    stop = data['stopId']
        
        return redirect(url_for('schedule', stop=stop, zone=zone))

@app.route("/<zone>/<stop>")
def schedule(stop, zone):

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
        delay_rest = ''
        delay_status = 'Brak opóźnień'
        if delay != None:     
   
            if delay < 0:
                delay_status = 'Przyśpieszenie: '
                delay = -delay + 1
                delay_rest = int(delay) % 60
                delay = int(delay) - int(delay_rest)
                delay = int(delay) / 60
                delay = (int(delay))
                delay = str(delay) + ' min ' + str(delay_rest) + ' s'
            elif delay < 60 and delay > 0:
                delay_status = 'Opóźnienie: '
                delay = '0 min ' + str(delay) + ' s'
            elif delay == 60:
                delay_status = 'Opóźnienie: '
                delay = '1 min 0 s'
            elif delay > 60:
                delay_status = 'Opóźnienie: '
                delay_rest = int(delay) % 60
                delay = int(delay) - int(delay_rest)
                delay = int(delay) / 60
                delay = (int(delay))
                delay = str(delay) + ' min ' + str(delay_rest) + ' s'
        else:
            delay = ''
        headsign = data['headsign']
        route = data['routeId']
        route = str(route)
        if int(route) > 400 < 500:
            route_night_second = str(route[-1])
            route_night_first = str(route[-2])
            if route_night_first == '0':
                route = 'N' + str(route_night_second)
            else:
                route = 'N' + str(route_night_first) + str(route_night_second)
        status = data['status']
        if str(status) == 'REALTIME':
            status = 'W drodze'
        if str(status) == 'SCHEDULED':
            status = 'Zaplanowany'
        theoretical = data['theoreticalTime']
        estimated_time = int(estimated[11]) * 10 + int(estimated[12]) + 2
        if int(estimated_time) >= 24:
            estimated_time = int(estimated_time) - 24
        estimated = str(estimated_time) + str(estimated[13]) + str(estimated[14]) + str(estimated[15]) + str(estimated[16]) + str(estimated[17]) + str(estimated[18])
        theoretical_time = int(theoretical[11]) * 10 + int(theoretical[12]) + 2
        if int(theoretical_time) >= 24:
            theoretical_time = int(theoretical_time) - 24
        theoretical = str(theoretical_time) + str(theoretical[13]) + str(theoretical[14]) + str(theoretical[15]) + str(theoretical[16]) + str(theoretical[17]) + str(theoretical[18])
        

        flash('================================')
        flash(str(route))
        flash('Kierunek: ' + headsign)
        flash('Status: ' + status)
        flash('Przewidywany przyjazd: ' + estimated)
        flash(str(delay_status) + str(delay))
        flash('Planowany przyjazd: ' + theoretical)
        flash('================================')
            
    return render_template("stop.html", stop=stop_name, zone=zone)
        
        


if __name__ == "__main__":
    app.run(debug=True)