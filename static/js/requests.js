



// COOKIE SETTING AND FETCHING COOKIE
function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + encodeURIComponent(value) + expires+";path=/";
}

function getCookie(cookieName) {
    // Split the document.cookie string into individual cookies
    var cookies = document.cookie.split('; ');

    // Loop through the cookies to find the one with the specified name
    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i];
        var cookieParts = cookie.split('=');

        // Check if the cookie name matches the desired name
        if (cookieParts[0] === cookieName) {
            // Return the decoded value of the cookie
            return decodeURIComponent(cookieParts[1]);
        }
    }

    // Return null if the cookie with the specified name is not found
    return null;
}


function logout() {
    // Set the expiration date to a past date
    document.cookie = 'JMT_USER_JWT_TOKEN' + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    window.location.href = '/jamaat/auth/jamaat_login';
}






















// REQUEST FUNCTIONS TO API FOR AUTHENTICATION
function jamaat_login(){

    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var formData = new FormData($("#jamaat_auth_form")[0]); 


   $.ajax({
        url: '/jamaat/auth/login', // URL to send the request to
        type: 'POST',      // HTTP method (GET, POST, etc.)
        dataType: 'json', // Expected data type of the response
        data: formData,        // Data to be sent with the request
        processData: false,    // Prevent jQuery from processing the data
        contentType: false,    // Prevent jQuery from setting the content type
        headers: {
            'X-CSRFToken': csrfToken  // Include the CSRF token in the headers
        },
        success: function(response) {
            // Callback function for successful response
            if(response.status == 200){
                jwt_token = response.token;
                setCookie('JMT_USER_JWT_TOKEN', jwt_token, 7);
                window.location.href = '/jamaat/allocation/wajebaat_appointment';
            }else if(response.status == 404){
                document.getElementById('alert-box').style.display = 'block';
            }else{
                document.getElementById('alert-box').style.display = 'block';
            }
            
        },
        error: function(xhr, status, error) {
            // Callback function for errors
            document.getElementById('alert-box').style.display = 'block';        }
    });
}



















// REQUEST FUNCTIONS TO CREATE APPOINTMENT
function jamaat_create_wajebaat_appointment(){

    var accessToken = getCookie('JMT_USER_JWT_TOKEN');
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var formData = new FormData($("#create_wajebaat_appointment")[0]); 

    document.getElementById('alert-box-success').style.display = 'none';
    document.getElementById('alert-box-error').style.display = 'none';


   $.ajax({
        url: '/jamaat/allocation/api_wajebaat_create_appointment', // URL to send the request to
        type: 'POST',      // HTTP method (GET, POST, etc.)
        dataType: 'json', // Expected data type of the response
        data: formData,        // Data to be sent with the request
        processData: false,    // Prevent jQuery from processing the data
        contentType: false,    // Prevent jQuery from setting the content type
        headers: {
            'X-CSRFToken': csrfToken,
            'Authorization': 'Bearer ' + accessToken
        },
        success: function(response) {
            // Callback function for successful response
            if(response.status == 200){
                document.getElementById('alert-box-success').style.display = 'block';
            }else if(response.status == 400){
                document.getElementById('alert-box-error').style.display = 'block';
                document.getElementById('alert-box-error').innerHTML = response.error;
            }else{
                document.getElementById('alert-box-error').style.display = 'block';
                document.getElementById('alert-box-error').innerHTML = response.error;
            }
            
        },
        error: function(xhr, status, error) {
            // Callback function for errors
            document.getElementById('alert-box-error').style.display = 'block';        }
    });
}














// FUNCTIONS TO SET IDS FOR  FOR EDIT AND DELETE
function setAppointmentIDForEdit(obj, slot_amount, appointment_start_time, appointment_end_time){

    console.log('chk1')
    document.getElementById('edit_appointment_id').value = parseInt(obj.id.split('_')[1])
    document.getElementById('slot_amount').value = slot_amount;
    document.getElementById('appointment_start_time').value = appointment_start_time;
    document.getElementById('appointment_end_time').value = appointment_end_time;
    $('#editAppointmentModal').modal('show');

}

function setAppointmentIDForDelete(obj){
    document.getElementById('delete_appointment_id').value = parseInt(obj.id.split('_')[1])
}



