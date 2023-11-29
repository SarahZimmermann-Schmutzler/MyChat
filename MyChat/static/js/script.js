
const wholeDate = new Date().toString();
const date = wholeDate.slice(4, 15)
let formdata = new FormData();
// brauchen formData, um Formular zu erstellen

/** function reads the data, sends it to backend and creates the message in the frontend with data from backend**/
async function sendMessage() {
    formdata.append('textmessage', messagefield.value);
    // let messagefield = document.getElementById('messagefield').value
    // nicht mehr notwendig, weil automatisch ausgeführt
    // append: name der Variable, die ans Backend gesendet werden soll und ihr Wert
    formdata.append('csrfmiddlewaretoken', token);
    // token muss mitgeschickt werden; definiert in base.html

    try {
        copyMessage();
        let response = await fetch('', {
            method: 'POST',
            body: formdata
        });
        // POST Request als JSON = Daten (=neue Message) an Server/Backend gesendet
        let json = await response.json();
        let message_data = JSON.parse(json);
        // response wird umgewandelt, damit wir im Frontend damit arbeiten können
        deleteMessagecopy();
        MessageFromBackend(message_data);
        clearMessagefield();
    } catch (e) {
        console.error('An error occured', e)
    }


    /** generates a copy of the message as placeholder until data from backed arrives **/
    function copyMessage() {
        messageContainer.innerHTML += `
            <div class="user-messages-index" id='deleteMessage'>
                <div class="message-user-index">
                    <span>{{request.user}}: <i>${messagefield.value}</i></span>
                    <div class="arrows-index">
                        <span>&#10003</span>
                    </div> 
                </div>
                <span class="color-grey">${date}</span>
            </div>
            `;
    }


    /** deletes placeholder **/
    function deleteMessagecopy() {
        document.getElementById('deleteMessage').remove();
    }


    /** creates the message with data from backend **/
    function MessageFromBackend(message_data) {
        messageContainer.innerHTML += `
            <div class="user-messages-index">
                <div class="message-user-index">
                    <span>{{request.user}}: <i>${message_data['fields']['text']}</i></span>
                    <div class="arrows-index">
                        <span>&#10003;&#10003;</span>
                    </div> 
                </div>
                <span class="color-grey">${date}</span>
            </div>`;
    }


    /** clears the inputfield **/
    function clearMessagefield() {
        messagefield.value = '';
    }
}