function goBack() {
 window.history.back();
};


function listen_to_changes(){

/******* FIREBASE INITIALIZATION ****************/
  var config = {
        apiKey: "AIzaSyCHL_Er9JtpQbadJtoaZbvYusIY-tBRVC0",
        authDomain: "guardapp-ac65a.firebaseapp.com",
        databaseURL: "https://guardapp-ac65a.firebaseio.com",
        storageBucket: "guardapp-ac65a.appspot.com",
        messagingSenderId: "299985780377"
      };

  firebase.initializeApp(config);
  var db = firebase.database();
  var rooms = db.ref('sensor/');
  /***********************************************/

  previous = 0;

  rooms.on('value', function(snapshot) {
    data = snapshot.val();
    data1 = snapshot.val();
    name = Object.keys(data)[0];

   var rasps = document.getElementsByClassName("keys"); //rasps_names
    // for (var i=0; i < rasps.length; i++) console.log(rasps[i].innerHTML);

    for (var i=0; i < rasps.length; i++) {
        if (name == rasps[i].innerHTML) {
            data = Object.values(data)[0];
            if (typeof previous.COSensor !== 'undefined'){

                for (sensor_name in data) {
                    val1 = Object.values(previous[sensor_name])[0];
                    val2 = Object.values(data[sensor_name])[0];
                    if ( val1 < val2) {
                        console.log('Danger in' , sensor_name);
                        changed_sensor = sensor_name;
                        $("#danger_title").text("Danger in " + name);
                        $('#danger_sensor').text("Sensor name: " + changed_sensor);
                        $('#danger_previous').text("Previous value: " + val1);
                        $('#danger_current').text("Current value: " + val2);
                        $('#modal_button').attr("href", "/rasp/"+name+"/")
                        $('#alert_modal').modal('show');
                        }
                    }

             }
             previous = data;
        }
    }
    });
} ;

function select_button(key){
    $('#'+ key).addClass('active');
};