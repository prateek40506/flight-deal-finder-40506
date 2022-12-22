from django.shortcuts import render, redirect

from django.contrib import messages
import requests
import mysql.connector

PASSWORD = "&SantroXing10"
from datetime import datetime, timedelta

now = datetime.now()
tomorrow_date = datetime.now() + timedelta(days=1)
late_date = tomorrow_date + timedelta(days=6 * 30)
tomorrow_date = tomorrow_date.strftime("%d/%m/%Y")
late_date = late_date.strftime("%d/%m/%Y")
SHEETY_URL = "https://api.sheety.co/4254c8a08f9e3954301901322721b43f/flightDealFinder/prices"
FLIGHT_IATACODE_SEARCH_ENDPOINT = "https://tequila-api.kiwi.com/locations/query"
FLIGHT_SEARCH_ENDPOINT = "https://tequila-api.kiwi.com/v2/search"
API_KEY = "NCBuBemOQPd9bPZtKqfdYzQC-fQ8UYF5"
header = {
    "apikey": API_KEY
}


class FlightSearch:
    def iatacode(self, city_name):
        search_query = {
            "term": city_name,
            "locale": "en-US",
            "location_types": "city",
            "limit": 1,
            "active_only": True
        }
        response = requests.get(url=FLIGHT_IATACODE_SEARCH_ENDPOINT, params=search_query, headers=header)
        response.raise_for_status()
        if len(response.json()["locations"]) != 0:
            return response.json()["locations"][0]["code"]
        else:
            return ""



def home(request):
    if request.method == "POST":
        if "logged_user" in request.session.keys():
            if request.session["logged_user"] != " ":
                response = requests.get(url=SHEETY_URL)
                response = response.json()["prices"]
                object_id = 2
                for city_record in response:
                    if city_record["iataCode"] == "":
                        flight_search = FlightSearch()
                        iata_code = flight_search.iatacode(city_record["city"])
                        req_body = {
                            "price": {
                                "iataCode": iata_code
                            }
                        }
                        sheety_put_endpoint = f"{SHEETY_URL}/{object_id}"
                        response = requests.put(url=sheety_put_endpoint, json=req_body)
                    object_id += 1
                return render(request, "form.html")
            else:
                messages.error(request, "Sign in first")
                return render(request, "signin.html")
        else:
            messages.error(request, "Sign in first")
            return render(request, "signin.html")

    logged_in_email = " "
    first_name = " "
    if "logged_user" in request.session.keys():
        if request.session["logged_user"] != " ":
            logged_in_email = request.session["logged_user"]
            conn = mysql.connector.connect(host="localhost", username="root", password=PASSWORD, database="flight_deal_finder")
            my_cursor = conn.cursor()
            my_cursor.execute("select full_name from user where email='{}'".format(logged_in_email))
            full_name = my_cursor.fetchone()
            if full_name:
                full_name = full_name[0]
                first_name = full_name.split(" ")[0]
    else:
        request.session["logged_user"] = " "
    context = {
        "logged_in_email": logged_in_email,
        "first_name": first_name
    }
    return render(request, "home.html", context)


