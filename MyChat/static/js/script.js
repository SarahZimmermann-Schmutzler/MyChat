// senden Daten an Backend und geben sie wieder aus
async function sendMessage() {
    let formdata = new FormData();
    // brauchen formData, um Formular zu erstellen
    formdata.append('textmessage', messagefield.value);
    // let messagefield = document.getElementById('messagefield').value
    // nicht mehr notwendig, weil automatisch ausgeführt
    // append: name der Variable, die ans Backend gesendet werden soll und ihr Wert

    let token = '{{csrf_token}}'
    formdata.append('csrfmiddlewaretoken', token);
    // token muss mitgeschickt werden

    try {
        const wholeDate = new Date().toString();
        const date = wholeDate.slice(4, 15)
        messageContainer.innerHTML += `
            <div class="user-messages" id='deleteMessage'>
                <div class="message-user">
                    <span>{{request.user}}: <i>${messagefield.value}</i></span>
                    <div class="arrows">
                        <span>&#10003</span>
                    </div> 
                </div>
                <span class="color-grey">${date}</span>
            </div>
            `;
        // Kopie der neuen Nachricht wird generiert mit einem weißen Haken



        let response = await fetch('', {
            method: 'POST',
            body: formdata
        });
        // POST Request als JSON = Daten (=neue Message) an Server/Backend gesendet

        let json = await response.json();
        let message_data = JSON.parse(json);
        // response wird umgewandelt, damit wir im Frontend damit arbeiten können
        // console.log('json is', json)
        // console.log('message data', message_data)

        document.getElementById('deleteMessage').remove();
        // Platzhalter wird wieder entfernt


        messageContainer.innerHTML += `
            <div class="user-messages">
                <div class="message-user">
                    <span>{{request.user}}: <i>${message_data['fields']['text']}</i></span>
                    <div class="arrows">
                        <span>&#10003;&#10003;</span>
                    </div> 
                </div>
                <span class="color-grey">${date}</span>
            </div>`;
        // jetzt zumindest beim Text Original Backend-Daten

        messagefield.value = '';
        // Messagefield leeren

        console.log('Success!')


    } catch (e) {
        console.error('An error occured', e)
    }
}