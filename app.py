from flask import Flask
from connections import postgres_connection
from flask import request, json,  Response
from flask_api import status
from validate_request_body import *
import configparser

conf = configparser.ConfigParser()
conf.read("config.ini")
username = conf.get('postgres', 'username')
password = conf.get('postgres', 'password')
port = conf.get('postgres', 'port')
database = conf.get('postgres', 'database')
hostname = conf.get('postgres', 'hostname')

app = Flask(__name__)

pgre_conn = postgres_connection(username, password, port, database, hostname)


@app.route('/xride_data', methods=["POST"])
def xride_data():
    try:
        data = request.data
        data = json.loads(data)
        booking_id = validate_keys(data, 'booking_id', int)
        user_id = validate_keys(data, 'user_id', int)
        vehicle_model_id = validate_keys(data, 'vehicle_model_id', int)
        package_id = validate_keys(data, 'package_id', int)
        travel_type_id = validate_keys(data, 'travel_type_id', int)
        from_area_id = validate_keys(data, 'from_area_id', int)
        to_area_id = validate_keys(data, 'to_area_id', int)
        from_city_id = validate_keys(data, 'from_city_id', int)
        to_city_id = validate_keys(data, 'to_city_id', int)
        from_date = validate_date(data, 'from_date')
        to_date = validate_date(data, 'to_date')
        online_booking = validate_keys(data, 'online_booking', int)
        mobile_site_booking = validate_keys(data, 'mobile_site_booking', int)
        booking_created = validate_date(data, 'booking_created')
        from_lat = validate_keys(data, 'from_lat', float)
        from_long = validate_keys(data, 'from_long', float)
        to_lat = validate_keys(data, 'to_lat', float)
        to_long = validate_keys(data, 'to_long', float)
        driver_id = validate_keys(data, 'driver_id', int)
        
        cur = pgre_conn.cursor()
        try:
            cur.execute("INSERT INTO cab_drivers ( driver_id, vehicle_model_id) VALUES (%s, %s) ;",
                        (driver_id, vehicle_model_id,))
            cur.execute("INSERT INTO customers (user_id) VALUES (%s) ;", (user_id,))
            cur.execute(
                "INSERT INTO cab_rides (user_id, driver_id, booking_id, package_id, travel_type_id, "
                "from_area_id, to_area_id, from_city_id, to_city_id, from_date, to_date, online_booking, "
                "mobile_site_booking, booking_created, from_lat, from_long, to_lat, to_long) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ;",
                (user_id, driver_id, booking_id, package_id, travel_type_id, from_area_id,
                 to_area_id, from_city_id, to_city_id, from_date, to_date, online_booking, mobile_site_booking,
                 booking_created, from_lat, from_long, to_lat, to_long,))
            pgre_conn.commit()

        except Exception as _:
            pgre_conn.rollback()
            raise FunctionalError(xride_data, "Query Execution Failed")

        cur.close()
        pgre_conn.close()

        response = Response(
            response=json.dumps({"booking_id": booking_id, "status": "Success"}),
            status=status.HTTP_200_OK,
            mimetype='application/json'
        )
        return response
    except ValidationError as error:
        return Response(
            response=json.dumps({"error_message": error.msg, "status": "Failed"}),
            status=error.status_code,
            mimetype='application/json'
        )
    except FunctionalError as _:
        return Response(
            response=json.dumps({"error_message": "Internal Server Error", "status": "Failed"}),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            mimetype='application/json'
        )
    except Exception as _:
        return Response(
            response=json.dumps({"error_message": "Internal Server Error"}),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            mimetype='application/json'
        )


if __name__ == '__main__':
    app.run('0.0.0.0')