function setAppointmentIDForClosed(obj){
    document.getElementById('close_appointment_id').value = parseInt(obj.id.split('_')[1])
}









// FUNCTIONS TO EDIT OR DELETE APPOINTMENTS
function jamaat_edit_wajebaat_appointment(){

    var accessToken = getCookie('JMT_USER_JWT_TOKEN');
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var formData = new FormData($("#edit_wajebaat_appointment")[0]); 
    var appointment_id = document.getElementById('edit_appointment_id').value;


   $.ajax({
        url: '/jamaat/allocation/api_wajebaat_edit_appointment/'+appointment_id, // URL to send the request to
        type: 'PUT',      // HTTP method (GET, POST, etc.)
        dataType: 'json', // Expected data type of the response
        data: formData,        // Data to be sent with the request
        processData: false,    // Prevent jQuery from processing the data
        contentType: false,    // Prevent jQuery from setting the content type
        headers: {
            'X-CSRFToken': csrfToken,
            'Authorization': 'Bearer ' + accessToken
        },
        success: function(response) {
            // Callback function for successful response
            if(response.status == 200){
                window.location.reload();
            }else if(response.status == 404){
                document.getElementById('alert-box-error').style.display = 'block';
                document.getElementById('alert-box-error').innerHTML = response.error;
            }else{
                document.getElementById('alert-box-error').style.display = 'block';
                document.getElementById('alert-box-error').innerHTML = response.error;
            }
            
        },
        error: function(xhr, status, error) {
            // Callback function for errors
            document.getElementById('alert-box-error').style.display = 'block';        }
    });
}




function jamaat_delete_wajebaat_appointment(){

    var accessToken = getCookie('JMT_USER_JWT_TOKEN');
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var appointment_id = document.getElementById('delete_appointment_id').value;


   $.ajax({
        url: '/jamaat/allocation/api_wajebaat_delete_appointment/'+appointment_id, // URL to send the request to
        type: 'DELETE',      // HTTP method (GET, POST, etc.)
        dataType: 'json', // Expected data type of the response
        processData: false,    // Prevent jQuery from processing the data
        contentType: false,    // Prevent jQuery from setting the content type
        headers: {
            'X-CSRFToken': csrfToken,
            'Authorization': 'Bearer ' + accessToken
        },
        success: function(response) {
            // Callback function for successful response
            if(response.status == 200){
                window.location.reload();
            }else if(response.status == 404){
                document.getElementById('alert-box-error').style.display = 'block';
                document.getElementById('alert-box-error').innerHTML = response.error;
            }else{
                document.getElementById('alert-box-error').style.display = 'block';
                document.getElementById('alert-box-error').innerHTML = response.error;
            }
            
        },
        error: function(xhr, status, error) {
            // Callback function for errors
            document.getElementById('alert-box-error').style.display = 'block';        }
    });
}




function jamaat_close_wajebaat_appointment(){

    var accessToken = getCookie('JMT_USER_JWT_TOKEN');
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var appointment_id = document.getElementById('close_appointment_id').value;

    var payload = {
        'event_flag': false
    }


   $.ajax({
        url: '/jamaat/allocation/api_wajebaat_edit_appointment/'+appointment_id, // URL to send the request to
        type: 'PUT',      // HTTP method (GET, POST, etc.)
        data: JSON.stringify(payload),
        dataType: 'json', // Expected data type of the response
        processData: false,    // Prevent jQuery from processing the data
        contentType: false,    // Prevent jQuery from setting the content type
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
            'Authorization': 'Bearer ' + accessToken
        },
        success: function(response) {
            // Callback function for successful response
            if(response.status == 200){
                window.location.reload();
            }else if(response.status == 404){
                document.getElementById('alert-box-error').style.display = 'block';
                document.getElementById('alert-box-error').innerHTML = response.error;
            }else{
                document.getElementById('alert-box-error').style.display = 'block';
                document.getElementById('alert-box-error').innerHTML = response.error;
            }
            
        },
        error: function(xhr, status, error) {
            // Callback function for errors
            document.getElementById('alert-box-error').style.display = 'block';        }
    });
}