def signup(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        email = request.POST["email"]
        password = request.POST["password"]
        conn = mysql.connector.connect(host="localhost", username="root", password=PASSWORD,
                                       database="flight_deal_finder")
        my_cursor = conn.cursor()
        my_cursor.execute("select email from user")
        user_mails = my_cursor.fetchall()
        my_cursor.close()
        for user_mail in user_mails:
            print(user_mail[0])
            if user_mail[0] == email:
                messages.error(request, "You are already registered, signin now!")
                return redirect("signin")
        conn = mysql.connector.connect(host="localhost", username="root", password=PASSWORD,
                                       database="flight_deal_finder")
        my_cursor = conn.cursor()
        sql = "insert into user values('{}', '{}', '{}', '{}')".format(email, password, full_name, 1)
        request.session["logged_user"] = email
        my_cursor.execute(sql)
        conn.commit()
        my_cursor.close()
        return redirect("home")
    return render(request, "signup.html")


def signin(request):
    if request.method == "POST":
        email = request.POST["email"]
        user_password = request.POST["password"]
        conn = mysql.connector.connect(host="localhost", username="root", password=PASSWORD,
                                       database="flight_deal_finder")
        my_cursor = conn.cursor()
        sql = "select * from user"
        my_cursor.execute(sql)
        user_records = my_cursor.fetchall()
        flag = 0
        for record in user_records:
            if record[0] == email and record[1] == user_password:
                my_cursor.execute("update user set is_logged_in=1 where email='{}'".format(email))
                request.session["logged_user"] = email
                flag = 1
                break
            elif record[0] == email and record[1] != user_password:
                messages.error(request, "Invalid login credentials")
                return render(request, "signin.html")
        if flag == 0:
            messages.error(request, 'Sign up first')
            return render(request, "signup.html")
        my_cursor.close()
        return redirect("home")
    return render(request, "signin.html")


def form(request):
    if request.method == "POST":
        res = requests.get(url=SHEETY_URL)
        res = res.json()["prices"]
        object_id = 2
        for city_record in res:
            if city_record["iataCode"] != "":
                flight_search = FlightSearch()
                iata_code = flight_search.iatacode(request.POST["fly-from"])
                adults = request.POST["adults"]
                children = request.POST["children"]
                search_params = {
                    "fly_from": iata_code,
                    "fly_to": city_record["iataCode"],
                    "date_from": request.POST["date-from"],
                    "date_to": request.POST["date-to"],
                    "nights_in_dst_from": request.POST["nights-from"],
                    "nights_in_dst_to": request.POST["nights-to"],
                    "flight_type": "round",
                    "adults": adults,
                    "children": children,
                    "max_stopovers": 0,
                    "vehicle_type": "aircraft",
                    "one_for_city": 1,
                    "curr": "INR"
                }
                response = requests.get(
                    url=FLIGHT_SEARCH_ENDPOINT,
                    headers=header,
                    params=search_params,
                )
                conn = mysql.connector.connect(host="localhost", username="root", password=PASSWORD, database="flight_deal_finder")
                my_cursor = conn.cursor()
                my_cursor.execute("insert into search_query values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(request.session["logged_user"], iata_code, city_record["iataCode"], request.POST["date-from"], request.POST["date-to"], request.POST["nights-from"], request.POST["nights-to"], adults, children, city_record["lowestPrice"]))
                conn.commit()
                my_cursor.close()
                try:
                    data = response.json()["data"][0]
                except IndexError:
                    print(f"No flights found for {city_record['city']}.")
                    continue
                price = data["price"]
                origin_city = data["route"][0]["cityFrom"],
                origin_airport = data["route"][0]["flyFrom"],
                destination_city = data["route"][0]["cityTo"],
                destination_airport = data["route"][0]["flyTo"],
                out_date = data["route"][0]["local_departure"].split("T")[0],
                return_date = data["route"][1]["local_departure"].split("T")[0]
                if price <= city_record["lowestPrice"]:
                    output_query = f"Plane flying from {origin_airport[0]}, {origin_city[0]} to {destination_airport[0]}, {destination_city[0]} from {out_date[0]} to {return_date} is available for {adults} adults and {children} children for Rs.{price}. It is a round trip with no layovers."
                    print(output_query)
                    conn = mysql.connector.connect(host="localhost", username="root", password=PASSWORD,
                                               database="flight_deal_finder")
                    my_cursor = conn.cursor()
                    my_cursor.execute("insert into dashboard values ('{}', '{}')".format(request.session["logged_user"], output_query))
                    conn.commit()
                    my_cursor.close()
                else:
                    print(f"No flights found for {city_record['city']}.")
            object_id += 1
        object_id = 2
        for _ in res:
            sheety_delete_endpoint = f"{SHEETY_URL}/{object_id}"
            result = requests.delete(url=sheety_delete_endpoint)
            object_id += 1
            print(result)
    return redirect("dashboard")


def logout(request):
    email = request.session["logged_user"]
    conn = mysql.connector.connect(host="localhost", username="root", password=PASSWORD, database="flight_deal_finder")
    my_cursor = conn.cursor()
    my_cursor.execute("update user set is_logged_in=0 where email='{}'".format(email))
    request.session["logged_user"] = " "
    conn.commit()
    my_cursor.close()
    return redirect("home")

def dashboard(request):
    email = request.session["logged_user"]
    if email != " ":
        conn = mysql.connector.connect(host="localhost", username="root", password=PASSWORD, database="flight_deal_finder")
        my_cursor = conn.cursor()
        my_cursor.execute("select response from dashboard where email='{}'".format(email))
        responses = my_cursor.fetchall()
        final_responses = []
        for response in responses:
            final_responses.append(response[0])
        cr = []
        s = 0
        e = 3
        total_responses = len(final_responses)
        rows = total_responses // 3
        remainder = total_responses % 3
        for i in range(rows):
            cr.append(final_responses[s:e])
            s += 3
            e += 3
        if remainder != 0:
            cr.append(final_responses[s:s+remainder])
        context = {
            'response_rows': cr
        }
        return render(request, 'dashboard.html', context)
    else:
        messages.error(request, "Signin now!")
        return redirect("signin")
    