// FUNCTIONS TO FETCH MUMIN MASTER LIST
function fetch_mumin_list(page){
    var accessToken = getCookie('JMT_USER_JWT_TOKEN');
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    let url = '';
    var pageSize = 20;


    if(page == 1){
        url = '/jamaat/allocation/api_wajebaat_mumin_list';
    }else{
        url = '/jamaat/allocation/api_wajebaat_mumin_list?page='+page;
    }


    console.log(url);

   $.ajax({
        url: url, // URL to send the request to
        type: 'GET',      // HTTP method (GET, console.log(url);POST, etc.)
        dataType: 'json', // Expected data type of the response
        processData: false,    // Prevent jQuery from processing the data
        contentType: false,    // Prevent jQuery from setting the content type
        headers: {
            'X-CSRFToken': csrfToken,
            'Authorization': 'Bearer ' + accessToken
        },
        success: function(response) {
            // Callback function for successful response
            if(response.results.status == 200){

                var tbody = document.getElementById('mumin_list_rows');

                if(response.count == 0){
                    tbody.innerHTML = `
                    <tr>
                        <td colspan="6">
                            <div class="alert alert-secondary" role="alert">
                              No data is uploaded. Please upload mumineen data using Upload Mumineen HOFs.
                            </div>
                        </td>
                    </tr>
                    `;
                    return;
                }

                tbody.innerHTML = '';

                for (let i = 0; i < response.results.results.length; i++) {
                    
                    var tr = document.createElement('tr');
                    var td1 = document.createElement('td');
                    var td2 = document.createElement('td');
                    var td3 = document.createElement('td');
                    var td4 = document.createElement('td');
                    var td5 = document.createElement('td');
                    var td6 = document.createElement('td');

                    td1.textContent = response.results.results[i].mumin_its;
                    td2.textContent = response.results.results[i].full_name;
                    td3.textContent = response.results.results[i].age;
                    td4.textContent = response.results.results[i].gender;
                    td5.textContent = response.results.results[i].sector;
                    td6.textContent = response.results.results[i].sub_sector;
                    
                    tr.appendChild(td1);
                    tr.appendChild(td2);
                    tr.appendChild(td3);
                    tr.appendChild(td4);
                    tr.appendChild(td5);
                    tr.appendChild(td6);

                    tbody.appendChild(tr);


                }

                document.getElementById('pagination_block').style.display = "block";

            }else if(response.status == 404){
                document.getElementById('alert-box-error').style.display = 'block';
                document.getElementById('alert-box-error').innerHTML = response.error;
            }else{
                document.getElementById('alert-box-error').style.display = 'block';
                document.getElementById('alert-box-error').innerHTML = response.error;
            }
            
        },
        error: function(xhr, status, error) {
            // Callback function for errors
            document.getElementById('alert-box-error').style.display = 'block';        }
    });
}



function markSelectedPage(obj){
    var pageLinks = document.querySelectorAll('.page-link');

    // Loop through each element and set the styles
    pageLinks.forEach(function(link) {
        link.style.color = 'white';
        link.style.backgroundColor = 'black';
        link.classList.remove('current-page');
    });

    obj.style.color = 'black';
    obj.style.backgroundColor = 'white';
    obj.classList.add('current-page');

    console.log(obj.innerHTML);

    fetch_mumin_list(parseInt(obj.innerHTML));

}


function prevNextActionHandler(obj){
    identifier = obj.innerHTML;
    prev_ref = document.getElementById('prev_ref').innerHTML;
    next_ref = document.getElementById('next_ref').innerHTML;

    if(identifier == "Previous"){
        if(prev_ref == 1){
            return;
        }else{
            document.getElementById('prev_ref').innerHTML = parseInt(prev_ref)-5;
            document.getElementById('2nd').innerHTML = parseInt(prev_ref)-4;
            document.getElementById('3rd').innerHTML = parseInt(prev_ref)-3;
            document.getElementById('4th').innerHTML = parseInt(prev_ref)-2;
            document.getElementById('next_ref').innerHTML = parseInt(prev_ref)-1;

            markSelectedPage(document.getElementById('next_ref'));
        }
    }


    if(identifier == "Next"){
        if(next_ref < 5){
            return;
        }else{
            document.getElementById('prev_ref').innerHTML = parseInt(next_ref)+1;
            document.getElementById('2nd').innerHTML = parseInt(next_ref)+2;
            document.getElementById('3rd').innerHTML = parseInt(next_ref)+3;
            document.getElementById('4th').innerHTML = parseInt(next_ref)+4;
            document.getElementById('next_ref').innerHTML = parseInt(next_ref)+5;

            markSelectedPage(document.getElementById('prev_ref'));
        }
    }



}















// FUNCTIONS TO INSERT MUMIN MASTER LIST
function jamaat_upload_mumineen_list(){

    var accessToken = getCookie('JMT_USER_JWT_TOKEN');
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var formData = new FormData($("#upload_mumineen_list")[0]); 


   $.ajax({
        url: '/jamaat/allocation/api_wajebaat_mumin_create_by_csv', // URL to send the request to
        type: 'POST',      // HTTP method (GET, POST, etc.)
        dataType: 'json', // Expected data type of the response
        data: formData,        // Data to be sent with the request
        processData: false,    // Prevent jQuery from processing the data
        contentType: false,    // Prevent jQuery from setting the content type
        headers: {
            'X-CSRFToken': csrfToken,
            'Authorization': 'Bearer ' + accessToken
        },
        success: function(response) {
            // Callback function for successful response
            if(response.status == 200){
                document.getElementById('alert-box-success').style.display = 'block';
                fetch_mumin_list(1);
            }else if(response.status == 404){
                document.getElementById('alert-box-error').style.display = 'block';
                document.getElementById('alert-box-error').innerHTML = response.error;
            }else{
                document.getElementById('alert-box-error').style.display = 'block';
                document.getElementById('alert-box-error').innerHTML = response.error;
            }
            
        },
        error: function(xhr, status, error) {
            // Callback function for errors
            document.getElementById('alert-box-error').style.display = 'block';        }
    });
}



















// FUNCTIONS TO GET MUMIN REGISTRATION STATUS
function fetch_mumin_registration_status(){

    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var mumin_its = parseInt(document.getElementById('mumin_its').value);

    document.getElementById('verification-alert-box-success').style.display = 'none';
    document.getElementById('verification-alert-box-error').style.display = 'none';

   $.ajax({
        url: '/jamaat/mumin/api_mumin_registration_status/'+mumin_its, // URL to send the request to
        type: 'GET',            // HTTP method (GET, POST, etc.)
        dataType: 'json',       // Expected data type of the response
        processData: false,     // Prevent jQuery from processing the data
        contentType: false,     // Prevent jQuery from setting the content type
        headers: {
            'X-CSRFToken': csrfToken,
        },
        success: function(response) {
            
            if(response.status == 200){
                document.getElementById("mumin_name").innerHTML = "Name of the HOF:"+response.mumin_full_name;
                document.getElementById('verification-alert-box-success').style.display = 'block';
                document.getElementById('mumin_token_registration_form').style.display = "block";
            }else if(response.status == 400){
                document.getElementById('verification-alert-box-error').style.display = 'block';
                document.getElementById('verification-alert-box-error').innerHTML = response.error;
            }else if(response.status == 300){
                document.getElementById('verification-alert-box-info').style.display = 'block';
                
                document.getElementById("redirect-token-link").href = response.redirect_link;

            }else{
                document.getElementById('verification-alert-box-error').style.display = 'block';
                document.getElementById('verification-alert-box-error').innerHTML = response.error;
            }
            
        },
        error: function(xhr, status, error) {
            // Callback function for errors
            document.getElementById('alert-box-error').style.display = 'block';        }
    });
}












// REQUEST FUNCTIONS TO GENERATE AND POST TOKEN FOR MUMIN
function string_to_numerical_date(date_string){

    // Parse the date using the Date object
    var date = new Date(date_string);

    // Get month, day, and year components
    var month = (date.getMonth() + 1).toString().padStart(2, '0'); // Adding 1 because months are zero-based
    var day = date.getDate().toString().padStart(2, '0');
    var year = date.getFullYear().toString();

    // Formatted date string
    var formattedDate = day + month;

    return formattedDate;
}



function create_mumin_registration_with_token(obj){

    obj.disabled = true;
    obj.innerHTML = `
        <span class="spinner-grow spinner-grow-sm" aria-hidden="true"></span>
        <span class="visually-hidden" role="status">Generating Token...</span>
    `;

    var mumin_its = parseInt(document.getElementById('mumin_its').value);

    document.getElementById('alert-box-success').style.display = 'none';
    document.getElementById('alert-box-error').style.display = 'none';

    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

    var appointments = document.getElementById("appointments");
    var appointmentOption = appointments.options[appointments.selectedIndex];
    var date_of_appointment = appointmentOption.id.split('_');

    var slot_no = appointmentOption.value.split('_');

    var start_ref = slot_no[0]-slot_no[1]+1;
    console.log(start_ref);

    var slot_token_date_prefix = string_to_numerical_date(date_of_appointment[1])

    var slot_token = "WJBT"+""+slot_token_date_prefix;


    var payload = {
        'mumin_its': mumin_its,
        'appointment_id': date_of_appointment[0],
        'slot_token': slot_token
    }

    console.log(payload);

    $.ajax({
        url: '/jamaat/mumin/api_mumin_appointment_register', // URL to send the request to
        type: 'POST',      // HTTP method (GET, POST, etc.)
        dataType: 'json', // Expected data type of the response
        data: JSON.stringify(payload),        // Data to be sent with the request
        processData: false,    // Prevent jQuery from processing the data
        contentType: false,    // Prevent jQuery from setting the content type
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        success: function(response) {
            // Callback function for successful response
            if(response.status == 200){
                obj.innerHTML = `
                    Token generated!
                `;
                document.getElementById('alert-box-success').style.display = 'block';
                window.location.href = '/jamaat/mumin/mumin_registration_token?token='+response.new_token;
            }else if(response.status == 404){
                document.getElementById('alert-box-error').style.display = 'block';
                document.getElementById('alert-box-error').innerHTML = response.error;
            }else{
                document.getElementById('alert-box-error').style.display = 'block';
                document.getElementById('alert-box-error').innerHTML = response.error;
            }
            
        },
        error: function(xhr, status, error) {
            // Callback function for errors
            document.getElementById('alert-box-error').style.display = 'block';        }
    });


}













// REQUEST FUNCTIONS TO DELETE AND CANCEL TOKEN
function mumin_cancel_token(){

    var accessToken = getCookie('JMT_USER_JWT_TOKEN');
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var token = document.getElementById('token').innerHTML;


   $.ajax({
        url: '/jamaat/mumin/api_mumin_appointment_cancel_token/'+token, // URL to send the request to
        type: 'DELETE',      // HTTP method (GET, POST, etc.)
        dataType: 'json', // Expected data type of the response
        processData: false,    // Prevent jQuery from processing the data
        contentType: false,    // Prevent jQuery from setting the content type
        headers: {
            'X-CSRFToken': csrfToken,
            'Authorization': 'Bearer ' + accessToken
        },
        success: function(response) {
            // Callback function for successful response
            if(response.status == 204){
                window.location.href = '/jamaat/mumin/mumin_self_allocation/home';
            }else if(response.status == 404){
                document.getElementById('alert-box-error').style.display = 'block';
                document.getElementById('alert-box-error').innerHTML = response.error;
            }else{
                document.getElementById('alert-box-error').style.display = 'block';
                document.getElementById('alert-box-error').innerHTML = response.error;
            }
            
        },
        error: function(xhr, status, error) {
            // Callback function for errors
            document.getElementById('alert-box-error').style.display = 'block';        }
    });
}


















function updateURL() {
  const dateValue = document.getElementById('date_filter').value;
  const timeValue = document.getElementById('appointment_start_time').value;
  const urlParams = new URLSearchParams(window.location.search);

  // Set or update the 'date' parameter with the new date value
  urlParams.set('date', dateValue);
  // Set or update the 'time' parameter with the new time value
  urlParams.set('time', timeValue);

  // Construct the new URL with the updated parameters
  const newURL = `${window.location.pathname}?${urlParams.toString()}`;

  // Replace the current URL with the updated one
  window.history.replaceState({}, '', newURL);
}







function getURLParams() {
  const urlParams = new URLSearchParams(window.location.search);
  const dateParam = urlParams.get('date');
  const timeParam = urlParams.get('time');
  return { date: dateParam, time: timeParam };
}








// REQUEST FUNCTION TO FETCH THE REGISTRATION DATA FOR THE SLOTS
function fetch_registration_list(page){

    document.getElementById("registration_data_rows").innerHTML = "";

    const urlParams = getURLParams();

    var date_val = document.getElementById("date_filter").value;
    var appointment_start_time = document.getElementById("appointment_start_time").value;
    let payload = {}


    var accessToken = getCookie('JMT_USER_JWT_TOKEN');
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    let url = '';
    var pageSize = 20;


    if(page == 1){
        url = '/jamaat/allocation/api_wajebaat_registration_data';
    }else{
        url = '/jamaat/allocation/api_wajebaat_registration_data?page='+page;
    }


    if(date_val != ''){
        payload['date'] = date_val;
    }else if(urlParams.date){
        payload['date'] = urlParams.date;
    }

    if(appointment_start_time != ''){
        payload['appointment_start_time'] = appointment_start_time;
    }else if(urlParams.time){
        payload['appointment_start_time'] = urlParams.time;
    }

    console.log(payload)

   $.ajax({
        url: url, // URL to send the request to
        type: 'GET',      // HTTP method (GET, console.log(url);POST, etc.)
        dataType: 'json', // Expected data type of the response
        data: payload,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
            'Authorization': 'Bearer ' + accessToken
        },
        success: function(response) {
            // Callback function for successful response
            if(response.results.status == 200){

                var tbody = document.getElementById('registration_data_rows');

                if(response.count == 0){
                    tbody.innerHTML = `
                    <tr>
                        <td colspan="6">
                            <div class="alert alert-secondary" role="alert">
                              No mumin has yet registered for Takhmeem. Registration data will flow in once mumineen starts selecting and confirming slots..
                            </div>
                        </td>
                    </tr>
                    `;
                    return;
                }

                tbody.innerHTML = '';

                for (let i = 0; i < response.results.results.length; i++) {

                    
                    var tr = document.createElement('tr');
                    var td1 = document.createElement('td');
                    var td2 = document.createElement('td');
                    var td3 = document.createElement('td');
                    var td4 = document.createElement('td');
                    var td5 = document.createElement('td');
                    var td6 = document.createElement('td');

                    td1.textContent = response.results.results[i].appointment_id.date;
                    td2.textContent = response.results.results[i].mumin_its.mumin_its;
                    td3.textContent = response.results.results[i].mumin_its.full_name;;
                    td4.textContent = response.results.results[i].slot_token;
                    td5.textContent = response.results.results[i].appointment_id.appointment_start_time+" - "+response.results.results[i].appointment_id.appointment_end_time;
                    if(response.results.results[i].status){
                            td6.innerHTML = `<span class="badge rounded-pill text-bg-success">Takhmeem Done</span>`;
                    }else{
                        td6.innerHTML = `
                            <span class="badge rounded-pill text-bg-warning">Takhmeem Not Done</span>
                            &nbsp;&nbsp;&nbsp;&nbsp;
                            <button class="btn btn-dark btn-sm" onclick="toggle_wajebaat_takhmeem_status(`+response.results.results[i].slot_id+`)">Mark as Done</button>
                        `;
                    }
                    
                    
                    tr.appendChild(td1);
                    tr.appendChild(td2);
                    tr.appendChild(td3);
                    tr.appendChild(td4);
                    tr.appendChild(td5);
                    tr.appendChild(td6);

                    tbody.appendChild(tr);


                }

                document.getElementById('pagination_block').style.display = "block";

            }else if(response.status == 404){
                document.getElementById('alert-box-error').style.display = 'block';
                document.getElementById('alert-box-error').innerHTML = response.error;
            }else{
                document.getElementById('alert-box-error').style.display = 'block';
                document.getElementById('alert-box-error').innerHTML = response.error;
            }
            
        },
        error: function(xhr, status, error) {
            // Callback function for errors
            document.getElementById('alert-box-error').style.display = 'block';        }
    });
}


function markSelectedRegistrationPage(obj){
    var pageLinks = document.querySelectorAll('.page-link');

    // Loop through each element and set the styles
    pageLinks.forEach(function(link) {
        link.style.color = 'white';
        link.style.backgroundColor = 'black';
        link.classList.remove('current-page');
    });

    obj.style.color = 'black';
    obj.style.backgroundColor = 'white';
    obj.classList.add('current-page');

    fetch_registration_list(parseInt(obj.innerHTML));

}



function prevNextRegistrationActionHandler(obj){
    identifier = obj.innerHTML;
    prev_ref = document.getElementById('prev_ref').innerHTML;
    next_ref = document.getElementById('next_ref').innerHTML;

    if(identifier == "Previous"){
        if(prev_ref == 1){
            return;
        }else{
            document.getElementById('prev_ref').innerHTML = parseInt(prev_ref)-5;
            document.getElementById('2nd').innerHTML = parseInt(prev_ref)-4;
            document.getElementById('3rd').innerHTML = parseInt(prev_ref)-3;
            document.getElementById('4th').innerHTML = parseInt(prev_ref)-2;
            document.getElementById('next_ref').innerHTML = parseInt(prev_ref)-1;

            markSelectedRegistrationPage(document.getElementById('next_ref'));
        }
    }


    if(identifier == "Next"){
        if(next_ref < 5){
            return;
        }else{
            document.getElementById('prev_ref').innerHTML = parseInt(next_ref)+1;
            document.getElementById('2nd').innerHTML = parseInt(next_ref)+2;
            document.getElementById('3rd').innerHTML = parseInt(next_ref)+3;
            document.getElementById('4th').innerHTML = parseInt(next_ref)+4;
            document.getElementById('next_ref').innerHTML = parseInt(next_ref)+5;

            markSelectedRegistrationPage(document.getElementById('prev_ref'));
        }
    }

}



















// REQUEST FUNCTION TO TOGGLE THE TAKHMEEM STATUS
function toggle_wajebaat_takhmeem_status(id){


    var accessToken = getCookie('JMT_USER_JWT_TOKEN');

    var payload = {
        'status': true
    }

    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();



    $.ajax({
        url: '/jamaat/allocation/api_toggle_takhmeem_status/'+id, // URL to send the request to
        type: 'PUT',      // HTTP method (GET, POST, etc.)
        dataType: 'json', // Expected data type of the response
        data: JSON.stringify(payload),
        processData: false,    // Prevent jQuery from processing the data
        contentType: false,    // Prevent jQuery from setting the content type
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
            'Authorization': 'Bearer ' + accessToken
        },
        success: function(response) {
            // Callback function for successful response
            if(response.status == 200){
                document.getElementById('alert-box-success').style.display = 'block';
                setTimeout(window.location.reload(), 3000);
            }else if(response.status == 404){
                document.getElementById('alert-box-error').style.display = 'block';
                document.getElementById('alert-box-error').innerHTML = response.error;
            }else{
                document.getElementById('alert-box-error').style.display = 'block';
                document.getElementById('alert-box-error').innerHTML = response.error;
            }
            
        },
        error: function(xhr, status, error) {
            // Callback function for errors
            document.getElementById('alert-box-error').style.display = 'block';        }
    });
}















// DOWNLOAD THE REGISTRATION DATA AS CSV

function downloadCSV() {


    var date_val = document.getElementById("date_filter").value;
    var appointment_start_time = document.getElementById("appointment_start_time").value;
    let payload = {}


    var accessToken = getCookie('JMT_USER_JWT_TOKEN');
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    let url = '/jamaat/allocation/export_csv?date='+date_val+"&appointment_start_time="+appointment_start_time;



    $.ajax({
        url: url, // URL to send the request to
        type: 'GET',      // HTTP method (GET, POST, etc.)
        dataType: 'text', // Expected data type of the response
        processData: false,    // Prevent jQuery from processing the data
        contentType: false,    // Prevent jQuery from setting the content type
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
            'Authorization': 'Bearer ' + accessToken
        },
        success: function(response) {
            const csvData = response;

            // Convert the CSV data to a Blob
            const blob = new Blob([csvData], { type: 'text/csv;charset=utf-8;' });

            // Create a temporary link element
            const link = document.createElement('a');
            const url = URL.createObjectURL(blob);

            // Set link attributes
            link.href = url;
            link.download = "Jamaat Report" +(date_val ? ` ${date_val}` : "") +(appointment_start_time ? ` Slot time: ${appointment_start_time}` : "")+'.csv';

            // Append the link to the document
            document.body.appendChild(link);

            // Trigger a click event on the link to initiate the download
            link.click();

            // Remove the link from the document
            document.body.removeChild(link);
        },
        error: function(xhr, status, error) {
            console.log(error);
            // Callback function for errors
            document.getElementById('alert-box-error').style.display = 'block';
        }
    });


    
}